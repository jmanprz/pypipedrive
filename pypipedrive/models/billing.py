from typing import List
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Billing(Model):
    """
    Billing is responsible for handling your subscriptions, payments, plans and 
    add-ons.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/Billing

    Returns the add-ons for a single company.
    GET[Cost:20] v1/billing/subscriptions/addons
    """

    code = F.TextField("code")  # leadbooster_v2, prospector, smart_docs_v2 ...

    class Meta:
        entity_name = "billing/subscriptions/addons"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError("Billing.get() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def all(cls, *args, **kwargs) -> List[Self]:
        return super().all(*args, **kwargs)

    @warn_endpoint_legacy
    def save(self, *args, **kwargs):
        raise NotImplementedError("Billing.save() is not allowed.")

    @warn_endpoint_legacy
    def delete(self, *args, **kwargs):
        raise NotImplementedError("Billing.delete() is not allowed.")
    
    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("Billing.batch_delete() is not allowed.")