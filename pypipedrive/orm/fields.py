import abc
import pydantic
import logging
from datetime import datetime, date, time, timedelta
from typing_extensions import Self as SelfType
from typing_extensions import TypeAlias
from typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Generic,
    Iterable,
    List,
    Optional,
    overload,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from .types import (
    assert_typed_dict,
    assert_typed_obj,
    LabelValuePrimaryDict,
    AddressDict,
    MonetaryDict,
    ParticipantDict,
    AttendeeDict,
    ItemSearchDict,
)
from pypipedrive import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

_ClassInfo: TypeAlias = Union[type, Tuple["_ClassInfo", ...]]
T          = TypeVar("T")
T_ORM      = TypeVar("T_ORM")      # type used to represent values internally
T_API      = TypeVar("T_API")      # type used to exchange values w/ Pipedrive API
T_ORM_List = TypeVar("T_ORM_List") # type used for lists of internal values
T_Missing  = TypeVar("T_Missing")  # type returned when Pipedrive has no value


class Field(Generic[T_API, T_ORM, T_Missing], metaclass=abc.ABCMeta):

    #: Types that are allowed to be passed to this field.
    valid_types: ClassVar[_ClassInfo] = ()

    #: The value to return when the field is missing
    missing_value: ClassVar[Any] = None

    # Contains a reference to the Model class (if possible)
    _model: Optional[Type["Model"]] = None

    # The name of the attribute on the Model class (if possible)
    _attribute_name: Optional[str] = None

    def __init__(
        self,
        field_name: str,
        validate_type: bool = True,
        validate: Union[
            None,
            Callable[[Any], Any],
            Iterable[Callable[[Any], Any]]
        ] = None,
        readonly: Optional[bool] = False) -> None:
        """
        Args:
            field_name: The name of the field in Pipedrive.
            validate_type: Whether to raise a TypeError if anything attempts to write
                an object of an unsupported type as a field value. If ``False``, you
                may encounter unpredictable behavior from the Pipedrive API.
            validate: A function or list of functions that will be called to validate
                the value of the field. Each function should accept a single argument
                and return a value. If a list is provided, the functions will be called
                in order, with the return value of each function passed to the next.
            readonly: If ``True``, any attempt to write a value to this field will
                raise an ``AttributeError``. Each field implements appropriate default
                values, but you may find it useful to mark fields as readonly if you
                know that the access token your code uses does not have permission
                to modify specific fields.
        """
        self.field_name = field_name
        self.validate_type = validate_type
        self.validate = validate
        
        # Each class will define its own default, but implementers can override it.
        # Overriding this to be `readonly=False` is probably always wrong, though.
        if readonly is not None:
            assert isinstance(readonly, bool)
            self.readonly = readonly

    def __set_name__(self, owner: Any, name: str) -> None:
        """
        Called when an instance of Field is created within a class.
        """
        self._model = owner
        self._attribute_name = name

    @property
    def _description(self) -> str:
        """
        Describes the field for the purpose of logging an error message.
        Handles an edge case where a field is created directly onto a class
        that already exists; in those cases, __set_name__ is not called.
        """
        if self._model and self._attribute_name:
            return f"{self._model.__name__}.{self._attribute_name}"
        return f"{self.field_name!r} field"

    def __repr__(self) -> str:
        args = [repr(self.field_name)]
        args += [f"{key}={val!r}" for (key, val) in self._repr_fields()]
        return self.__class__.__name__ + "(" + ", ".join(args) + ")"

    def _repr_fields(self) -> List[Tuple[str, Any]]:
        return [
            ("readonly", self.readonly),
            ("validate_type", self.validate_type),
        ]

    def __get__(
        self, instance: Optional["Model"], owner: Type[Any]
    ) -> Union[SelfType, T_ORM, T_Missing]:
        # allow calling Model.field to get the field object instead of a value
        if not instance:
            return self
        field_name_to_attribute_map = instance._field_name_to_attribute_map()
        try:
            value = instance._fields[field_name_to_attribute_map[self.field_name]]
        except (KeyError, AttributeError):
            return cast(T_Missing, self.missing_value)
        if value is None:
            return cast(T_Missing, self.missing_value)
        return cast(T_ORM, value)

    def __set__(self, instance: "Model", value: Optional[T_ORM]) -> None:
        # self._raise_if_readonly()
        # Validte field type
        if self.validate_type and value is not None:
            self.valid_or_raise(value)
        # Validate field value
        if self.validate is not None:
            if isinstance(self.validate, Iterable):
                for validator in self.validate:
                    value = validator(value)
            else:
                value = self.validate(value)
        instance._fields[self._attribute_name] = value
        if hasattr(instance, "_changed"):
            instance._changed[self.field_name] = True

    def valid_or_raise(self, value: Any) -> None:
        """
        Validate the type of the given value and raise TypeError if invalid.
        """
        if self.valid_types and not isinstance(value, self.valid_types):
            raise TypeError(
                f"{self.__class__.__name__} value must be {self.valid_types}; got {type(value)}"
            )

    def _raise_if_readonly(self) -> None:
        if self.readonly:
            raise AttributeError(f"{self._description} is read-only")

    def to_internal_value(self, value: Any) -> Any:
        """
        Convert a value from the API into the value's internal representation.
        """
        return value

    def to_record_value(self, value: Any) -> Any:
        """
        Calculate the value which should be persisted to the API.
        """
        return value


#: A generic Field with internal and API representations that are the same type.
_BasicField: TypeAlias = Field[T, T, None]


class TextField(Field):
    
    missing_value = None
    valid_types = str


class NumberField(Field):

    missing_value = None
    valid_types   = (int, float)


class FloatField(Field):

    missing_value = None
    valid_types = float


class IntegerField(Field):

    missing_value = None
    valid_types = int


class BooleanField(Field):

    missing_value = None
    valid_types = bool


class DatetimeField(Field[str, datetime, None]):
    """
    DateTime field. Accepts only `datetime <https://docs.python.org/3/library/datetime.html#datetime-objects>`_ values.
    """

    missing_value = None
    valid_types   = datetime

    def to_record_value(self, value: datetime) -> str:
        """
        Convert a ``datetime`` into an ISO 8601 string, e.g. "2014-09-05T12:34:56.000Z".
        """
        try:
            return utils.datetime_to_iso_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value

    def to_internal_value(self, value: str) -> datetime:
        """
        Convert an ISO 8601 string, e.g. "2014-09-05T07:00:00.000Z" into a ``datetime``.
        """
        try:
            return utils.datetime_from_iso_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value


class DateField(Field[str, date, None]):
    """
    Date field. Accepts only `date <https://docs.python.org/3/library/datetime.html#date-objects>`_ values.
    """

    missing_value = None
    valid_types   = date

    def to_record_value(self, value: date) -> str:
        """
        Convert a ``date`` into an ISO 8601 string, e.g. "2014-09-05".
        """
        try:
            return utils.date_to_iso_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value

    def to_internal_value(self, value: str) -> date:
        """
        Convert an ISO 8601 string, e.g. "2014-09-05" into a ``date``.
        """
        try:
            return utils.date_from_iso_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return None


class TimeField(Field[str, time, None]):

    missing_value = None
    valid_types   = time

    def to_record_value(self, value):
        try:
            return utils.time_to_iso_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value
    
    def to_internal_value(self, value):
        try:
            return utils.time_from_iso_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value


class DurationField(Field[int, timedelta, None]):
    """
    Duration field. Accepts only `timedelta <https://docs.python.org/3/library/datetime.html#timedelta-objects>`_ values.
    """

    missing_value = None
    valid_types   = timedelta

    def to_record_value(self, value: timedelta) -> float:
        """
        Convert a ``timedelta`` into a number of seconds.
        """
        try:
            return utils.duration_to_hh_ss_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value

    def to_internal_value(self, value: Union[int, float]) -> timedelta:
        """
        Convert a number of seconds into a ``timedelta``.
        """
        try:
            return utils.duration_from_hh_ss_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value


class _DictField(Generic[T], _BasicField[T]):
    """
    Generic field type that stores a single dict.
    should be subclassed by concrete field types (below).
    """

    missing_value = {}
    valid_types   = dict

    def valid_or_raise(self, value: Any) -> None:
        """
        Validate the type of the given value and raise TypeError if invalid.
        """
        if self.contains_type and not isinstance(value, self.contains_type):
            raise TypeError(
                f"{self.__class__.__name__} value must be {self.contains_type}; got {type(value)}"
            )

    def to_internal_value(self, value: Optional[T_ORM]) -> T_ORM:
        if value is None:
            return {}
        else:
            return assert_typed_dict(self.contains_type, value)

    def to_record_value(self, value: T_ORM) -> T_API:
        if value:
            record_value = value.model_dump()
            for field,v in record_value.items():
                if isinstance(v, datetime):
                    record_value[field] = utils.datetime_to_iso_str(v)
                elif isinstance(v, date):
                    record_value[field] = utils.date_to_iso_str(v)
            return record_value
        return {}


class AddressField(_DictField[AddressDict]):
    """
    Dict field containing address information:
        - value: the full address
        - street_number: the street number
        - route: the street name
        - sublocality: the sublocality
        - locality: the locality
        - admin_area_level_1: the state or province
        - admin_area_level_2: the city
        - country: the country
        - postal_code: the postal code
        - formatted_address: the formatted address
    """

    contains_type = AddressDict


class MonetaryField(_DictField[MonetaryDict]):
    """
    Accepts a `dict` with schema {"value": value, "currency": "UNIT"}
    """

    contains_type = MonetaryDict


class _ListField(
    Generic[T_API, T_ORM, T_ORM_List],
    Field[List[T_API], List[T_ORM], T_ORM_List]
    ):
    """
    Generic type for a field that stores a list of values.
    Not for direct use; should be subclassed by concrete field types (below).

    Generic type parameters:
        * ``T_API``: The type of value returned by the Pipedrive API.
        * ``T_ORM``: The type of value stored internally.
        * ``T_ORM_List``: The type of list object that will be returned.
    """

    missing_value = []
    valid_types   = list

    # List fields will always return a list, never ``None``, so we
    # have to overload the type annotations for __get__

    @overload
    def __get__(self, instance: None, owner: Type[Any]) -> SelfType: ...

    @overload
    def __get__(self, instance: "Model", owner: Type[Any]) -> List[T_ORM]: ...

    def __get__(
        self, instance: Optional["Model"], owner: Type[Any]
    ) -> Union[SelfType, List[T_ORM]]:
        if not instance:
            return self
        return self._get_list_value(instance)

    def _get_list_value(self, instance: "Model") -> List[T_ORM]:
        value = cast(List[T_ORM], instance._fields.get(self._attribute_name))
        # If returns no value, substitute an empty list.
        if value is None:
            value = []
            # For implementers to be able to modify this list in place
            # and persist it later when they call .save(), we need to
            # set this empty list as the field's value.
            if not self.readonly:
                instance._fields[self.field_name] = value
        return value

    def to_internal_value(self, value: Optional[List[T_ORM]]) -> List[T_ORM]:
        if value is None:
            value = []
        internal_values = []
        for obj in value:
            if isinstance(obj, dict):
                internal_values.append(assert_typed_dict(self.contains_type, obj))
            else:
                internal_values.append(assert_typed_obj(self.contains_type, obj))
        return internal_values

    def to_record_value(self, value: List[T_ORM]) -> List[T_API]:
        record_values = []
        for obj in value:
            if isinstance(obj, pydantic.BaseModel):
                record_value = obj.model_dump()
                for field,v in record_value.items():
                    if isinstance(v, datetime):
                        record_value[field] = utils.datetime_to_iso_str(v)
                    elif isinstance(v, date):
                        record_value[field] = utils.date_to_iso_str(v)
                record_values.append(record_value)
            else:
                record_values.append(obj)
        return record_values


class _ValidatingListField(Generic[T], _ListField[T, T, T]):
    contains_type: Type[T]

    def valid_or_raise(self, value: Any) -> None:
        super().valid_or_raise(value)
        for obj in value:
            if not isinstance(obj, self.contains_type):
                raise TypeError(f"expected {self.contains_type}; got {type(obj)}")


class PhonesField(_ValidatingListField[LabelValuePrimaryDict]):
    """
    Accepts a list of dicts in the format of LabelValuePrimaryDict.
    """

    contains_type = LabelValuePrimaryDict


class EmailsField(_ValidatingListField[LabelValuePrimaryDict]):
    """
    Accepts a list of dicts in the format of LabelValuePrimaryDict.
    """

    contains_type = LabelValuePrimaryDict


class ImField(_ValidatingListField[LabelValuePrimaryDict]):
    """
    Accepts a list of dicts in the format of LabelValuePrimaryDict.
    """

    contains_type = LabelValuePrimaryDict


class LabelIdsField(_ValidatingListField[int]):
    """
    Accepts a list of integers.
    """

    contains_type = int


class ParticipantField(_ValidatingListField[ParticipantDict]):
    """
    Accepts a list of dicts in the format of ParticipantDict.
    """

    contains_type = ParticipantDict


class AttendeeField(_ValidatingListField[AttendeeDict]):
    """
    Accepts a list of dicts in the format of AttendeeDict.
    """

    contains_type = AttendeeDict


class ItemSearchField(_ValidatingListField[ItemSearchDict]):
    """
    Accepts a list of dicts in the format of ItemSearch.
    """

    contains_type = ItemSearchDict