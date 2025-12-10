from typing import Dict, List, Optional, Union
from typing_extensions import Self
from datetime import date
from pypipedrive.api import V1, V2
from pypipedrive.api.api import ApiResponse
from pypipedrive.utils import warn_endpoint_legacy, warn_endpoint_beta
from pypipedrive.orm.model import Model, SaveResult
from pypipedrive.orm import fields as F
from .item_search import ItemSearch


class Leads(Model):
    """
    Leads are potential deals stored in Leads Inbox before they are archived 
    or converted to a deal. Each lead needs to be named (using the ``title`` 
    field) and be linked to a person or an organization. In addition to that, 
    a lead can contain most of the fields a deal can (such as ``value`` or 
    ``expected_close_date``).

    See `Leads API reference <https://developers.pipedrive.com/docs/api/v1/Leads>`_.

    Get all leads.

      * GET[Cost:20] ``v1/leads``

    Get all archived leads.

      * GET[Cost:40] ``v1/leads/archived``

    Get one lead.

      * GET[Cost:2] ``v1/leads/{id}``

    List permitted users.

      * GET[Cost:10] ``v1/leads/permittedUsers``

    Search leads.

      * GET[Cost:40] ``v1/leads/search``
      * GET[Cost:20] ``v2/leads/search``

    Get Lead conversion status (BETA).

      * GET[Cost:1] ``v2/leads/{id}/convert/status/{conversion_id}``

    Add a lead.

      * POST[Cost:10] ``v1/leads``

    Convert a lead to a deal (BETA).

      * POST[Cost:40] ``v2/leads/{id}/convert/deal``

    Update a lead.

      * PATCH[Cost:10] ``v1/leads/{id}``

    Delete a lead.

      * DELETE[Cost:6] ``v1/leads/{id}``
    """

    id                  = F.TextField("id", readonly=True)
    title               = F.TextField("title")
    owner_id            = F.IntegerField("owner_id")
    creator_id          = F.IntegerField("creator_id")
    person_id           = F.IntegerField("person_id")
    organization_id     = F.IntegerField("organization_id")
    label_ids           = F.LabelIdsField("label_ids")
    source_name         = F.TextField("source_name")
    origin              = F.TextField("origin")
    origin_id           = F.IntegerField("origin_id")
    channel             = F.IntegerField("channel")
    channel_id          = F.TextField("channel_id")
    is_archived         = F.BooleanField("is_archived")
    was_seen            = F.BooleanField("was_seen")
    value               = F.MonetaryField("value")
    expected_close_date = F.DateField("expected_close_date")
    next_activity_id    = F.IntegerField("next_activity_id")
    archive_time        = F.DatetimeField("archive_time", readonly=True)
    add_time            = F.DatetimeField("add_time", readonly=True)
    update_time         = F.DatetimeField("update_time", readonly=True)
    visible_to          = F.IntegerField("visible_to")
    cc_email            = F.TextField("cc_email", readonly=True)

    class Meta:
        entity_name = "leads"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> any:
        raise NotImplementedError("Leads.batch_delete() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def archived(cls, params: Dict = {}) -> List[Self]:
        """
        Returns multiple archived leads. Leads are sorted by the time they 
        were created, from oldest to newest. Pagination can be controlled 
        using ``limit`` and ``start`` query parameters. If a lead contains 
        custom fields, the fields' values will be included in the response in 
        the same format as with the ``Deals`` endpoints. If a custom field's 
        value hasn't been set for the lead, it won't appear in the response. 
        Please note that leads do not have a separate set of custom fields, 
        instead they inherit the custom fields' structure from deals.

        Allowed query parameters:

            - ``limit`` (int): For pagination, the limit of entries to be 
              returned. If not provided, 100 items will be returned.
            - ``start`` (int): For pagination, the position that represents 
              the first result for the page.
            - ``owner_id`` (int): If supplied, only leads matching the given 
              user will be returned. However, ``filter_id`` takes precedence 
              over ``owner_id`` when supplied.
            - ``person_id`` (int): If supplied, only leads matching the given 
              person will be returned. However, ``filter_id`` takes precedence 
              over ``person_id`` when supplied.
            - ``organization_id`` (int): If supplied, only leads matching the 
              given organization will be returned. However, ``filter_id`` takes 
              precedence over ``organization_id`` when supplied.
            - ``filter_id`` (int): The ID of the filter to use.
            - ``sort`` (str): The field names and sorting mode separated by a 
              comma (``field_name_1 ASC``, ``field_name_2 DESC``). Only 
              first-level field keys are supported (no nested keys). Values: 
              id, title, owner_id, creator_id, was_seen, expected_close_date,
              next_activity_id, add_time, update_time.

        Args:
            params: Additional query parameters.
        Returns:
            A list of Lead instances.
        """
        uri = f"{cls._get_meta('entity_name')}/archived"
        response = cls.get_api(version=V1).get(uri=uri, params=params)
        return [cls(**lead) for lead in response.data]

    @warn_endpoint_legacy
    def permitted_users(self) -> List[Dict]:
        """
        Lists the users permitted to access a lead.

        Returns:
            List of permitted users data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/permittedUsers"
        return self.get_api(version=V1).get(uri=uri).to_dict()

    @classmethod
    def search(cls, term: str = None, params: Dict = {}) -> List[ItemSearch]:
        """
        Searches all leads by title, notes and/or custom fields. This endpoint 
        is a wrapper of /v1/itemSearch with a narrower OAuth scope. Found leads 
        can be filtered by the person ID and the organization ID.

        Args:
            term: The search term to look for. Minimum 2 characters
            (or 1 if using ``exact_match``). Please note that the search term 
            has to be URL encoded.
            params: Query params passed to the API (copied internally).
        Returns:
            List of ItemSearch objects.
        """
        return ItemSearch.search(term=term, item_types=["lead"], params=params)

    @warn_endpoint_beta
    def conversion_status(self, conversion_id: str) -> Dict:
        """
        Returns data about the conversion. Status is always present and its 
        value (not_started, running, completed, failed, rejected) represents 
        the current state of the conversion. Deal ID is only present if the 
        conversion was successfully finished. This data is only temporary and 
        removed after a few days.

        Args:
            conversion_id: The ID of the conversion process (UUID).
        Returns:
            Dictionary containing conversion status data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/convert/status/{conversion_id}"
        return self.get_api(version=V2).get(uri=uri).to_dict()

    @warn_endpoint_beta
    def convert_to_deal(self) -> Dict:
        """
        Initiates a conversion of a lead to a deal.

        The return value is an ID of a job that was assigned to perform the 
        conversion. Related entities (notes, files, emails, activities, ...) 
        are transferred during the process to the target entity. If the 
        conversion is successful, the lead is marked as deleted.

        To retrieve the created entity ID and the result of the conversion, use
        ``/api/v2/leads/{lead_id}/convert/status/{conversion_id}`` endpoint.

        Allowed query parameters:

            - ``stage_id`` (int): The ID of a stage the created deal will be 
              added to. Please note that a pipeline will be assigned 
              automatically based on the ``stage_id``. If omitted, the deal 
              will be placed in the first stage of the default pipeline.
            - ``pipeline_id`` (int): The ID of a pipeline the created deal 
              will be added to. By default, the deal will be added to the first 
              stage of the specified pipeline. Please note that ``pipeline_id`` 
              and ``stage_id`` should not be used together as ``pipeline_id`` 
              will be ignored.

        Returns:
            The API response data as a dictionary containing the 
            ``conversion_id``.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/convert/deal"
        return self.get_api(version=V2).post(uri=uri, json={}).to_dict()