from typing import Dict, List
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model, SaveResult
from pypipedrive.orm import fields as F


class DealFields(Model):
    """
    Deal fields represent the near-complete schema for a deal in the context of 
    the company of the authorized user. Each company can have a different 
    schema for their deals, with various custom fields. In the context of using 
    deal fields as a schema for defining the data fields of a deal, it must be 
    kept in mind that some types of custom fields can have additional data 
    fields which are not separate deal fields per se. Such is the case with 
    monetary, daterange and timerange fields - each of these fields will have 
    one additional data field in addition to the one presented in the context 
    of deal fields. For example, if there is a monetary field with the key 
    ``ffk9s9`` stored on the account, ``ffk9s9`` would hold the numeric value of 
    the field, and ``ffk9s9_currency`` would hold the ISO currency code that goes 
    along with the numeric value. To find out which data fields are available, 
    fetch one deal and list its keys.

    See `DealFields API reference <https://developers.pipedrive.com/docs/api/v1/DealFields>`_.

    Returns data about all deal fields.

      * GET[Cost:20] ``v1/dealFields``

    Returns data about a specific deal field.

      * GET[Cost:2] ``v1/dealFields/{id}``

    Adds a new deal field. See: `adding a new custom field <https://pipedrive.readme.io/docs/adding-a-new-custom-field>`_.

      * POST[Cost:10] ``v1/dealFields``

    Updates a deal field. See: `updating custom field value <https://pipedrive.readme.io/docs/updating-custom-field-value>`_.

      * PUT[Cost:10] ``v1/dealFields/{id}``

    Marks multiple deal fields as deleted.

      * DELETE[Cost:10] ``v1/dealFields``

    Marks a field as deleted. See: `deleting a custom field <https://pipedrive.readme.io/docs/deleting-a-custom-field>`_.

      * DELETE[Cost:6] ``v1/dealFields/{id}``
    """

    id                      = F.IntegerField("id")
    key                     = F.TextField("key")
    name                    = F.TextField("name")
    order_nr                = F.IntegerField("order_nr")
    field_type              = F.TextField("field_type")
    add_time                = F.DatetimeField("add_time")
    update_time             = F.DatetimeField("update_time")
    last_updated_by_user_id = F.IntegerField("last_updated_by_user_id")
    created_by_user_id      = F.IntegerField("created_by_user_id")
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
    options                 = F.OptionsField("options")

    class Meta:
        entity_name = "dealFields"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, id: int, params: Dict = {}) -> Self:
        """
        Returns data about a specific deal field.

        Args:
            id: The ID of the deal field to retrieve.
            params: Additional query parameters.
        Returns:
            An instance of DealFields representing the deal field.
        """
        return super().get(id=id, params=params)

    @warn_endpoint_legacy
    @classmethod
    def all(cls, params: Dict = {}) -> List[Self]:
        """
        Returns data about all deal fields.

        Allowed query parameters:

            - ``start`` (int): Pagination start. Default: 0.
            - ``limit`` (int): Items shown per page.

        Args:
            params: Query parameters for filtering and pagination.
        Returns:
            A list of DealFields instances.
        """
        return super().all(params=params)

    @warn_endpoint_legacy
    def save(self, force: bool = False) -> SaveResult:
        """
        Adds a new deal field. For more information, see the tutorial for 
        `adding a new custom field <https://pipedrive.readme.io/docs/adding-a-new-custom-field>`_.

        The values for ``DealFields.field_type`` are:

            - ``address``: Address field
            - ``date``: Date (format YYYY-MM-DD)
            - ``daterange``: Date-range field (has a start/end date values 
              YYYY-MM-DD)
            - ``double``: Numeric value
            - ``enum``: Options field with a single possible chosen option
            - ``monetary``: Monetary field (has a numeric value and a currency 
              value)
            - ``org``: Org field (contains an org ID which is stored on the 
              same account)
            - ``people``: Person field (contains a person ID which is stored 
              on the same account)
            - ``phone``: Phone field (up to 255 numbers and/or characters)
            - ``set``: Options field with a possibility of having multiple 
              chosen options
            - ``text``: Long text (up to 65k characters)
            - ``time``: Time field (format HH:MM:SS)
            - ``timerange``: Time-range field (has a start/end time values 
              HH:MM:SS)
            - ``user``: User field (contains a user ID of another Pipedrive user)
            - ``varchar``: Text (up to 255 characters)
            - ``varchar_auto``: Autocomplete text (up to 255 characters)
            - ``visible_to``: System field that keeps item's visibility setting

        To update a deal field, the allowed updatable fields are (they are
        set at the instance level):

            - ``name``: The name of the field.
            - ``options``: When field_type is either set or enum, possible options 
              must be supplied as a JSON-encoded sequential array of 
              objects. All active items must be supplied and already 
              existing items must have their ID supplied. New items only 
              require a ``label``. Example: 
              ``[{"id":123,"label":"Existing Item"},{"label":"New Item"}]``.
            - ``add_visible_flag``: Whether the field is available in 'add new' 
              modal or not (both in web and mobile app). Default: True.

        Args:
            force: Whether to force the save operation.
        Returns:
            A SaveResult object containing the result of the save operation.
        """
        return super().save(force=force)

    @warn_endpoint_legacy
    def delete(self, *args, **kwargs) -> bool:
        """
        Marks a field as deleted. For more information, see the tutorial for 
        `deleting a custom field: <https://pipedrive.readme.io/docs/deleting-a-custom-field>`_.
        """
        return super().delete(*args, **kwargs)

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Dict:
        """
        Marks multiple deal fields as deleted.
        """
        return super().batch_delete(*args, **kwargs).to_dict()