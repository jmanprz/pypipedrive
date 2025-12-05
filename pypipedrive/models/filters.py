from typing import Dict
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Filters(Model):
    """
    Each filter is essentially a set of data validation conditions. A filter 
    of the same kind can be applied when fetching a list of deals, leads, 
    persons, organizations or products in the context of a pipeline. Filters 
    are limited to a maximum of 16 conditions. When applied, only items matching 
    the conditions of the filter are returned. Detailed definitions of filter 
    conditions and additional functionality is not yet available.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/Filters

    Get all filters.
    GET[Cost:20] v1/filters

    Get all filter helpers.
    GET[Cost:20] v1/filters/helpers

    Get one filter.
    GET[Cost:2] v1/filters/{id}

    Add a new filter.
    POST[Cost:10] v1/filters

    Update filter.
    PUT[Cost:10] v1/filters/{id}   

    Delete multiple filters in bulk
    DELETE[Cost:10] v1/filters

    Delete a filter
    DELETE[Cost:6] v1/productFields/{id}
    """

    id             = F.IntegerField("id", readonly=True)
    name           = F.TextField("name")
    active_flag    = F.BooleanField("active_flag")
    type           = F.TextField("type")
    temporary_flag = F.BooleanField("temporary_flag")
    user_id        = F.IntegerField("user_id")
    add_time       = F.DatetimeField("add_time")
    update_time    = F.DatetimeField("update_time")
    visible_to     = F.BooleanField("visible_to")
    custom_view_id = F.IntegerField("custom_view_id")

    class Meta:
        entity_name = "filters"
        version     = V1
    
    @warn_endpoint_legacy
    @classmethod
    def helpers(cls) -> Dict:
        """
        Returns all supported filter helpers. It helps to know what conditions 
        and helpers are available when you want to add or update filters. For 
        more information, see the tutorial for adding a filter:
        https://pipedrive.readme.io/docs/adding-a-filter

        Returns:
            A dictionary containing filter helpers (operators,
            deprecated_operators, relative_dates, address_field_components).
        """
        uri = f"{cls._get_meta('entity_name')}/helpers"
        return cls.get_api(version=V1).get(uri).to_dict()