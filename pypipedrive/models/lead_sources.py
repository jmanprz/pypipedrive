from typing import Any
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class LeadSources(Model):
    """
    A lead source indicates where your lead came from. Currently, these are 
    the possible lead sources: ``Manually created``, ``Deal``, ``Web forms``, 
    ``Prospector``, ``Leadbooster``, ``Live chat``, ``Import``, 
    ``Website visitors``, ``Workflow automation``, and ``API``. Lead sources 
    are pre-defined and cannot be edited. Please note that leads sourced from 
    the Chatbot feature are assigned the value ``Leadbooster``. Please also 
    note that this list is not final and new sources may be added as needed.

    Get all lead sources.

        * GET[Cost:2] ``v1/leadSources``
    """

    id   = F.TextField("id", readonly=True)  # Used for compatibility (=None)
    name = F.TextField("name")

    class Meta:
        entity_name = "leadSources"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadSources.get() is not allowed.")

    @warn_endpoint_legacy
    def save(self, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadSources.save() is not allowed.")
    
    @warn_endpoint_legacy
    @classmethod
    def delete(self, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadSources.delete() is not allowed.")
    
    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("LeadSources.batch_delete() is not allowed.")