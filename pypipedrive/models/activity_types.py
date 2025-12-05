from typing import Dict, List
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F
from pypipedrive.utils import warn_endpoint_legacy


class ActivityTypes(Model):
    """
    Activity types represent different kinds of activities that can be stored. 
    Each activity type is presented to the user with an icon and a name. 
    Additionally, a color can be defined (not implemented in the Pipedrive app 
    as of today). Activity types are linked to activities via 
    `ActivityType.key_string = Activity.type`. The `key_string` will be generated 
    by the API based on the given name of the activity type upon creation, and 
    cannot be changed. Activity types should be presented to the user in an 
    ordered manner, using the `ActivityType.order_nr` value.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/ActivityTypes

    Returns all activity types.
    GET[Cost:20] v1/activityTypes

    Adds a new activity type.
    POST[Cost:10] v1/activityTypes

    Updates an activity type.
    PUT[Cost:10] v1/activityTypes/{id}

    Marks multiple activity types as deleted.
    DELETE[Cost:10] v1/activityTypes

    Marks an activity type as deleted.
    DELETE[Cost:6] v1/activityTypes/{id}
    """

    id                      = F.IntegerField("id")
    order_nr                = F.IntegerField("order_nr")
    name                    = F.TextField("name")
    key_string              = F.TextField("key_string")
    icon_key                = F.TextField("icon_key")
    active_flag             = F.BooleanField("active_flag")
    color                   = F.TextField("color")
    is_custom_flag          = F.BooleanField("is_custom_flag")
    add_time                = F.DatetimeField("add_time")
    update_time             = F.DatetimeField("update_time")

    class Meta:
        entity_name = "activityTypes"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError("ActivityTypes.get() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def all(cls, *args, **kwargs) -> List[Self]:
        return super().all(*args, **kwargs)

    @warn_endpoint_legacy
    def save(self, *args, **kwargs) -> "SaveResult":  # type: ignore
        return super().save(*args, **kwargs)

    @warn_endpoint_legacy
    def delete(self, *args, **kwargs) -> bool:
        return super().delete(*args, **kwargs)
    
    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Dict:
        return super().batch_delete(*args, **kwargs).to_dict()