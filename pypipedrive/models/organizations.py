from typing_extensions import Self
from typing import Dict, List
from pypipedrive.api import V1, V2
from pypipedrive.api.api import ApiResponse
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F
from .item_search import ItemSearch
from .files import Files


class Organizations(Model):
    """
    Organizations are companies and other kinds of organizations you are making 
    deals with. Persons can be associated with organizations so that each 
    organization can contain one or more persons.

    See `Organizations API reference <https://developers.pipedrive.com/docs/api/v1/Organizations>`_.

    Returns all organizations.

      * GET[Cost:20] ``v1/organizations`` **DEPRECATED**
      * GET[Cost:10] ``v2/organizations``

    Returns all organizations.

      * GET[Cost:10] ``v1/organizations/collection`` **DEPRECATED**

    Searches all organizations by name, address, notes and/or custom fields.

      * GET[Cost:40] ``v1/organizations/search`` **DEPRECATED**
      * GET[Cost:20] ``v2/organizations/search``

    Returns the details of a specific organization.

      * GET[Cost:2] ``v1/organizations/{id}`` **DEPRECATED**
      * GET[Cost:1] ``v2/organizations/{id}``

    Lists activities associated with an organization.

      * GET[Cost:20] ``v1/organizations/{id}/activities`` **DEPRECATED**

    Lists updates about field values of an organization.

      * GET[Cost:20] ``v1/organizations/{id}/changelog``

    Lists deals associated with an organization.

      * GET[Cost:20] ``v1/organizations/{id}/deals`` **DEPRECATED**

    Lists files associated with an organization.

      * GET[Cost:20] ``v1/organizations/{id}/files``

    List updates about an organization.

      * GET[Cost:40] ``v1/organizations/{id}/flow``

    List followers of an organization.

      * GET[Cost:10] ``v2/organizations/{id}/followers``

    List mail messages associated with an organization.

      * GET[Cost:20] ``v1/organizations/{id}/mailMessages``

    List permitted users.

      * GET[Cost:10] ``v1/organizations/{id}/permittedUsers``

    List persons of an organization.

      * GET[Cost:20] ``v1/organizations/{id}/persons`` **DEPRECATED**

    List followers changelog of an organization.

      * GET[Cost:10] ``v2/organizations/{id}/followers/changelog``

    Add an organization.

      * POST[Cost:5] ``v1/organizations`` **DEPRECATED**
      * POST[Cost:5] ``v2/organizations`` 

    Add a follower to an organization.

      * POST[Cost:10] ``v1/organizations/{id}/followers`` **DEPRECATED**
      * POST[Cost:5]  ``v2/organizations/{id}/followers``

    Update an organization.

      * PUT[Cost:10]  ``v1/organizations/{id}`` **DEPRECATED**
      * PATCH[Cost:5] ``v2/organizations/{id}``

    Merge two organizations

      * PUT[Cost:40] ``v1/organizations/{id}/merge``

    Delete multiple organizations in bulk.

      * DELETE[Cost:10] ``v1/organizations`` **DEPRECATED**

    Delete an organization.

      * DELETE[Cost:6] ``v1/organizations/{id}`` **DEPRECATED**
      * DELETE[Cost:3] ``v2/organizations/{id}``

    Delete a follower from an organization.

      * DELETE[Cost:6] ``v1/organizations/{id}/followers/{follower_id}`` **DEPRECATED**
      * DELETE[Cost:3] ``v2/organizations/{id}/followers/{follower_id}``
    """

    id          = F.IntegerField("id", readonly=True)
    name        = F.TextField("name")
    add_time    = F.DatetimeField("add_time", readonly=True) # "2025-02-10T18:06:06Z"
    update_time = F.DatetimeField("update_time", readonly=True) # "2025-02-13T13:20:25Z"
    visible_to  = F.IntegerField("visible_to")
    owner_id    = F.IntegerField("owner_id")
    label_ids   = F.LabelIdsField("label_ids")
    is_deleted  = F.BooleanField("is_deleted", readonly=True)
    address     = F.AddressField("address")

    class Meta:
        entity_name = "organizations"
        version     = V2

    @classmethod
    def all(cls, *args, **kwargs) -> List[Self]:
        """
        Returns all organizations.

        Allowed query parameters:

            - ``filter_id`` (int): If supplied, only organizations matching 
              the specified filter are returned.
            - ``ids`` (str): Optional comma separated string array of up to 
              100 entity ids to fetch. If `filter_id` is provided, this is 
              ignored. If any of the requested entities do not exist or are not 
              visible, they are not included in the response.
            - ``owner_id`` (int): If supplied, only organization owned by the 
              specified user are returned. If `filter_id` is provided, this is 
              ignored.
            - ``updated_since`` (str): If set, only organizations with an 
              `update_time` later than or equal to this time are returned. 
              In RFC3339 format, e.g. 2025-01-01T10:20:00Z.
            - ``updated_till`` (str): If set, only organizations with an 
              `update_time` earlier than this time are returned. In RFC3339 
              format, e.g. 2025-01-01T10:20:00Z.
            - ``sort_by`` (str): The field to sort by. Supported fields: `id`, 
              `update_time`, `add_time`. Default: `id`.
            - ``sort_direction`` (str): The sorting direction. Supported 
              values: `asc`, `desc`. Default: `asc`.
            - ``include_fields`` (str): Optional comma separated string array 
              of additional fields to include.
            - ``custom_fields`` (str): Optional comma separated string array 
              of custom fields keys to include. If you are only interested in a 
              particular set of custom fields, please use this parameter for 
              faster results and smaller response. A maximum of 15 keys is 
              allowed.
            - ``limit`` (int): For pagination, the limit of entries to be 
              returned. If not provided, 100 items will be returned. Please 
              note that a maximum value of 500 is allowed.
            - ``cursor`` (str): For pagination, the marker (an opaque string 
              value) representing the first item on the next page.

        Returns:
            List of Organization instances.
        """
        return super().all(*args, **kwargs)

    @classmethod
    def search(cls, term: str = None, params: Dict = {}) -> List[ItemSearch]:
        """
        Searches all organizations by name, address, notes and/or custom fields.
        This endpoint is a wrapper of /v1/itemSearch with a narrower OAuth scope.

        Args:
            term: The search term to look for. Minimum 2 characters (or 1 if 
            using exact_match). Please note that the search term has to be URL 
            encoded.
            params: Query params passed to the API (copied internally).
        Returns:
            List of ItemSearch objects.
        """
        return ItemSearch.search(term=term, item_types=["organization"], params=params)

    @warn_endpoint_legacy
    def changelog(self, params: Dict = {}) -> List[Dict]:
        """
        V1 endpoint. Lists updates about field values of an organization. 

        Allowed query params:

            - ``limit`` (int): Items shown per page.
            - ``cursor`` (str): For pagination, the marker (an opaque string 
              value) representing the first item on the next page.

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
        Lists files associated with an organization.

        Allowed query params:

            - ``start`` (int): Pagination start. Default: 0.
            - ``limit`` (int): Amount of results to return. Max: 100.
            - ``sort`` (str): Sort order. Possible values: "id", "update_time".

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
        Lists updates about an organization.
        
        Allowed query params:

            - ``start`` (int): Pagination start. Default: 0.
            - ``limit`` (int): Amount of results to return. Default: 100. 
              Max: 500.
            - ``all_changes`` (str): Whether to show custom field updates or 
              not. 1 = Include custom field changes. If omitted returns changes 
              without custom field updates.
            - ``items`` (str): A comma-separated string for filtering out item 
              specific updates. Possible values: call, activity, plannedActivity, 
              change, note, deal, file, dealChange, personChange, 
              organizationChange, follower, dealFollower, personFollower, 
              organizationFollower, participant, comment, mailMessage, 
              mailMessageWithAttachment, invoice, document, 
              marketing_campaign_stat, marketing_status_change.

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            Dictionary containing flow data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/flow"
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    def followers(self, params: Dict = {}) -> List[Dict]:
        """
        Lists users who are following the organization.

        Allowed query params:

            - ``limit`` (int): Amount of results to return. Default: 100.
              Max: 500.
            - ``cursor`` (str): For pagination, the marker (an opaque string 
              value) representing the first item on the next page

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
        List mail messages associated with an organization.

        Allowed query params:

            - ``start`` (int): Pagination start. Default: 0.
            - ``limit`` (int): Items shown per page.

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of mail messages data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/mailMessages"
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def permitted_users(self) -> List[Dict]:
        """
        List users permitted to access an organization.

        Returns:
            List of permitted users data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/permittedUsers"
        return self.get_api(version=V1).get(uri=uri).to_dict()

    def followers_changelog(self, params: Dict = {}) -> Dict:
        """
        Lists changelogs about users have followed the organization.

        Allowed query params:

            - ``limit`` (int): Amount of results to return. Default: 100. 
              Max: 500.
            - ``cursor`` (str): For pagination, the marker (an opaque string 
              value) representing the first item on the next page.

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            Dictionary containing changelog data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers/changelog"
        return self.get_api(version=V2).all(uri=uri, params=params).to_dict()

    def add_follower(self, user_id: int) -> Dict:
        """
        Adds a user as a follower to the organization.

        Args:
            user_id: The ID of the user to add as a follower.
        Returns:
            The API response data as a dictionary.
        """
        assert user_id is not None, "`user_id` must be provided."
        assert isinstance(user_id, int), "`user_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers"
        body = {"user_id": user_id}
        return self.get_api(version=V2).post(uri=uri, json=body).to_dict()

    @warn_endpoint_legacy
    def merge(self, merge_with_id: int) -> Dict:
        """
        Merges an organization with another organization. For more 
        information, see the tutorial for `merging two organizations <https://pipedrive.readme.io/docs/merging-two-organizations>`_.

        Args:
            merge_with_id: The ID of the orgnization to merge into this organization.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(merge_with_id, int), "`merge_with_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/merge"
        body = {"merge_with_id": merge_with_id}
        return self.get_api(version=V1).put(uri=uri, json=body).to_dict()

    def delete_follower(self, follower_id: int) -> Dict:
        """
        Deletes a user follower from the organization.

        Args:
            follower_id: The ID of the follower to delete.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(follower_id, int), "`follower_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers/{follower_id}"
        return self.get_api(version=V2).delete(uri=uri).to_dict()