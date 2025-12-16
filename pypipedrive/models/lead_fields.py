from typing import Any
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class LeadFields(Model):
    """
    Lead fields represent the near-complete schema for a lead in the context 
    of the company of the authorized user. Each company can have a different 
    schema for their leads, with various custom fields. In the context of using 
    lead fields as a schema for defining the data fields of a lead, it must be 
    kept in mind that some types of custom fields can have additional data 
    fields which are not separate lead fields per se. Such is the case with 
    monetary, daterange and timerange fields - each of these fields will have 
    one additional data field in addition to the one presented in the context 
    of lead fields. For example, if there is a monetary field with the key 
    ``ffk9s9`` stored on the account, ``ffk9s9`` would hold the numeric value 
    of the field, and ``ffk9s9_currency`` would hold the ISO currency code 
    that goes along with the numeric value. To find out which data fields are 
    available, fetch one lead and list its keys.

    Get all lead fields.

        * GET[Cost:20] ``v1/leadFields``
    """

    id                      = F.IntegerField("id", readonly=True)
    key                     = F.TextField("key")
    name                    = F.TextField("name")
    group_id                = F.IntegerField("group_id")
    order_nr                = F.IntegerField("order_nr")
    field_type              = F.TextField("field_type")
    add_time                = F.DatetimeField("add_time")
    update_time             = F.DatetimeField("update_time")
    last_updated_by_user_id = F.IntegerField("last_updated_by_user_id")
    created_by_user_id      = F.IntegerField("created_by_user_id")
    json_column_flag        = F.BooleanField("json_column_flag")
    active_flag             = F.BooleanField("active_flag")
    edit_flag               = F.BooleanField("edit_flag")
    index_visible_flag      = F.BooleanField("index_visible_flag")
    details_visible_flag    = F.BooleanField("details_visible_flag")
    add_visible_flag        = F.BooleanField("add_visible_flag")
    important_flag          = F.BooleanField("important_flag")
    bulk_edit_allowed       = F.BooleanField("bulk_edit_allowed")
    searchable_flag         = F.BooleanField("searchable_flag")
    filtering_allowed       = F.BooleanField("filtering_allowed")
    sortable_flag           = F.BooleanField("sortable_flag")
    mandatory_flag          = F.BooleanField("mandatory_flag")
    description             = F.TextField("description")
    options                 = F.OptionsField("options")

    class Meta:
        entity_name = "leadFields"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadFields.get() is not allowed.")

    @warn_endpoint_legacy
    def save(self, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadFields.save() is not allowed.")
    
    @warn_endpoint_legacy
    @classmethod
    def delete(self, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadFields.delete() is not allowed.")
    
    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadFields.batch_delete() is not allowed.")