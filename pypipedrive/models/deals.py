from datetime import date
from typing import Any, Dict, List, Self, Union

from pypipedrive.api import V1, V2
from pypipedrive.api.api import ApiResponse
from pypipedrive.utils import warn_endpoint_legacy, warn_endpoint_beta
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F
from .deal_fields import DealFields
from .item_search import ItemSearch
from .files import Files
from .products import Products


class Deals(Model):
    """
    Deals represent ongoing, lost or won sales to an organization or to a 
    person. Each deal has a monetary value and must be placed in a stage. 
    Deals can be owned by a user, and followed by one or many users. Each deal 
    consists of standard data fields but can also contain a number of custom 
    fields. The custom fields can be recognized by long hashes as keys. These 
    hashes can be mapped against `DealField.key`. The corresponding label for 
    each such custom field can be obtained from `DealField.name`.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/Deals

    Returns data about all not archived deals.
    GET[Cost:20] v1/deals DEPRECATED
    GET[Cost:20] v2/deals

    Returns data about all archived deals.
    GET[Cost:40] v1/deals/archived DEPRECATED
    GET[Cost:20] v2/deals/archived

    Returns all deals collection.
    GET[Cost:10] v1/deals DEPRECATED

    Searches all deals by title, notes and/or custom fields.
    GET[Cost:40] v1/deals/search DEPRECATED
    GET[Cost:20] v2/deals/search

    Returns a summary of all not archived deals.
    GET[Cost:40] v1/deals/summary

    Returns a summary of all not archived deals.
    GET[Cost:80] v1/deals/summary/archived DEPRECATED

    Get deals timeline
    GET[Cost:20] v1/deals/timeline

    Get archived deals timeline
    GET[Cost:20] v1/deals/timeline/archived DEPRECATED

    Returns the details of a specific deal.
    GET[Cost:2] v1/deals/{id} DEPRECATED
    GET[Cost:1] v2/deals/{id}

    List activities associated with a deal.
    GET[Cost:20] v1/deals/{id}/activities DEPRECATED

    Lists updates about field values of an deal.
    GET[Cost:20] v1/deals/{id}/changelog

    Lists files associated with a deal.
    GET[Cost:20] v1/deals/{id}/files

    List updates about a deal.
    GET[Cost:40] v1/deals/{id}/flow

    List updates about participants of a deal.
    GET[Cost:10] v1/deals/{id}/participantsChangelog

    List followers of a deal.
    GET[Cost:20] v1/deals/{id}/followers DEPRECATED
    GET[Cost:10] v2/deals/{id}/followers

    List mail messages associated with a deal.
    GET[Cost:20] v1/deals/{id}/mailMessages

    List participants of a deal.
    GET[Cost:10] v1/deals/{id}/participants

    List permitted users.
    GET[Cost:10] v1/deals/{id}/permittedUsers

    List all persons associated with a deal.
    GET[Cost:20] v1/deals/{id}/persons DEPRECATED

    List products attached to a deal.
    GET[Cost:20] v1/deals/{id}/products DEPRECATED
    GET[Cost:10] v2/deals/{id}/products

    List followers changelog of a deal.
    GET[Cost:10] v2/deals/{id}/followers/changelog

    Get deal products of several deals.
    GET[Cost:20] v2/deals/products

    List discounts added to a deal.
    GET[Cost:10] v2/deals/{id}/discounts

    List installments added to a list of deals (BETA).
    GET[Cost:10] v2/deals/installments

    Get Deal conversion status (BETA)
    GET[Cost:10] v2/deals/{id}/convert/status/{conversion_id}

    Add a deal.
    POST[Cost:10] v1/deals DEPRECATED
    POST[Cost:5] v2/deals

    Duplicate deal.
    POST[Cost:10] v1/deals/{id}/duplicate

    Add a follower to a deal.
    POST[Cost:10] v1/deals/{id}/followers DEPRECATED
    POST[Cost:5]  v2/deals/{id}/followers

    Add a participant to a deal.
    POST[Cost:5] v1/deals/{id}/participants

    Add a product to a deal.
    POST[Cost:10] v1/deals/{id}/products
    POST[Cost:5]  v2/deals/{id}/products

    Add multiple products to a deal.
    POST[Cost:25] v2/deals/{id}/products/bulk

    Add a discount to a deal.
    POST[Cost:5] v2/deals/{id}/discounts

    Add an installment to a deal.
    POST[Cost:5] v2/deals/{id}/installments

    Convert a deal to a lead (BETA).
    GET[Cost:40] v2/deals/{id}/convert/lead

    Update a deal.
    PUT[Cost:10]  v1/deals/{id} DEPRECATED
    PATCH[Cost:5] v2/deals/{id}

    Merge two deals.
    PUT[Cost:40] v1/deals/{id}/merge (merge_with_id in body)

    Update the product attached to a deal.
    PUT[Cost:10]  v1/deals/{id}/products/{product_attachment_id} DEPRECATED
    PATCH[Cost:5] v2/deals/{id}/products/{product_attachment_id}

    Update a discount added to a deal.
    PATCH[Cost:5] v2/deals/{id}/discounts/{discount_id}

    Update an installment added to a deal.
    PATCH[Cost:5] v2/deals/{id}/installments/{installment_id}

    Delete multiple deals in bulk
    DELETE[Cost:10] v1/deals DEPRECATED

    Delete a deal.
    DELETE[Cost:6] v1/deals/{id} DEPRECATED
    DELETE[Cost:3] v2/deals/{id}

    Delete a follower from a deal.
    DELETE[Cost:6] v1/deals/{id}/followers/{follower_id} DEPRECATED
    DELETE[Cost:3] v2/deals/{id}/followers/{follower_id}

    Delete a participant from a deal.
    DELETE[Cost:3] v1/deals/{id}/participants/{participant_id}

    Delete many products from a deal.
    DELETE[Cost:25] v2/deals/{id}/products

    Delete an attached product from a deal
    DELETE[Cost:5] v1/deals/{id}/products/{product_attachment_id}
    DELETE[Cost:3] v2/deals/{id}/products/{product_attachment_id}

    Delete a discount from a deal
    DELETE[Cost:3] v2/deals/{id}/discounts/{discount_id}

    Delete an installment from a deal
    DELETE[Cost:3] v2/deals/{id}/installments/{installment_id}
    """

    id                  = F.IntegerField("id", readonly=True)
    title               = F.TextField("title")
    creator_user_id     = F.IntegerField("creator_user_id", readonly=True)
    user_id             = F.IntegerField("user_id", readonly=True)
    org_id              = F.IntegerField("org_id")
    person_id           = F.IntegerField("person_id")
    stage_id            = F.IntegerField("stage_id")
    pipeline_id         = F.IntegerField("pipeline_id")
    owner_id            = F.IntegerField("owner_id")
    value               = F.NumberField("value") # In field currency
    currency            = F.TextField("currency") # Of field value
    add_time            = F.DatetimeField("add_time", readonly=True)
    update_time         = F.DatetimeField("update_time", readonly=True)
    status              = F.TextField("status")
    probability         = F.IntegerField("probability")
    lost_reason         = F.TextField("lost_reason")
    visible_to          = F.IntegerField("visible_to")
    close_time          = F.DatetimeField("close_time")
    won_time            = F.DatetimeField("won_time")
    lost_time           = F.DatetimeField("lost_time")
    stage_change_time   = F.DatetimeField("stage_change_time")
    local_won_date      = F.DateField("local_won_date")
    local_lost_date     = F.DateField("local_lost_date")
    local_close_date    = F.DateField("local_close_date")
    expected_close_date = F.DateField("expected_close_date")
    label_ids           = F.LabelIdsField("label_ids")
    is_deleted          = F.BooleanField("is_deleted", readonly=True)
    origin              = F.TextField("origin")
    origin_id           = F.TextField("origin_id")
    channel             = F.TextField("channel")
    channel_id          = F.IntegerField("channel_id")
    is_archived         = F.BooleanField("is_archived")
    archive_time        = F.DatetimeField("archive_time")
    acv                 = F.FloatField("acv")
    arr                 = F.FloatField("arr")
    mrr                 = F.FloatField("mrr")
    custom_fields       = F.CustomFieldsField("custom_fields")

    class Meta:
        entity_name = "deals"
        version     = V2

    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("Deals.batch_delete() not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def fields(cls) -> List[DealFields]:
        """
        V1 endpoint that returns the list of field names for the Deals model.
        """
        return DealFields.all()

    @classmethod
    def archived(cls, params: Dict = {}) -> List[Self]:
        """
        Returns data about all archived deals.

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of archived Deal instances.
        """
        uri = f"{cls._get_meta('entity_name')}/archived"
        return cls.all(uri=uri, params=params)

    @classmethod
    def search(cls, term: str = None, params: Dict = {}) -> List[ItemSearch]:
        """
        Searches all deals by title, notes and/or custom fields. This endpoint
        is a wrapper of /v2/itemSearch with a narrower OAuth scope. Found deals
        can be filtered by the person ID and the organization ID.

        Args:
            term: The search term to look for. Minimum 2 characters
                  (or 1 if using exact_match). Please note that the search 
                  term has to be URL encoded.
            params: Query params passed to the API (copied internally).
        Returns:
            List of ItemSearch objects.
        """
        return ItemSearch.search(term=term, item_types=["deal"], params=params)

    @warn_endpoint_legacy
    @classmethod
    def summary(cls, params: Dict = {}) -> Dict:
        """
        V1 endpoint. Returns a summary of all not archived deals.
        Allowed query params:
            - status (str): Filter by deal status. Possible values: "open", "won", "lost".
            - currency (str): Filter by currency code (e.g. "USD", "EUR").
            - filter_id (int): Filter by predefined filter ID.
            - user_id (int): Filter by owner user ID.
            - pipeline_id (int): Filter by pipeline ID.
            - stage_id (int): Filter by stage ID.
        """
        uri = f"{cls._get_meta('entity_name')}/summary"
        return cls.get_api(version=V1).get(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    @classmethod
    def timeline(
        cls,
        start_date: date,
        interval: str,
        amount: int,
        field_key: str,
        params: Dict = {}) -> Dict:
        """
        V1 endpoint. Returns not archived open and won deals, grouped by a 
        defined interval of time set in a date-type dealField (`field_key`) 
        — e.g. when month is the chosen interval, and 3 months are asked 
        starting from January 1st, 2012, deals are returned grouped into 
        3 groups — January, February and March — based on the value of the 
        given `field_key`.

        NB: Api also returns custom fields (uuid). Returning as dict for now
        because of the complexity of the data structure.

        Args:
            start_date: The start date for the timeline (YYYY-MM-DD).
            interval: The interval for grouping. Possible values:
                      "day", "week", "month", "quarter".
            amount: The number of intervals to return.
            field_key: The deal field key to group by (must be date-type).
            params: Query params passed to the API (copied internally).
        Returns:
            List of Deal instances.
        """
        assert isinstance(start_date, date), "`start_date` must be a date object"
        assert interval and interval in ["day", "week", "month", "quarter"], \
            "`interval` must be one of: day, week, month, quarter"
        assert isinstance(amount, int) and amount > 0, \
            "`amount` must be a positive integer"
        assert field_key and isinstance(field_key, str), \
            "`field_key` must be a non-empty string"

        params.update({
            "start_date": start_date.strftime("%Y-%m-%d"),
            "interval":   interval,
            "amount":     amount,
            "field_key":  field_key,
        })
        uri = f"{cls._get_meta('entity_name')}/timeline"
        return cls.get_api(version=V1).get(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def changelog(self, params: Dict = {}) -> List[Dict]:
        """
        V1 endpoint. Lists updates about field values of an deal. This is a 
        cursor-paginated endpoint. For more information, please refer to our 
        documentation on pagination. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            Dictionary containing changelog data.
        """
        uri = f"{self._get_meta("entity_name")}/{self.id}/changelog"
        params={k:v for k,v in params.items() if k in ["cursor", "limit"]}
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def files(self, params: Dict = {}) -> List[Files]:
        """
        V1 endpoint. Lists files associated with a deal. Allowed query params:
            - start (int): Pagination start. Default: 0.
            - limit (int): Amount of results to return. Max: 100.
            - sort (str): Sort order. Possible values: "id", "update_time".
        
        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of files data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/files"
        response: ApiResponse = self.get_api(version=V1).all(uri=uri, params=params)
        return [Files(**f) for f in response.data]

    @warn_endpoint_legacy
    def flow(self, params: Dict = {}) -> Dict:
        """
        V1 endpoint. Lists updates about a deal. Allowed query params:
            - start (int): Pagination start. Default: 0.
            - limit (int): Amount of results to return. Default: 100. Max:
            - all_changes (str): Whether to show custom field updates or not. 
                                 1 = Include custom field changes. If omitted 
                                 returns changes without custom field updates.
            -items (str): A comma-separated string for filtering out item 
                          specific updates. Possible values: call, activity, 
                          plannedActivity, change, note, deal, file, dealChange, 
                          personChange, organizationChange, follower, dealFollower, 
                          personFollower, organizationFollower, participant, 
                          comment, mailMessage, mailMessageWithAttachment, 
                          invoice, document, marketing_campaign_stat, 
                          marketing_status_change.

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            Dictionary containing flow data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/flow"
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def participants_changelog(self, params: Dict = {}) -> Dict:
        """
        V1 endpoint. List updates about participants of a deal. This is a 
        cursor-paginated endpoint. For more information, please refer to our 
        documentation on pagination. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            Dictionary containing participants changelog data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/participantsChangelog"
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    def followers(self, params: Dict = {}) -> List[Dict]:
        """
        List followers of a deal. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of followers data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers"
        return self.get_api(version=V2).all(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def mail_messages(self, params: Dict = {}) -> List[Dict]:
        """
        V1 endpoint. List mail messages associated with a deal. Allowed query params:
            - start (int): Pagination start. Default: 0.
            - limit (int): Items shown per page.

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of mail messages data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/mailMessages"
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def participants(self, params: Dict = {}) -> List[Dict]:
        """
        V1 endpoint. Lists the participants associated with a deal. If a company 
        uses the Campaigns product, then this endpoint will also return the 
        `data.marketing_status` field. Allowed query params:
            - start (int): Pagination start. Default: 0.
            - limit (int): Items shown per page.

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of participants data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/participants"
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def permitted_users(self) -> List[Dict]:
        """
        V1 endpoint. Lists the users permitted to access a deal.

        Returns:
            List of permitted users data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/permittedUsers"
        return self.get_api(version=V1).get(uri=uri).to_dict()

    def products(self, params: Dict = {}) -> List[Products]:
        """
        List products attached to a deal. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page.
            - sort_by (str): Field to sort by. Default "id".
                             Values: "id", "add_time", "update_time", "order_nr".
            - sort_direction (str): Sort direction. Default "asc".

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of products data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/products"
        results: ApiResponse = self.get_api(version=V2).all(uri=uri, params=params)
        return [Products(**p) for p in results.data]

    def followers_changelog(self, params: Dict = {}) -> Dict:
        """
        Lists changelogs about users have followed the deal. Allowed query params:
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            Dictionary containing changelog data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers/changelog"
        return self.get_api(version=V2).all(uri=uri, params=params).to_dict()

    @classmethod
    def deals_products(
        cls,
        deal_ids: List[int] = None,
        params: Dict = {}) -> List[Products]:
        """
        Returns data about products attached to deals. Allowed query params:
            - deal_ids (array): An array of integers with the IDs of the deals 
                                for which the attached products will be returned. 
                                A maximum of 100 deal IDs can be provided.
            - cursor (str): For pagination, the marker (an opaque string value)
                            representing the first item on the next page.
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - sort_by (str): The field to sort by. Supported fields: "id" (default), 
                             "deal_id", "add_time", "update_time", "order_nr".
            - sort_direction (str): The sort direction. Possible values: "asc" 
                                    (default), "desc".

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of deal products data.
        """
        if deal_ids not in [None, []]:
            assert isinstance(deal_ids, list), "`deal_ids` must be a list of integers."
            assert all(isinstance(x, int) for x in deal_ids), "`deal_ids` must be a list of integers."
            params.update({"deal_ids": ",".join(map(str, deal_ids))})
        else:
            raise ValueError("`deal_ids` must be provided and not empty.")
        uri = f"{cls._get_meta('entity_name')}/products"
        results: ApiResponse = cls.get_api(version=V2).all(uri=uri, params=params)
        return [Products(**p) for p in results.data]

    def discounts(self) -> Dict:
        """
        Lists discounts attached to a deal.

        Returns:
            Dictionary containing discounts data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/discounts"
        return self.get_api(version=V2).get(uri=uri).to_dict()

    @warn_endpoint_beta
    @classmethod
    def installments(cls, deal_ids: List[int] = None, params: Dict = {}) -> Dict:
        """
        [BETA] Lists installments attached to a deal. Only available in Growth 
        and above plans. Allowed query params:
            - deal_ids (array): An array of integers with the IDs of the deals 
                                for which the attached products will be returned. 
                                A maximum of 100 deal IDs can be provided.
            - cursor (str): For pagination, the marker (an opaque string value)
                            representing the first item on the next page.
            - limit (int): Amount of results to return. Default: 100. Max: 500.
            - sort_by (str): The field to sort by. Supported fields: "id" (default), 
                             "billing_date", "deal_id".
            - sort_direction (str): The sort direction. Possible values: "asc" 
                                    (default), "desc".

        Args:
            deal_ids: List of deal IDs to filter installments.
            params: Query params passed to the API (copied internally).
        Returns:
            List of installments data.
        """
        if deal_ids is not None:
            assert isinstance(deal_ids, list), "`deal_ids` must be a list of integers."
            assert all(isinstance(x, int) for x in deal_ids), "`deal_ids` must be a list of integers."
            params.update({"deal_ids": deal_ids})
        else:
            raise ValueError("`deal_ids` must be provided.")
        uri = f"{cls._get_meta('entity_name')}/installments"
        return cls.get_api(version=V2).all(uri=uri, params=params).to_dict()

    @warn_endpoint_beta
    def conversion_status(self, conversion_id: int) -> Dict:
        """
        [BETA] Returns information about the conversion. Status is always present 
        and its value (not_started, running, completed, failed, rejected) 
        represents the current state of the conversion. Lead ID is only present 
        if the conversion was successfully finished. This data is only temporary 
        and removed after a few days.

        Args:
            conversion_id: The ID of the conversion process (UUID).
        Returns:
            Dictionary containing conversion status data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/convert/status/{conversion_id}"
        return self.get_api(version=V2).get(uri=uri).to_dict()

    @warn_endpoint_legacy
    def duplicate(self) -> Self:
        """
        V1 endpoint. Duplicate a deal.

        Returns:
            The newly created Deal instance.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/duplicate"
        response = self.get_api(version=V1).post(uri=uri)
        return Deals(**response.data)

    def add_follower(self, user_id: int) -> Dict:
        """
        Add a follower to a deal.

        Args:
            user_id: The ID of the user to add as a follower.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(user_id, int), "`user_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers"
        body = {"user_id": user_id}
        return self.get_api(version=V2).post(uri=uri, json=body).to_dict()

    @warn_endpoint_legacy
    def add_participant(self, person_id: int = None) -> Dict:
        """
        V1 endpoint. Adds a participant to a deal.

        Args:
            person_id: The ID of the person/participant to add to the deal.
        Returns:
            The API response data as a dictionary.
        """
        assert person_id is not None, "`person_id` must be provided."
        assert isinstance(person_id, int), "`person_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/participants"
        body = {"person_id": person_id}
        return self.get_api(version=V1).post(uri=uri, json=body).to_dict()

    def add_product(
        self,
        product_id: int = None,
        item_price: Union[int, float] = None,
        quantity: Union[int, float] = None,
        params: Dict = {}) -> Dict:
        """
        Add a product to a deal. Allowed query params:
            - product_id (int): The ID of the product.
            - item_price (number): The price value of the product.
            - quantity (number): The quantity of the product.
            - tax (number): The product tax.
            - comments (str): The comments of the product.
            - discount (number): The value of the discount. The `discount_type` 
                                 field can be used to specify whether the value 
                                 is an amount or a percentage. Default: 0.
            - is_enabled (bool): Whether this product is enabled for the deal.
                                 Not possible to disable the product if the deal 
                                 has installments associated and the product is 
                                 the last one enabled. Not possible to enable the 
                                 product if the deal has installments associated 
                                 and the product is recurring. Deafult: true.
            - tax_method (str): The tax option to be applied to the products. 
                                When using inclusive, the tax percentage will 
                                already be included in the price. When using 
                                exclusive, the tax will not be included in the 
                                price. When using none, no tax will be added. 
                                Use the tax field for defining the tax percentage 
                                amount. By default, the user setting value for 
                                tax options will be used. Changing this in one 
                                product affects the rest of the products attached 
                                to the deal.
            - discount_type (str): The value of the discount. The `discount_type` 
                                   field can be used to specify whether the 
                                   value is an amount or a percentage.
                                   Values: `percentage` (default), `amount`.
            - product_variation_id (int): The ID of the product variation.
            - billing_frequency (str): Only available in Growth and above plans.
                                       How often a customer is billed for access 
                                       to a service or product. To set 
                                       `billing_frequency` different than one-time, 
                                       the deal must not have installments 
                                       associated. A deal can have up to 20 
                                       products attached with `billing_frequency` 
                                       different than one-time.
            - billing_frequency_cycles (int): Only available in Growth and above 
                                              plans. The number of times the 
                                              billing frequency repeats for a 
                                              product in a deal. When 
                                              `billing_frequency` is set to 
                                              one-time, this field must be `null`.
                                              When `billing_frequency` is set 
                                              to weekly, this field cannot be 
                                              `null`. For all the other values 
                                              of `billing_frequency`, `null` 
                                              represents a product billed 
                                              indefinitely. Must be a positive 
                                              integer less or equal to 208.
            - billing_start_date (str): Only available in Growth and above plans.
                                        The billing start date. Must be between 
                                        10 years in the past and 10 years in the 
                                        future. Format: YYYY-MM-DD.

        Args:
            product_id: The ID of the product to add to the deal.
            item_price: The price value of the product.
            quantity: The quantity of the product.
            params: Query params passed to the API (copied internally).
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(product_id, int), "`product_id` must be an integer."
        assert isinstance(item_price, (int, float)), "`item_price` must be a number."
        assert isinstance(quantity, (int, float)), "`quantity` must be a number."
        params["product_id"] = product_id
        params["item_price"] = item_price
        params["quantity"] = quantity
        uri = f"{self._get_meta('entity_name')}/{self.id}/products"
        return self.get_api(version=V2).post(uri=uri, json=params).to_dict()

    def add_product_bulk(self, data: List[Dict]) -> Dict:
        """
        Add multiple products to a deal in bulk.

        Args:
            data: List of product dictionaries to add to the deal. See 
                  Deals.add_product() for the structure of each dictionary.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(data, list) and all(isinstance(d, dict) for d in data), \
            "`data` must be a list of dictionaries."
        uri = f"{self._get_meta('entity_name')}/{self.id}/products/bulk"
        return self.get_api(version=V2).post(uri=uri, json={"data": data}).to_dict()

    def add_discount(
        self,
        description: str = None,
        amount: Union[int, float] = None,
        type: str = None) -> Dict:
        """
        Adds a discount to a deal.
        
        Args:
            description: The description of the discount.
            amount: The discount amount. Must be a positive number (excl. 0).
            type: Determines whether the discount is applied as a `percentage` 
                  or a fixed amount.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(description, str), "`description` must be a string."
        assert isinstance(amount, (int, float)) and amount > 0, \
            "`amount` must be a positive number."
        assert type in ["percentage", "amount"], \
            "`type` must be either 'percentage' or 'amount'."
        body = {
            "description": description,
            "amount": amount,
            "type": type,
        }
        uri = f"{self._get_meta('entity_name')}/{self.id}/discounts"
        return self.get_api(version=V2).post(uri=uri, json=body).to_dict()

    @warn_endpoint_beta
    def add_installment(
        self,
        description: str = None,
        amount: Union[int, float] = None,
        billing_date: str = None) -> Dict:
        """
        Adds an installment to a deal.
        
        An installment can only be added if the deal includes at least one 
        one-time product. If the deal contains at least one recurring product, 
        adding installments is not allowed.

        Only available in Growth and above plans.

        Args:
            description: The description of the discount.
            amount: The discount amount. Must be a positive number (excl. 0).
            billing_date: The date which the installment will be charged. 
                          Must be in the format YYYY-MM-DD.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(description, str), "`description` must be a string."
        assert isinstance(amount, (int, float)) and amount > 0, \
            "`amount` must be a positive number."
        assert isinstance(billing_date, (str, date)), "`billing_date` must be a string or date."
        if isinstance(billing_date, str):
            assert date.fromisoformat(billing_date), "`billing_date` wrong format (YYYY-MM-DD)."
        else:
            billing_date = billing_date.strftime("%Y-%m-%d")
        body = {
            "description": description,
            "amount": amount,
            "billing_date": billing_date,
        }
        uri = f"{self._get_meta('entity_name')}/{self.id}/installments"
        return self.get_api(version=V2).post(uri=uri, json=body).to_dict()

    @warn_endpoint_beta
    def convert_to_lead(self) -> Dict:
        """
        Initiates a conversion of a deal to a lead.

        The return value is an ID of a job that was assigned to perform the 
        conversion. Related entities (notes, files, emails, activities, ...) 
        are transferred during the process to the target entity. There are 
        exceptions for entities like invoices or history that are not transferred 
        and remain linked to the original deal. If the conversion is successful, 
        the deal is marked as deleted.

        To retrieve the created entity ID and the result of the conversion, use
        `/api/v2/deals/{deal_id}/convert/status/{conversion_id}` endpoint.

        Returns:
            The API response data as a dictionary.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/convert/lead"
        return self.get_api(version=V2).post(uri=uri).to_dict()

    @warn_endpoint_legacy
    def merge(self, merge_with_id: int) -> Dict:
        """
        V1 endpoint. Merges a deal with another deal.

        Args:
            merge_with_id: The ID of the deal to merge into this deal.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(merge_with_id, int), "`merge_with_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/merge"
        body = {"merge_with_id": merge_with_id}
        return self.get_api(version=V1).put(uri=uri, json=body).to_dict()

    def update_attached_product(
        self,
        product_attachment_id: int,
        params: Dict = {}) -> Dict:
        """
        Updates the details of the product that has been attached to a deal.

        Args:
            product_attachment_id: The ID of the deal-product (the ID of the 
                                   product attached to the deal).
            params: Query params passed to the API (copied internally).
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(product_attachment_id, int), \
            "`product_attachment_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/products/{product_attachment_id}"
        return self.get_api(version=V2).patch(uri=uri, json=params).to_dict()

    def update_discount(self, discount_id: str, params: Dict = {}) -> Dict:
        """
        Edits a discount added to a deal, changing the deal value if the deal 
        has one-time products attached.

        Args:
            discount_id: The ID of the discount. Format UUID.
            params: Query params passed to the API (copied internally).
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(discount_id, str), "`discount_id` must be a string."
        uri = f"{self._get_meta('entity_name')}/{self.id}/discounts/{discount_id}"
        return self.get_api(version=V2).patch(uri=uri, json=params).to_dict()

    def update_installment(self, installment_id: int, params: Dict = {}) -> Dict:
        """
        Edits an installment added to a deal.

        Only available in Growth and above plans.

        Args:
            installment_id: The ID of the installment.
            params: Query params passed to the API (copied internally).
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(installment_id, int), "`installment_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/installments/{installment_id}"
        return self.get_api(version=V2).patch(uri=uri, json=params).to_dict()

    def delete_follower(self, follower_id: int) -> Dict:
        """
        Deletes a user follower from the deal.

        Args:
            follower_id: The ID of the follower to delete.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(follower_id, int), "`follower_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers/{follower_id}"
        return self.get_api(version=V2).delete(uri=uri).to_dict()

    @warn_endpoint_legacy
    def delete_participant(self, deal_participant_id: int) -> Dict:
        """
        Deletes a user participant from the deal.

        Args:
            deal_participant_id: The ID of the participant of the deal.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(deal_participant_id, int), "`deal_participant_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/participants/{deal_participant_id}"
        return self.get_api(version=V1).delete(uri=uri).to_dict()

    def delete_products(self, ids: List[int]) -> Dict:
        """
        Deletes multiple products from a deal. If no product IDs are specified, 
        up to 100 products will be removed from the deal. A maximum of 100 
        product IDs can be provided per request.

        Args:
            ids: Comma-separated list of deal product IDs to delete. If not 
                 provided, all deal products will be deleted up to 100 items. 
                 Maximum 100 IDs allowed.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(ids, list), "`ids` must be a list of integers."
        assert all(isinstance(i, int) for i in ids), "`ids` must be a list of integers."
        params = {"ids": ",".join(map(str, ids))}
        uri = f"{self._get_meta('entity_name')}/{self.id}/products"
        return self.get_api(version=V2).delete(uri=uri, params=params).to_dict()

    def delete_attached_product(self, product_attachment_id: int) -> Dict:
        """
        Deletes a product attached to a deal using `product_attachment_id`.

        Args:
            product_attachment_id: The ID of the deal-product (the ID of the 
                                   product attached to the deal).
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(product_attachment_id, int), \
            "`product_attachment_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/products/{product_attachment_id}"
        return self.get_api(version=V2).delete(uri=uri).to_dict()

    def delete_discount(self, discount_id: str) -> Dict:
        """
        Deletes a discount added to a deal.

        Args:
            discount_id: The ID of the discount. Format UUID.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(discount_id, str), "`discount_id` must be a string."
        uri = f"{self._get_meta('entity_name')}/{self.id}/discounts/{discount_id}"
        return self.get_api(version=V2).delete(uri=uri).to_dict()

    @warn_endpoint_beta
    def delete_installment(self, installment_id: int) -> Dict:
        """
        Deletes an installment added to a deal.

        Only available in Growth and above plans.

        Args:
            installment_id: The ID of the installment.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(installment_id, int), "`installment_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/installments/{installment_id}"
        return self.get_api(version=V2).delete(uri=uri).to_dict()