from typing import List
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Currencies(Model):
    """
    Supported currencies which can be used to represent the monetary value of 
    a deal, or a value of any monetary type custom field. The ``Currency.code``
    field must be used to point to a currency. ``Currency.code`` is the ISO-4217 
    format currency code for non-custom currencies. You can differentiate 
    custom and non-custom currencies using the ``is_custom_flag`` property. For 
    custom currencies, it is intended that the formatted sums are displayed 
    in the UI using the following format: 
    [sum][non-breaking space character][currency.symbol], 
    for example: 500 users. Custom currencies cannot be added or removed via 
    the API yet — rather the admin users of the account must configure them 
    from the Pipedrive app.

    See `Currencies API reference <https://developers.pipedrive.com/docs/api/v1/Currencies>`_.
    
    Returns all supported currencies in given account.

      * GET[Cost:20] ``v1/currencies``
    """

    id             = F.IntegerField("id")
    code           = F.TextField("code")
    name           = F.TextField("name")
    decimal_points = F.IntegerField("decimal_points")
    symbol         = F.TextField("symbol")
    active_flag    = F.BooleanField("active_flag")
    is_custom_flag = F.BooleanField("is_custom_flag")

    class Meta:
        entity_name = "currencies"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError("Currencies.get() is not allowed")

    @warn_endpoint_legacy
    @classmethod
    def all(cls, term: str = None) -> List[Self]:
        """
        Returns all supported currencies in given account which should be used 
        when saving monetary values with other objects. The `code` parameter of 
        the returning objects is the currency code according to ISO 4217 for 
        all non-custom currencies.

        Args:
            term: Optional search term that is searched for from currency's 
            name and/or code
        Returns:
            List of Currency objects
        """
        params = {"term": str(term)} if term not in [None, ""] else None
        return super().all(params=params)

    @warn_endpoint_legacy
    def save(self, *args, **kwargs):
        raise NotImplementedError("Currencies.save() is not allowed.")

    @warn_endpoint_legacy
    def delete(self, *args, **kwargs):
        raise NotImplementedError("Currencies.delete() is not allowed.")
    
    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("Currencies.batch_delete() is not allowed.")