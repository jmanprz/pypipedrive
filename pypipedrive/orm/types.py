import pydantic
from typing import Any, Dict, List, Optional, Union, Type, TypeVar
from typing_extensions import TypeAlias


T = TypeVar("T")

#: An alias for ``str`` used internally for disambiguation.
#: Field names can be any valid string.
FieldName: TypeAlias = str


def assert_typed_dict(cls: Type[T], obj: Any) -> T:
    """
    Check that `obj` is a dict and conforms to the pydantic model `cls`,
    else raise TypeError or pydantic.ValidationError.

    Args:
        cls: The pydantic model class representing the expected dict type.
        obj: The object to check.
    Returns:
        An instance of `cls` constructed from `obj` if the checks pass.
    """
    if not isinstance(obj, dict):
        raise TypeError(f"expected dict, got {type(obj)}")
    instance = cls(**obj)  # type: ignore
    return instance


def assert_typed_obj(cls: Type[T], obj: Any) -> T:
    """
    Check that `obj` is an instance of `cls`, else raise TypeError.
    
    Args:
        cls: The expected class/type of `obj`.
        obj: The object to check.
    Returns:
        The object `obj` typed as `cls` if the check passes.
    """
    if not isinstance(obj, cls):
        raise TypeError(f"expected {cls.__name__}, got {type(obj)}")
    return obj


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


class PriceDict(pydantic.BaseModel):
    product_id: Optional[int]    = None
    price: Optional[float]       = None
    currency: Optional[str]      = None
    cost: Optional[float]        = None
    direct_cost: Optional[float] = None
    notes: Optional[str]         = None


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


class CustomFieldsProductDict(pydantic.BaseModel):
    """
    Represents the custom fields for a Product entity.
    """
    type:                  Optional[str] = None
    description:           Optional[str] = None
    additional_properties: Optional[Dict] = {}


class _ItemId(pydantic.BaseModel):
    id: Optional[int]


class _ItemIdName(_ItemId):
    name: Optional[str] = None


class _ItemIdNameAddress(_ItemIdName):
    address: Optional[str] = None


class _ItemSearch(pydantic.BaseModel):
    id:            Optional[Union[int, str]] = None
    type:          Optional[str] = None
    name:          Optional[str] = None
    code:          Optional[Union[str, int]] = None
    address:       Optional[str] = None
    title:         Optional[str] = None
    value:         Optional[int] = None
    currency:      Optional[str] = None
    status:        Optional[str] = None
    visible_to:    Optional[int] = None
    owner:         Optional[Union[_ItemId, int, str]] = {}
    stage:         Optional[_ItemIdName] = {}
    person:        Optional[_ItemIdName] = {}
    organization:  Optional[_ItemIdNameAddress] = {}
    custom_fields: Optional[List] = [] # of strings
    notes:         Optional[List] = [] # of strings
    is_archived:   Optional[bool] = None


class ItemSearchDict(pydantic.BaseModel):
    item:         Optional[_ItemSearch] = None
    result_score: Optional[float]       = None


class _ItemSearchDeal(pydantic.BaseModel):
    id:            Optional[Union[int, str]] = None
    type:          Optional[str] = None
    title:         Optional[str] = None
    value:         Optional[int] = None
    currency:      Optional[str] = None
    status:        Optional[str] = None
    visible_to:    Optional[int] = None
    owner:         Optional[_ItemId] = {}
    stage:         Optional[_ItemIdName] = {}
    person:        Optional[_ItemIdName] = {}
    organization:  Optional[_ItemIdNameAddress] = {}
    custom_fields: Optional[list] = [] # of strings
    notes:         Optional[list] = [] # of strings
    is_archived:   Optional[bool] = None


class ItemSearchDealDict(pydantic.BaseModel):
    item:         Optional[_ItemSearchDeal] = None
    result_score: Optional[float]           = None


class _ItemSearchPerson(pydantic.BaseModel):
    id:            Optional[Union[int, str]] = None
    type:          Optional[str] = None
    name:          Optional[str] = None
    phones:        Optional[list] = [] # of LabelValuePrimaryDict
    emails:        Optional[list] = [] # of LabelValuePrimaryDict
    visible_to:    Optional[int] = None
    owner:         Optional[_ItemId] = {}
    organization:  Optional[_ItemIdNameAddress] = {}
    custom_fields: Optional[list] = [] # of strings
    notes:         Optional[list] = [] # of strings


class ItemSearchPersonDict(pydantic.BaseModel):
    result_score: Optional[float]       = None
    item:         Optional[_ItemSearchPerson] = None


class IdLabelDict(pydantic.BaseModel):
    id:    Optional[int | str] = None
    label: Optional[str]       = None
    color: Optional[str]       = None


class SubfieldDict(pydantic.BaseModel):
    field_code: Optional[str] = None
    field_name: Optional[str] = None
    field_type: Optional[str] = None


class CodeDict(pydantic.BaseModel):
    code: Optional[str] = None


class EntityUpdateDict(pydantic.BaseModel):
    """
    Represents a single change in the changelog of an entity.
    """

    field_key:                Optional[str] = None
    old_value:                Optional[Union[str, list[Dict]]] = None
    new_value:                Optional[Union[str, list[Dict]]] = None
    actor_user_id:            Optional[int] = None
    time:                     Optional[str] = None
    change_source:            Optional[str] = None
    change_source_user_agent: Optional[str] = None
    is_bulk_update_flag:      Optional[bool] = None