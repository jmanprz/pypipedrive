from typing import Dict, List, Optional
from typing_extensions import Self
from urllib.parse import quote
from pypipedrive.api import V2
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


ALLOWED_ITEM_TYPES = [
    "deal",
    "person",
    "organization",
    "lead",
    "product",
    "project"
]


class ItemSearch(Model):
    """
    Ordered reference objects, pointing to either deals, persons, organizations,
    leads, products, files or mail attachments.

    See `ItemSearch API reference <https://developers.pipedrive.com/docs/api/v1/ItemSearch>`_.

    Performs a search from your choice of item types and fields.

      * GET[Cost:40] ``v1/itemSearch`` **DEPRECATED**
      * GET[Cost:20] ``v2/itemSearch``

    Performs a search from the values of a specific field.

      * GET[Cost:40] ``v1/itemSearch/field`` **DEPRECATED**
      * GET[Cost:20] ``v2/itemSearch/field``
    """

    id            = F.IntegerField("id", readonly=True)  # Used for compatibility (=None)
    items         = F.ItemsField("items")
    related_items = F.ItemsField("related_items")

    class Meta:
        entity_name = "itemSearch"
        version     = V2

    @classmethod
    def search(
        cls,
        term: str,
        item_types: List[str] = [],
        params: Dict = {}) -> Optional[List[Self]]:
        """
        Performs a search from your choice of item types and fields.

        Allowed query parameters:

            - ``item_types`` (str): A comma-separated string array. The type of 
              items to perform the search from. Defaults to all. Values: `deal`, 
              `person`, `organization`, `product`, `lead`, `file`, 
              `mail_attachment`, `project`.
            - ``fields`` (str): A comma-separated string array. The fields to 
              perform the search from. Defaults to all.
            - ``search_for_related_items`` (bool): When enabled, the response 
              will include up to 100 newest related leads and 100 newest related 
              deals for each found person and organization and up to 100 newest 
              related persons for each found organization.
            - ``exact_match`` (bool): When enabled, only full exact matches 
              against the given term are returned. It is not case sensitive.
            - ``include_fields`` (str): A comma-separated string array. 
              Supports including optional fields in the results which are not 
              provided by default. Values: `deal.cc_email`, `person.picture`, 
              `product.price`.
            - ``limit`` (int): For pagination, the limit of entries to be 
              returned. If not provided, 100 items will be returned. Please 
              note that a maximum value of 100 is allowed.
            - ``cursor`` (str): For pagination, the marker (an opaque string 
              value) representing the first item on the next page.

        Args:
            term: The search term.
            item_types: The types of items to search for (ex: 'persons', 'deals').
            params: Additional search parameters.
        Returns:
            A list of ItemSearchPersonDict or ItemSearchDealDict objects.
        """
        assert isinstance(term, str), "search `term` must be provided."
        params["term"] = quote(term)
        if item_types:
            for item_type in item_types:
                assert item_type in ALLOWED_ITEM_TYPES, \
                    f"Invalid item type `{item_type}` (allowed: {ALLOWED_ITEM_TYPES})."
            params["item_types"] = ",".join(item_types)
        uri = f"{cls._get_meta('entity_name')}"
        return super().all(uri=uri, params=params)

    @classmethod
    def search_field(
        cls,
        term: str,
        entity_type: str,
        field: str,
        params: Dict = {}) -> Optional[List[Dict]]:
        """
        Performs a search from the values of a specific field. Results can 
        either be the distinct values of the field (useful for searching 
        autocomplete field values), or the IDs of actual items (deals, leads, 
        persons, organizations or products).

        Allowed query parameters:

        - ``match`` (str): The type of match used against the term. The 
          search is case sensitive. E.g. in case of searching for a value 
          ``monkey``. With ``exact`` match, you will only find it if term is 
          ``monkey``. With ``beginning`` match, you will only find it if the 
          term matches the beginning or the whole string, e.g. ``monk`` and 
          ``monkey``. With ``middle`` match, you will find it if the term 
          matches any substring of the value, e.g. ``onk`` and ``ke``. Default: 
          ``exact``. Values: ``exact``, ``beginning``, ``middle``.
        - ``limit`` (int): For pagination, the limit of entries to be 
          returned. If not provided, 100 items will be returned. Please 
          note that a maximum value of 500 is allowed.
        - ``cursor`` (str): For pagination, the marker (an opaque string 
          value) representing the first item on the next page.

        Args:
            term: The search term.
            entity_type: The type of entity to search for (ex: 'persons', 'deals').
            field: The key of the field to search from.
            params: Additional search parameters.
        Returns:
            A list of dictionaries representing the search results.
        """
        assert isinstance(term, str), "search `term` must be provided."
        assert entity_type in ALLOWED_ITEM_TYPES, \
            f"Invalid entity type: {entity_type}. Allowed types: {ALLOWED_ITEM_TYPES}"
        assert isinstance(field, str), "`field` must be provided and not empty."
        params["term"] = quote(term)
        params["entity_type"] = entity_type
        params["field"] = field
        uri = f"{cls._get_meta('entity_name')}/field"
        return super().all(uri=uri, params=params)  # Dicts are returned

    @classmethod
    def all(cls, *args, **kwargs):
        raise NotImplementedError("ItemSearch.all() is not allowed.")

    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError("ItemSearch.get() is not allowed.")

    def save(self, *args, **kwargs):
        raise NotImplementedError("ItemSearch.save() is not allowed.")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("ItemSearch.delete() is not allowed.")

    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("ItemSearch.batch_delete() is not allowed.")