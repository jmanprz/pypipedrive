import pydantic
from typing import (
    Any,
    Optional,
    Type,
    TypeAlias,
    TypeVar,
)


T = TypeVar("T")

#: An alias for ``str`` used internally for disambiguation.
#: Field names can be any valid string.
FieldName: TypeAlias = str


def assert_typed_dict(cls: Type[T], obj: Any) -> T:
    """
    Raises a TypeError if the given object is not a dict, or raises
    pydantic.ValidationError if the given object does not conform
    to the interface declared by the given TypedDict.
    """
    if not isinstance(obj, dict):
        raise TypeError(f"expected dict, got {type(obj)}")
    instance = cls(**obj)  # type: ignore
    return instance


def assert_typed_obj(cls: Type[T], obj: Any) -> T:
    if not isinstance(obj, cls):
        raise TypeError(f"expected {cls.__name__}, got {type(obj)}")
    return cls(obj)


class LabelValuePrimaryDict(pydantic.BaseModel):
    label:   Optional[str]  = None
    value:   Optional[str]  = None
    primary: Optional[bool] = None


class AddressDict(pydantic.BaseModel):
    value:              Optional[str] = None
    street_number:      Optional[str] = None
    route:              Optional[str] = None
    sublocality:        Optional[str] = None
    locality:           Optional[str] = None
    admin_area_level_1: Optional[str] = None
    admin_area_level_2: Optional[str] = None
    country:            Optional[str] = None
    postal_code:        Optional[str] = None
    formatted_address:  Optional[str] = None


class MonetaryDict(pydantic.BaseModel):
    value:    Optional[float] = None
    currency: Optional[str]   = None


class ParticipantDict(pydantic.BaseModel):
    person_id: Optional[int]  = None
    primary:   Optional[bool] = None


class AttendeeDict(pydantic.BaseModel):
    email:        Optional[str]  = None
    name:         Optional[str]  = None
    status:       Optional[str]  = None
    is_organizer: Optional[bool] = None
    person_id:    Optional[int]  = None
    user_id:      Optional[int]  = None