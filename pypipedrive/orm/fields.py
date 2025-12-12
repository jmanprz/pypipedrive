import abc
import numbers
import pydantic
import logging
import datetime
from typing_extensions import Self, TypeAlias
from typing import (
    Any,
    Callable,
    Dict,
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
    PartiesDict,
    assert_typed_dict,
    assert_typed_obj,
    AddressDict,
    AssigneeDict,
    AttendeeDict,
    CodeDict,
    CustomFieldsProductDict,
    ExpectedOutcomeDict,
    GoalDurationDict,
    IdLabelDict,
    ItemSearchDict,
    ItemSearchDealDict,
    ItemSearchPersonDict,
    LabelValuePrimaryDict,
    MonetaryDict,
    ParticipantDict,
    PartiesDict,
    PriceDict,
    SeasonalityDict,
    SubfieldDict,
    TypeDict,
)
from pypipedrive import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

_ClassInfo: TypeAlias = Union[type, Tuple["_ClassInfo", ...]]
T          = TypeVar("T")
T_Model    = TypeVar("T_Model")    # type used to represent Model subclasses
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
    _model: Optional[Type[T_Model]] = None

    # The name of the attribute on the Model class (if possible)
    _attribute_name: Optional[str] = None

    def __init__(
        self,
        field_name: str,
        validate_type: bool = True,
        validate: Union[None, Callable[[Any], Any], Iterable[Callable[[Any], Any]]] = None,
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
        self,
        instance: Optional[T_Model],
        owner: Type[Any]) -> Union[Self, T_ORM, T_Missing]:
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

    def __set__(self, instance: T_Model, value: Optional[T_ORM]) -> None:
        # Ensure assignment is allowed for readonly fields. Note: callers that
        # populate instance._fields directly (e.g. Model.from_record) bypass
        # this check intentionally.
        self._raise_if_readonly(is_init=instance._init)

        # Type validation: only run if the instance attribute `validate_type` (bool) is True
        if getattr(self, "validate_type", True) and value is not None:
            # Prefer a class-level `validate_type(self, value)` method on subclasses
            # because instance attribute `self.validate_type` is a boolean and would
            # shadow a method of the same name.
            class_validator = getattr(type(self), "validate_type", None)
            if callable(class_validator):  # Call the subclass validator (bound)
                class_validator(self, value)
            else:  # Fallback to the generic valid_types check
                self.valid_or_raise(value) if self.validate_type else None
        
        # Field-specific validators (callable or iterable of callables)
        if self.validate is not None:
            if isinstance(self.validate, Iterable):
                for validator in self.validate:
                    value = validator(value)
            else:
                value = self.validate(value)
        
        # Assign the validated value to the instance's fields dictionary
        instance._fields[self._attribute_name] = self.to_internal_value(value)

        # Mark the field as changed if the model tracks changes
        if hasattr(instance, "_changed"):
            instance._changed[self.field_name] = True

    def valid_or_raise(self, value: Any) -> None:
        """
        Validate the type of the given value and raise TypeError if invalid.
        """
        if self.valid_types and not isinstance(value, self.valid_types):
            raise TypeError(
                f"{self.__class__.__name__} {self.field_name} value must be "
                f"{self.valid_types}; got {type(value)} (value: {value})."
            )

    def _raise_if_readonly(self, is_init: bool = False) -> None:
        if self.readonly and not is_init:
            raise AttributeError(
                f"{self._description} {self.__class__.__name__} "
                f"{self.field_name} is read-only (is init: {is_init})."
            )

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


class TextField(Field):
    
    missing_value = None
    valid_types = str


class BytesField(Field):
    
    missing_value = None
    valid_types = bytes


class NumberField(Field):

    missing_value = None
    valid_types   = (int, float)

    def validate_type(self, value):
        """
        Accept numeric values but reject booleans.
        """
        if value is None:
            return

        # Explicitly reject bool (bool subclasses int)
        if isinstance(value, bool):
            raise TypeError(
                f"{self.__class__.__name__} {self.field_name} expects a "
                f"boolean; got {type(value)!r} (value: {value})."
            )

        # Accept real numeric types (int, float, Decimal, etc.)
        if not isinstance(value, numbers.Real):
            raise TypeError(
                f"{self.__class__.__name__} {self.field_name} expects a "
                f"numbers.Real value; got {type(value)!r} (value: {value})."
            )


class FloatField(Field):

    missing_value = None
    valid_types = float


class IntegerField(Field):

    missing_value = None
    valid_types = int

    def validate_type(self, value):
        if value in [None, ""]:
            return

        # bool subclasses int, explicitly reject it
        if isinstance(value, bool):
            raise TypeError(
                f"{self.__class__.__name__} {self.field_name} expects a boolean "
                f"value; got {type(value)!r} (value: {value})."
            )

        # accept int-like integrals (e.g. numpy.int64)
        if not isinstance(value, numbers.Integral):
            if not(isinstance(value, str) and value.isdigit()):
                raise TypeError(
                    f"{self.__class__.__name__} {self.field_name} expects a "
                    f"numbers.Integral; got {type(value)!r} (value: {value})."
            )


class BooleanField(Field):

    missing_value = None
    valid_types = bool


class DatetimeField(Field[str, datetime.datetime, None]):
    """
    DateTime field. Accepts only `datetime <https://docs.python.org/3/library/datetime.html#datetime-objects>`_ values.
    """

    missing_value = None
    valid_types   = datetime.datetime

    def to_record_value(self, value: Optional[datetime.datetime]) -> Optional[str]:
        """
        Convert a ``datetime`` into an ISO 8601 string, e.g. "2014-09-05T12:34:56.000Z".
        """
        if value in [None, ""]:
            return self.missing_value
        try:
            return utils.datetime_to_iso_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value

    def to_internal_value(self, value: Optional[str]) -> Optional[datetime.datetime]:
        """
        Convert an ISO 8601 string, e.g. "2014-09-05T07:00:00.000Z" into a ``datetime``.
        """
        if value in [None, ""]:
            return self.missing_value
        elif isinstance(value, datetime.datetime):
            return value
        else:
            try:
                return utils.datetime_from_iso_str(value)
            except Exception as exc:
                if self.validate_type:
                    raise ValueError(
                        f"Invalid datetime string for field {self.field_name}: "
                        f"{value}"
                    ) from exc
                logger.warning(f"field {self.field_name}: {exc}")
                return self.missing_value

    def valid_or_raise(self, value: Any) -> None:
        """
        Validate the type of the given value and raise TypeError if invalid.
        """
        if self.valid_types:
            try:
                self.to_internal_value(value)
            except Exception:
                raise TypeError(
                    f"{self.__class__.__name__} {self.field_name} value must "
                    f"be {self.valid_types}; got {type(value)} which could "
                    f"not be converted (value: {value})."
                )


class DateField(Field[str, datetime.date, None]):
    """
    Date field. Accepts only `date <https://docs.python.org/3/library/datetime.html#date-objects>`_ values.
    """

    missing_value = None
    valid_types   = datetime.date

    def validate_type(self, value):
        """
        Ensure only datetime.date (but not datetime.datetime) values are accepted.
        """
        if value is None:
            return

        # Reject datetime.datetime explicitly (it's a subclass of date)
        if isinstance(value, datetime.datetime):
            raise TypeError(
                f"{self.__class__.__name__} {self.field_name} expects a datetime.date "
                "(not datetime.datetime). Use DateTimeField for timestamps; "
                f"got {type(value)!r} (value: {value})."
            )

        if not isinstance(value, datetime.date):
            raise TypeError(
                f"{self.__class__.__name__} {self.field_name} expects datetime.date; "
                f"got {type(value)!r} (value: {value})."
            )

    def to_record_value(self, value: Optional[datetime.date]) -> Optional[str]:
        """
        Convert a ``date`` into an ISO 8601 string, e.g. "2014-09-05".
        """
        if value in [None, ""]:
            return self.missing_value
        try:
            return utils.date_to_iso_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value

    def to_internal_value(self, value: Optional[str]) -> Optional[datetime.date]:
        """
        Convert an ISO 8601 string, e.g. "2014-09-05" into a ``date``.
        """
        if value in [None, ""]:
            return self.missing_value
        elif isinstance(value, datetime.date):
            return value
        else:
            try:
                return utils.date_from_iso_str(value)
            except Exception as exc:
                if self.validate_type:
                    raise ValueError(
                        f"Invalid datetime string for field {self.field_name}: "
                        f"{value}"
                    ) from exc
                logger.warning(f"field {self.field_name}: {exc}")
                return self.missing_value

    def valid_or_raise(self, value: Any) -> None:
        """
        Validate the type of the given value and raise TypeError if invalid.
        """
        if self.valid_types:
            try:
                self.to_internal_value(value)
            except Exception:
                raise TypeError(
                    f"{self.__class__.__name__} {self.field_name} value must "
                    f"be {self.valid_types}; got {type(value)} which could not "
                    f"be converted (value: {value})."
                )


class TimeField(Field[str, datetime.time, None]):

    missing_value = None
    valid_types   = datetime.time

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


class DurationField(Field[int, datetime.timedelta, None]):
    """
    Duration field. Accepts only `timedelta <https://docs.python.org/3/library/datetime.html#timedelta-objects>`_ values.
    """

    missing_value = None
    valid_types   = datetime.timedelta

    def to_record_value(self, value: datetime.timedelta) -> float:
        """
        Convert a ``datetime.timedelta`` into a number of seconds.
        """
        try:
            return utils.duration_to_hh_ss_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value

    def to_internal_value(self, value: Union[int, float]) -> datetime.timedelta:
        """
        Convert a number of seconds into a ``datetime.timedelta``.
        """
        try:
            return utils.duration_from_hh_ss_str(value)
        except Exception as exc:
            logger.warning(f"field {self.field_name}: {exc}")
            return self.missing_value

# === Dict fields ===

class _DictField(Generic[T], Field[Dict, Dict, Dict]):
    """
    Generic field type that stores a single dict. Should be subclassed by 
    concrete field types.
    """

    missing_value = {}
    valid_types   = dict
    contains_type: Type[T] = dict

    def valid_or_raise(self, value: Any) -> None:
        """
        Validate the type of the given value and raise TypeError if invalid.
        """
        if self.contains_type is None:
            raise TypeError(
                f"{self.__class__.__name__}.contains_type {self.field_name} "
                f"must be set (value: {value})."
            )
        elif isinstance(value, dict):
            assert_typed_dict(self.contains_type, value)
        elif not isinstance(value, self.contains_type):
            raise TypeError(
                f"{self.__class__.__name__} {self.field_name} value must "
                f"be {self.contains_type}; got {type(value)} (value: {value})."
            )

    def to_internal_value(self, value: Optional[T_ORM]) -> T_ORM:
        if value is None:
            return {}
        else:
            if isinstance(value, dict):
                return assert_typed_dict(self.contains_type, value)
            return value

    def to_record_value(self, value: T_ORM) -> T_API:
        if value:
            record_value = value.model_dump()
            for field,v in record_value.items():
                if isinstance(v, datetime.datetime):
                    record_value[field] = utils.datetime_to_iso_str(v)
                elif isinstance(v, datetime.date):
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


class CustomFieldsProductField(_DictField[CustomFieldsProductDict]):
    """
    Accepts a `dict` with schema `CustomFieldsProductDict`.
    """

    contains_type = CustomFieldsProductDict


class AssigneeField(_DictField[AssigneeDict]):
    """
    Accepts a `dict` with schema `AssigneeDict` (Goal).
    """

    contains_type = AssigneeDict


class TypeField(_DictField[TypeDict]):
    """
    Accepts a `dict` with schema `TypeDict` (Goal).
    """

    contains_type = TypeDict


class GoalDurationField(_DictField[GoalDurationDict]):
    """
    Accepts a `dict` with schema `GoalDurationDict` (Goal).
    """

    contains_type = GoalDurationDict


class SeasonalityField(_DictField[SeasonalityDict]):
    """
    Accepts a `dict` with schema `SeasonalityDict` (Goal).
    """

    contains_type = SeasonalityDict


class ExpectedOutcomeField(_DictField[ExpectedOutcomeDict]):
    """
    Accepts a `dict` with schema `ExpectedOutcomeDict` (Goal).
    """

    contains_type = ExpectedOutcomeDict


class PartiesField(_DictField[PartiesDict]):
    """
    Accepts a `dict` with schema `PartiesDict` (Mailbox/MailThreads to, from, 
    bcc and cc).
    """

    contains_type = PartiesDict


# === List fields ===

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
    def __get__(self, instance: None, owner: Type[Any]) -> Self: ...

    @overload
    def __get__(self, instance: T_Model, owner: Type[Any]) -> List[T_ORM]: ...

    def __get__(
        self, instance: Optional[T_Model], owner: Type[Any]
    ) -> Union[Self, List[T_ORM]]:
        if not instance:
            return self
        return self._get_list_value(instance)

    def _get_list_value(self, instance: T_Model) -> List[T_ORM]:
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
        if not isinstance(value, list):
            raise TypeError(
                f"{self.__class__.__name__} {self.field_name} expected list; "
                f"got {type(value)} (value: {value})."
            )
        for obj in value:
            if isinstance(obj, dict):
                internal_values.append(assert_typed_dict(self.contains_type, obj))
            elif isinstance(obj, self.contains_type):
                internal_values.append(assert_typed_obj(self.contains_type, obj))
            else:
                raise TypeError(
                    f"{self.__class__.__name__} {self.field_name} expected "
                    f"{self.contains_type} or dict; got {type(obj)} (value: {obj})."
                )
        return internal_values

    def to_record_value(self, value: List[T_ORM]) -> List[T_API]:
        record_values = []
        for obj in value:
            if isinstance(obj, pydantic.BaseModel):
                record_value = obj.model_dump()
                for field,v in record_value.items():
                    if isinstance(v, datetime.datetime):
                        record_value[field] = utils.datetime_to_iso_str(v)
                    elif isinstance(v, datetime.date):
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
            if isinstance(obj, dict):
                assert_typed_dict(self.contains_type, obj)
            elif not isinstance(obj, self.contains_type):
                raise TypeError(
                    f"{self.__class__.__name__} {self.field_name} expected "
                    f"{self.contains_type}; got {type(obj)} (value: {obj})."
                )


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


class LabelIdsField(_ValidatingListField[Union[int, str]]):
    """
    Accepts a list of integers or strings.
    """

    contains_type = Union[int, str]


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


class ItemsField(_ValidatingListField[ItemSearchDict]):
    """
    Accepts a list of dicts in the format of ItemSearchDict (Model.ItemSearch).
    """

    contains_type = ItemSearchDict


class ItemSearchDealField(_ValidatingListField[ItemSearchDealDict]):
    """
    Accepts a list of dicts in the format of ItemSearchDealDict.
    """

    contains_type = ItemSearchDealDict


class ItemSearchPersonField(_ValidatingListField[ItemSearchPersonDict]):
    """
    Accepts a list of dicts in the format of ItemSearchPersonDict.
    """

    contains_type = ItemSearchPersonDict


class OptionsField(_ValidatingListField[IdLabelDict]):
    """
    Accepts a list of dicts in the format of IdLabelDict.
    """

    contains_type = IdLabelDict


class SubfieldField(_ValidatingListField[SubfieldDict]):
    """
    Accepts a list of dicts in the format of SubfieldDict.
    """

    contains_type = SubfieldDict


class DataField(_ValidatingListField[CodeDict]):
    """
    Accepts a list of dicts in the format of CodeDict.
    """

    contains_type = CodeDict


class PricesField(_ValidatingListField[PriceDict]):
    """
    Accepts a list of dicts in the format of PriceDict.
    """

    contains_type = PriceDict


class CustomFieldsField(_ValidatingListField[str]):
    """
    Accepts a list of dicts in the format of CodeDict.
    """

    contains_type = str
