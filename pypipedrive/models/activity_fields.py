from typing import List
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class ActivityFields(Model):
    """
    Activity fields represent different fields that an activity has.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/ActivityFields

    Returns all activity fields.
    GET[Cost:20] v1/activityFields
    """

    id                      = F.IntegerField("id")
    key                     = F.TextField("key")
    name                    = F.TextField("name")
    group_id                = F.IntegerField("group_id")
    order_nr                = F.IntegerField("order_nr")
    field_type              = F.TextField("field_type")
    json_column_flag        = F.BooleanField("json_column_flag")
    add_time                = F.DatetimeField("add_time")
    update_time             = F.DatetimeField("update_time")
    last_updated_by_user_id = F.IntegerField("last_updated_by_user_id")
    created_by_user_id      = F.IntegerField("created_by_user_id")
    active_flag             = F.BooleanField("active_flag")
    edit_flag               = F.BooleanField("edit_flag")
    details_visible_flag    = F.BooleanField("details_visible_flag")
    add_visible_flag        = F.BooleanField("add_visible_flag")
    important_flag          = F.BooleanField("important_flag")
    bulk_edit_allowed       = F.BooleanField("bulk_edit_allowed")
    searchable_flag         = F.BooleanField("searchable_flag")
    filtering_allowed       = F.BooleanField("filtering_allowed")
    sortable_flag           = F.BooleanField("sortable_flag")
    mandatory_flag          = F.BooleanField("mandatory_flag")
    options                 = F.OptionsField("options")
    restriction_settings    = F.TextField("restriction_settings")
    user_restrictions       = F.TextField("user_restrictions")
    description             = F.TextField("description")

    class Meta:
        entity_name = "activityFields"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError("ActivityFields.get() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def all(cls, *args, **kwargs) -> List[Self]:
        return super().all(*args, **kwargs)
    
    @warn_endpoint_legacy
    def save(self, *args, **kwargs):
        raise NotImplementedError("ActivityFields.save() is not allowed.")

    @warn_endpoint_legacy
    def delete(self, *args, **kwargs):
        raise NotImplementedError("ActivityFields.delete() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("ActivityFields.batch_delete() is not allowed.")