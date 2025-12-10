import os
import logging
import pydantic
from functools import lru_cache
from pypipedrive import utils
from pypipedrive.api import Api, ApiResponse, V1, V2
from pypipedrive.orm.fields import Field
from pypipedrive.orm.types import FieldName, ItemSearchDict, EntityUpdateDict
from typing import Any, Dict, List, Optional, Union, Set
from typing_extensions import Self


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class SaveResult(pydantic.BaseModel):
    """
    Represents the result of saving a record to the API. The result's
    attributes contain more granular information about the save operation:

        >>> result = model.save()
        >>> result.id
        123
        >>> result.created
        False
        >>> result.updated
        True
        >>> result.forced
        False
        >>> result.field_names
        {'Name', 'Email'}

    If none of the model's fields have changed, calling :meth:`~pipedrive.orm.Model.save`
    will not perform any API requests and will return a SaveResult with no changes.

        >>> model = Model()
        >>> result = model.save()
        >>> result.saved
        True
        >>> second_result = model.save()
        >>> second_result.saved
        False
    """

    id:        Union[int, str]
    created:   bool = False
    updated:   bool = False
    forced:    bool = False
    field_names: Set[FieldName] = pydantic.Field(default_factory=set)

    def __bool__(self) -> bool:
        """
        Returns ``True`` if the record was created.
        """
        return self.created

    @property
    def saved(self) -> bool:
        """
        Whether the record was saved to the API. If ``False``, this indicates there
        were no changes to the model and the :meth:`~pipedrive.orm.Model.save`
        operation was not forced.
        """
        return self.created or self.updated


class Model:
    """
    Model class. `custom_` is a reserved keyword for Pipedrive entity custom 
    fields that map to field api key.
    """

    _deleted: bool = False
    _fetched: bool = False
    _init:    bool = False  # Indicates if the instance is being initialized
    _fields:  Dict[FieldName, Any]
    _changed: Dict[FieldName, bool]

    def __init__(self, **fields):
        """
        `fields` is a dictionary of Pipedrive record field names to fields.
        """
        # Indicate that initialization is in progress. Used to bypass raise when
        # field is read-only.
        self._init = True
        self._fields: Dict[str, Any] = {}
        try:
            # Populate internal storage for `id` directly to avoid triggering
            # Field.__set__ (which enforces readonly). This is intentional so
            # that constructing models from API records (which may include
            # readonly fields like `id`) does not raise during initialization.
            value_id = fields.pop("id")
            id_field = getattr(type(self), "id", None)
            key = getattr(id_field, "_attribute_name", "id") if id_field is not None else "id"
            self._fields[key] = value_id
        except KeyError:
            pass

        _attribute_descriptor_map = self._attribute_descriptor_map()
        for key, value in fields.items():
            if key in _attribute_descriptor_map:
                setattr(self, key, value)

        # Only start tracking changes after the object is created
        self._changed ={}
        # Initialization complete
        self._init = False

    def __init_subclass__(cls, **kwargs: Any):
        cls._validate_class()
        super().__init_subclass__(**kwargs)

    def __repr__(self) -> str:
        id = self._get_id()
        if not id:
            return f"<unsaved {self.__class__.__name__}>"
        return f"<{self.__class__.__name__} id={id!r}>"

    def _get_id(self) -> Optional[Union[int, str]]:
        """
        Get the instance ID. Helper method to lookup the Meta.field_id attribute.
        """
        field_id = self._get_meta("field_id")
        if field_id is None:
            return self.id
        return getattr(self, field_id, None)

    @classmethod
    def _get_meta(
        cls,
        name: str,
        default: Any = None,
        required: bool = False,
        call: bool = True) -> Any:
        """
        Retrieves the value of a Meta attribute.

        Args:
            default: The default value to return if the attribute is not set.
            required: Raise an exception if the attribute is not set.
            call: If the value is callable, call it before returning a result.
        """
        if not hasattr(cls, "Meta"):
            raise AttributeError(f"{cls.__name__}.Meta must be defined")
        if not hasattr(cls.Meta, name):
            if required:
                raise ValueError(f"{cls.__name__}.Meta.{name} must be defined")
            return default
        value = getattr(cls.Meta, name)
        if call and callable(value):
            value = value()
        if required and value is None:
            raise ValueError(f"{cls.__name__}.Meta.{name} cannot be None")
        return value

    @classmethod
    def _validate_class(cls) -> None:
        """
        Validate the model class to ensure it meets required criteria.
        """
        # Check that required Meta attributes are set (but don't call any callables)
        assert cls._get_meta("entity_name", required=True, call=False)
        assert cls._get_meta("version", required=True, call=False)

        model_attributes = [a for a in cls.__dict__.keys() if not a.startswith("__")]
        # Model methods allowed to be overridden at the model level.
        ALLOWED_OVERRIDE_METHODS = [
            "all", "iterator", "get", "save", "update", "delete",
            "batch_delete", "files", "changelog"
        ]
        model_keys = [k for k in Model.__dict__.keys() if k not in ALLOWED_OVERRIDE_METHODS]
        overridden = set(model_attributes).intersection(model_keys)
        if overridden:
            raise ValueError(
                "Class {cls} fields clash with existing method: {name}".format(
                    cls=cls.__name__, name=overridden
                )
            )

    @classmethod
    def _attribute_descriptor_map(cls) -> Dict[str, Any]:
        """
        Build a mapping of the model's attribute names to field descriptor
        instances, including inherited attributes.

        >>> class Test(Model):
        ...     first_name = TextField("First Name")
        ...     age = NumberField("Age")
        ...
        >>> Test._attribute_descriptor_map()
        >>> {
        ...     "field_name": <TextField field_name="First Name">,
        ...     "another_Field": <NumberField field_name="Age">,
        ... }
        """
        attributes = {}
        for base in cls.__mro__:
            if issubclass(base, Model):
                attributes.update({k: v for k, v in base.__dict__.items() if isinstance(v, Field)})
        return attributes

    @classmethod
    def _field_name_descriptor_map(cls) -> Dict[str, Any]:
        """
        Build a mapping of the model's field names to field descriptor instances.
        Also, substitue the field key api to the model attribute custom field name.
        
        >>> class Test(Model):
        ...     first_name = TextField("First Name")
        ...     age = NumberField("Age")
        ...
        >>> Test._field_name_descriptor_map()
        >>> {
        ...     "First Name": <TextField field_name="First Name">,
        ...     "Age": <NumberField field_name="Age">,
        ... }
        """
        custom_fields_model = {
            k:v for k,v in cls._attribute_descriptor_map().items()
            if k.startswith("custom_")
        }
        return {f.field_name: f for f in cls._attribute_descriptor_map().values()}

    @classmethod
    def _field_name_to_attribute_map(cls) -> Dict[str, str]:
        """
        Build a mapping of Pipedrive field names to model attributes.

        >>> class Test(Model):
        ...     first_name = TextField("First Name")
        ...     age = NumberField("Age")
        ...
        >>> Test._field_name_to_attribute_map()
        >>> {
        ...     "First Name": "first_name",
        ...     "Age": "age"
        ... }
        """
        return {
            f.field_name: k for k, f in cls._attribute_descriptor_map().items()
        }

    @classmethod
    def _attribute_to_field_name_map(cls) -> Dict[str, str]:
        """
        Build a mapping of model attributes to Pipedrive field names.

        >>> class Test(Model):
        ...     first_name = TextField("First Name")
        ...     age = NumberField("Age")
        ...
        >>> Test._attribute_to_field_name_map()
        >>> {
        ...     "first_name": "First Name",
        ...     "age": "Age"
        ... }
        """
        return {
            k: f.field_name for k, f in cls._attribute_descriptor_map().items()
        }

    @classmethod
    def from_record(cls, **record: Dict):
        """
        Build an internal instance from the Pipedrive object.
        """
        field_name_descriptor_map = cls._field_name_descriptor_map()
        field_to_attribute        = cls._field_name_to_attribute_map()

        # Model field values
        field_values = {}

        # Select custom fields from the fetched Pipedrive record
        custom_fields = record.get("custom_fields")
        if custom_fields:
            del record["custom_fields"]

        # Get model custom fields based on attribute's names
        custom_fields_model = {
            k:v for k,v in cls._attribute_descriptor_map().items()
            if k.startswith("custom_") and k not in ["custom_fields", "custom_view_id"]
        }

        # Set defined model custom fields into model field values
        for k,v in custom_fields_model.items():
            value = custom_fields.get(v.field_name)
            # if value is not None:
            field_values[k] = v.to_internal_value(value)

        for field,value in record.items():
            # if field in field_name_descriptor_map and value is not None:
            if field in field_name_descriptor_map:
                field_values[field_to_attribute[field]] = field_name_descriptor_map[field].to_internal_value(value)

        # Since instance(**field_values) will perform validation and fail on
        # any readonly fields, instead we directly set instance._fields.
        instance_id      = record.get("id")
        instance         = cls(id=instance_id)
        instance._fields = field_values
        return instance

    def to_record(self, only_writable: bool = False) -> Dict:
        """
        This method converts internal field values into values expected by Pipedrive.
        For example, a ``datetime`` value is converted into an ISO 8601 string.

        Warning: A limitation of this method is that ``field`` keys are the 
        attributes names and not the Pipedrive field names. Some work need to
        be done in order to correctly map those fields as well as set the custom
        fields properly under the `custom_fields` key.

        Args:
            only_writable: If ``True``, the result will exclude any
                values which are associated with readonly fields.
        """
        field_name_descriptor_map = self._field_name_descriptor_map()
        map_ = {}
        for field_name, attribute_name in self._field_name_to_attribute_map().items():
            if attribute_name in self._fields:
                map_[attribute_name] = field_name_descriptor_map[field_name]
        fields = {
            field: map_[field].missing_value if value is None else map_[field].to_record_value(value)
            for field, value in self._fields.items()
            if not (map_[field].readonly and only_writable)
        }
        add_time = self._fields.get("add_time")
        created_at = utils.datetime_to_iso_str(add_time) if add_time else None
        return {
            "entity":     self._get_meta("entity_name"),
            "created_at": created_at,
            "id":         self._get_id(),
            "fields":     fields
        }

    @classmethod
    @lru_cache
    def get_api(cls, version: str = None) -> Api:
        if "PIPEDRIVE_API_TOKEN" not in os.environ:
            raise ValueError("PIPEDRIVE_API_TOKEN environment variable is not set")
        return Api(
            api_token=os.environ["PIPEDRIVE_API_TOKEN"],
            version=cls._get_meta(name="version") if version is None else version
        )

    def exists(self) -> bool:
        """
        Check if the instance exists in Pipedrive.
        """
        id = self._get_id()
        if not id:
            return False
        else:
            try:
                _ = self.get(id=id)
                return True
            except Exception as exc:
                return False

    def fetch(self) -> None:
        """
        Fetch field values from the API and resets instance field values.
        """
        id = self._get_id()
        if not id:
            raise ValueError("cannot be fetched: instance does not have an `id`")

        instance = self.get(id=id)
        self._fields = instance._fields
        self._changed.clear()
        self._fetched = True

    @classmethod
    def get(cls, id: Union[int, str] = None, params: Dict = {}) -> Self:
        if id is None:
            raise ValueError("id must be provided to fetch a single record")
        api = cls.get_api()
        entity_name = cls._get_meta("entity_name")
        uri = entity_name if id is None else f"{entity_name}/{id}"
        response: ApiResponse = api.get(uri=uri, params=params)
        if response.success:
            if isinstance(response.data, list):
                if len(response.data) > 1:
                    raise ValueError(
                        f"Expected a single record for {entity_name}/{id}, "
                        f"but got {len(response.data)} records."
                    )
            return cls.from_record(**response.data)
        else:
            raise ValueError(f"Failed to fetch record {entity_name}/{id}.")

    @classmethod
    def all(cls, uri: str = None, params: Dict = {}) -> Union[List[Self], Dict]:
        results: List[Self] = []
        uri = cls._get_meta("entity_name") if uri is None else uri
        iterator = cls.get_api().iterator(uri=uri, params=params)
        for page in iterator:
            if isinstance(page.data, list):
                if uri is None:
                    results.extend([cls.from_record(**record) for record in page.data])
                # Return data as if since payload is {id: int, field: ...}
                # where field is the field searched by field search (dynamic).
                elif uri == "itemSearch/field":
                    results.extend(page.data)
                elif uri.endswith("/changelog"):
                    results.extend([EntityUpdateDict(**record) for record in page.data])
                elif uri.endswith("/files"):
                    # Avoid circular import
                    from pypipedrive.models.files import Files
                    results.extend([Files(**record) for record in page.data])
                else:
                    results.extend([cls.from_record(**record) for record in page.data])
            elif isinstance(page.data, dict):
                items = page.data.get("items") or []

                if uri == "itemSearch":
                    related_items = page.data.get("related_items") or []
                    results.extend([
                        cls(
                            items=[ItemSearchDict(**item) for item in items],
                            related_items=[ItemSearchDict(**item) for item in related_items]
                        )
                    ])
                else:
                    logger.warning(f"Unknown search type in URI {uri} for {len(items)} items")
                    break
        return results

    def save(self, *, force: bool = False, additional_params: Dict = {}) -> SaveResult:
        """
        Create/Save the resource into Pipedrive.

        If the instance does not exist already, it will be created. Otherwise, 
        the existing record will be updated, using only the fields which have 
        been modified since it was retrieved.

        Args:
            force: If ``True``, all fields will be saved, even if they have not changed.
            additional_params: Additional parameters for saving the resource.
        """
        assert isinstance(additional_params, dict), "`additional_params` must be a dictionary"
        if self._deleted:
            raise RuntimeError(f"{self.id} was deleted")

        field_values: Dict = self.to_record(only_writable=True)["fields"]
        version = self._get_meta("version")
        entity_name = self._get_meta("entity_name")
        api = self.get_api(version=version)

        # Create the a resource in Pipedrive.
        id = self._get_id()
        if not id:
            if additional_params:
                field_values.update(additional_params)
            response : ApiResponse = api.post(uri=entity_name, json=field_values)
            self._init = True  # Bypass readonly checks during initialization
            record: Dict = response.data
            # Particular case for Goals, it returns {"goal": {...} } on creation
            if entity_name == "goals" and "goal" in record:
                record = record.get("goal", {})
            field_id = self._get_meta("field_id")
            self.id = record.get("id" if field_id is None else field_id)
            self.add_time = utils.datetime_from_iso_str(record.get("add_time", None))
            self.update_time = utils.datetime_from_iso_str(record.get("update_time", None))

            # Update instance attributes with fields returned from the API
            # that were not set in `field_values`. E.g. `is_deleted`, `done` etc.
            for field in set(record).difference(field_values):
                if record[field] is not None:
                    setattr(self, field, record[field])

            self._init = False
            self._changed.clear()
            return SaveResult(id=self.id, created=True, field_names=set(field_values))

        # Update the existing resource in Pipedrive.
        # Improvement: separate save/create and update methods
        if not force:
            if not self._changed and additional_params == {}:
                return SaveResult(id=id) # Nothing to update and not forcing

            # Only include changed fields in the update payload
            attribute_to_field_name_map = self._attribute_to_field_name_map()
            field_values = {
                attribute_to_field_name_map.get(field_name): value
                for field_name, value in field_values.items()
                if self._changed.get(attribute_to_field_name_map.get(field_name))
            }

        uri = f"{entity_name}/{id}"
        # Special case where LeadFields/LeadLabels use PATCH instead of PUT 
        # for updates even though they are V1 endpoints.
        if version == V1 and entity_name in ["leads", "leadLabels"]:
            method = api.patch
        else:
            method = api.update_method()
        if additional_params:
            field_values.update(additional_params)
        response: ApiResponse = method(uri=uri, json=field_values)

        self._changed.clear()
        return SaveResult(
            id          = id,
            updated     = True,
            forced      = force,
            field_names = set(field_values)
        )

    def delete(self) -> bool:
        """
        Marks the record as deleted. After 30 days, the record will be 
        permanently deleted.
        """
        if not self.id:
            raise ValueError("cannot be deleted because it does not have id")
        api = self.get_api(version=self._get_meta("version"))
        response: ApiResponse = api.delete(f"{self._get_meta('entity_name')}/{self.id}")
        self._deleted = response.success
        return self._deleted

    @classmethod
    def batch_delete(
        cls,
        ids: List[Union[int, str]] = [],
        models: List[Self] = [],
        version: str = None) -> ApiResponse:
        """
        Marks multiple entities as deleted. After 30 days, the entities will
        be permanently deleted. `ids` and `models` are mutually exclusive.

        Args:
            ids: A list of model IDs to delete.
            models: A list of model instances to delete.
        """
        if not ids and not models:
            raise ValueError("either `ids` or `models` must be provided")
        if ids and models:
            raise ValueError("only one of `ids` or `models` can be provided")
        
        if ids:  # Delete by ids. Make sure all ids are integers or strings.
            assert all(isinstance(id_, (int, str)) for id_ in ids), \
                "all `ids` must be integers or strings"
        else:  # Delete by models. Make sure all models are same type with ids.
            if not all(isinstance(model, cls) for model in models):
                raise TypeError(set(type(model) for model in models))
            if not all(isinstance(model.id, int) for model in models):
                raise ValueError("cannot delete an unsaved model")
            ids = [model.id for model in models]

        version = cls._get_meta("version") if version is None else version
        uri     = cls._get_meta("entity_name")
        return cls.get_api(version=version).batch_delete(uri=uri, ids=ids)
