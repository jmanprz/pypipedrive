from typing import Any
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class LeadLabels(Model):
    """
    Lead labels allow you to visually categorize your leads. There are three 
    default lead labels: hot, cold, and warm, but you can add as many new 
    custom labels as you want.

    Get all lead labels.

        * GET[Cost:10] ``v1/leadLabels``

    Add a lead label.

        * POST[Cost:10] ``v1/leadLabels``

    Update a lead label.

        * PATCH[Cost:10] ``v1/leadLabels/{id}``

    Delete a lead label.

        * DELETE[Cost:6] ``v1/leadLabels/{id}``
    """

    id          = F.TextField("id", readonly=True)
    name        = F.TextField("name")
    color       = F.TextField("color")
    add_time    = F.DatetimeField("add_time")
    update_time = F.DatetimeField("update_time")

    class Meta:
        entity_name = "leadLabels"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadLabels.get() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadLabels.batch_delete() is not allowed.")