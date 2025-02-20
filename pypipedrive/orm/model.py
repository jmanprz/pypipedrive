import json
import logging
import dataclasses
from functools import lru_cache
from dataclasses import dataclass
from pypipedrive import utils
from pypipedrive.api import Api, V1, V2
from pypipedrive.orm.fields import Field
from pypipedrive.orm.types import FieldName
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    Set,
)
from typing_extensions import Self as SelfType


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class Model:
    """
    Model class. `custom_` is a reserved keyword for Pipedrive entity custom 
    fields that map to field api key.
    """

    _deleted: bool = False
    _fetched: bool = False
    _fields:  Dict[FieldName, Any]
    _changed: Dict[FieldName, bool]

    def __init__(self, **fields):
        """
        `fields` is a dictionary of Pipedrive record field names to fields.
        """
        self._fields: Dict[str, Any] = {}
        try:
            self.id = fields.pop("id")
        except KeyError:
            pass

        _attribute_descriptor_map = self._attribute_descriptor_map()
        for key, value in fields.items():
            if key in _attribute_descriptor_map:
                setattr(self, key, value)

        # Only start tracking changes after the object is created
        self._changed ={}

    def __init_subclass__(cls, **kwargs: Any):
        cls._validate_class()
        super().__init_subclass__(**kwargs)

    def __repr__(self) -> str:
        if not self.id:
            return f"<unsaved {self.__class__.__name__}>"
        return f"<{self.__class__.__name__} id={self.id!r}>"

    @classmethod
    def _get_meta(
        cls, name: str, default: Any = None, required: bool = False, call: bool = True
    ) -> Any:
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
        # Verify required Meta attributes were set (but don't call any callables)
        assert cls._get_meta("entity_name", required=True, call=False)
        assert cls._get_meta("config", required=True, call=False)

        model_attributes = [a for a in cls.__dict__.keys() if not a.startswith("__")]
        # Skip Model method all and get used to fetch records to allow overridden
        # it at the model level.
        model_keys = [k for k in Model.__dict__.keys() if k not in ["all", "get"]]
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
    def _get_method_version(cls, method: str, version: str = None) -> str:
        """
        Get the version of the Pipedrive API that supports the given method.

        Args:
            method (str): The method to check for support.
            version (str): The version of the API to use. If ``None``, the 
                           latest version that supports the method will be used.
        """
        versions = cls.Meta.config.get(method)
        if not versions:
            raise ValueError(f"{cls.__name__} does not support {method}")
        if version is None:
            return versions[-1]
        if version not in versions:
            raise ValueError(f"{cls.__name__} does not support {method}/{version}")
        return version

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
            if k.startswith("custom_")
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
        fields properly under the `custom_fields.api_key` key.

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
            "entity": self.Meta.entity_name,
            "created_at": created_at,
            "id": self.id,
            "fields": fields
        }

    @classmethod
    @lru_cache
    def get_api(cls, version=V2) -> Api:
        return Api(version=version)

    def exists(self) -> bool:
        """
        Check if the instance exists in Pipedrive.
        """
        if not self.id:
            return False
        else:
            try:
                _ = self.get(self.id)
                return True
            except Exception as exc:
                return False

    def fetch(self) -> None:
        """
        Fetch field values from the API and resets instance field values.
        """
        if not self.id:
            raise ValueError("cannot be fetched because instance does not have an id")

        instance = self.get(id=self.id)
        self._fields = instance._fields
        self._changed.clear()
        self._fetched = True

    @classmethod
    def get(cls, id: Union[int, str] = None, params: Dict = {}, version: str = None) -> SelfType:
        version = cls._get_method_version(method="get", version=version)
        api = cls.get_api(version=version)
        print(f"Version : {version} for api {api}")
        uri = cls.Meta.entity_name if id is None else f"{cls.Meta.entity_name}/{id}"
        response = api.get(uri=uri, params=params)
        if response.ok:
            return cls.from_record(**response.json()["data"])
        else:
            raise ValueError(
                f"Failed to fetch record {cls.Meta.entity_name}/{id}. "
                f"Status code: {response.status_code}. Reason {response.reason}."
            )

    @classmethod
    def all(cls, params: Dict = {}, version: str = None) -> List[SelfType]:
        version = cls._get_method_version(method="all", version=version)
        api = cls.get_api(version=version)
        print(api.endpoint_url)
        response = api.get(uri=f"{cls.Meta.entity_name}", params=params)
        if response.ok:
            records = response.json()
            if records:
                return [cls.from_record(**record) for record in records["data"]]
            return []
        else:
            raise ValueError(
                f"Failed to fetch record {cls.Meta.entity_name}. "
                f"Status code: {response.status_code}. Reason {response.reason}."
            )

    def save(self, *, force: bool = False, version: str = None) -> "SaveResult":
        """
        Save the model to the Pipedrive API.

        If the instance does not exist already, it will be created;
        otherwise, the existing record will be updated, using only the
        fields which have been modified since it was retrieved.

        Args:
            force: If ``True``, all fields will be saved, even if they have not changed.
        """
        if self._deleted:
            raise RuntimeError(f"{self.id} was deleted")

        field_values = self.to_record(only_writable=True)["fields"]

        if not self.id: # Create the object.
            version = self._get_method_version(method="save", version=version)
            api = self.get_api(version=version)
            created = api.post(uri=self.Meta.entity_name, body=field_values)
            if created.ok:
                record = created.json()["data"]
                self.id = record["id"]
                self.add_time = utils.datetime_from_iso_str(record["add_time"])
                self.update_time = utils.datetime_from_iso_str(record["update_time"])

                # Update instance attributes with fields returned from the API
                # that were not set in `field_values`. E.g. `is_deleted`, `done` etc.
                for field in set(record).difference(field_values):
                    if record[field] is not None:
                        setattr(self, field, record[field])

                self._changed.clear()
                return SaveResult(self.id, created=True, field_names=set(field_values))

        if not force:
            if not self._changed:
                return SaveResult(self.id)

            attribute_to_field_name_map = self._attribute_to_field_name_map()
            field_values = {
                attribute_to_field_name_map.get(field_name): value
                for field_name, value in field_values.items()
                if self._changed.get(attribute_to_field_name_map.get(field_name))
            }

        version = self._get_method_version(method="update", version=version)
        api = self.get_api(version=version)
        response = api.patch(uri=f"{self.Meta.entity_name}/{self.id}", body=field_values)
        if response.ok:
            self._changed.clear()
            return SaveResult(
                self.id, forced=force, updated=True, field_names=set(field_values)
            )
        else:
            raise ValueError(
                f"Failed to save record {self.Meta.entity_name}/{self.id}. "
                f"Status code: {response.status_code}. Reason {response.reason}. "
                f"Error: {json.loads(response.text).get('error')}"
            )

    def delete(self, version: str = None) -> bool:
        """
        Marks the record as deleted. After 30 days, the record will be 
        permanently deleted.
        """
        if not self.id:
            raise ValueError("cannot be deleted because it does not have id")
        version = self._get_method_version(method="delete", version=version)
        api = self.get_api(version=version)
        response = api.delete(f"{self.Meta.entity_name}/{self.id}")
        result = response.json()
        if response.ok:
            self._deleted = result["success"]
        else:
            """
            Trying to delete an already deleted entity returns below payload.
            Which is why we only check for the error containing "already deleted".
            {
                "success": false,
                "error": "Activity is already deleted",
                "code": "ERR_BAD_REQUEST"
            }
            """
            if "already deleted" in result["error"]:
                logger.warning(f"{self.__class__.__name__.lower()}/{self.id} is already deleted")
                return True
            else:
                raise ValueError(
                    f"Unexpected behavior while deleting "
                    f"{self.__class__.__name__.lower()}/{self.id}"
                )
        return self._deleted

    @classmethod
    def batch_delete(cls, models: List[SelfType]) -> None:
        """
        Marks multiple entities as deleted. After 30 days, the entities will
        be permanently deleted.

        Args:
            models: A list of model instances to delete.
        """
        if not all(model.id for model in models):
            raise ValueError("cannot delete an unsaved model")
        if not all(isinstance(model, cls) for model in models):
            raise TypeError(set(type(model) for model in models))
        ids = ",".join([str(model.id) for model in models])
        version = cls._get_method_version(method="batch_delete", version=version)
        api = cls.get_api(version=version)
        response = api.batch_delete(uri=f"{cls.Meta.entity_name}", ids=ids)
        if response.ok:
            return True
        else:
            raise ValueError(
                f"Failed to batch delete {cls.Meta.entity_name}. "
                f"Status code: {response.status_code}. Reason {response.reason}."
            )

@dataclass(frozen=True)
class SaveResult:
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

        >>> model = YourModel()
        >>> result = model.save()
        >>> result.saved
        True
        >>> second_result = model.save()
        >>> second_result.saved
        False
    """

    id:        int
    created:   bool = False
    updated:   bool = False
    forced:    bool = False
    field_names: Set[FieldName] = dataclasses.field(default_factory=set)

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