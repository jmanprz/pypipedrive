from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class ItemSearch(Model):
    """
    Ordered reference objects, pointing to either deals, persons, organizations,
    leads, products, files or mail attachments.
    
    https://developers.pipedrive.com/docs/api/v1/ItemSearch

    Cost: 20.
    """
    items         = F.ItemSearchField("items")

    class Meta:
        id_name     = "id"
        entity_name = "itemSearch"

    @classmethod
    def all(cls, *args, **kwargs) -> None:
        raise NotImplementedError("ItemSearch.all() is not allowed. Use ItemSearch.get().")