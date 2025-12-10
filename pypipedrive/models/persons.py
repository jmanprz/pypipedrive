from typing import Any, List, Dict
from pypipedrive.api import V1, V2
from pypipedrive.api.api import ApiResponse
from pypipedrive.utils import build_multipart_file_tuple, warn_endpoint_legacy
from pypipedrive.orm import fields as F
from pypipedrive.orm.model import Model
from .item_search import ItemSearch
from .files import Files


class Persons(Model):
    """
    Persons are your contacts, the customers you are doing deals with. Each 
    person can belong to an organization. Persons should not be confused with users.

    See `Persons API reference <https://developers.pipedrive.com/docs/api/v1/Persons>`_.

    Get all persons.

      * GET[Cost:20] ``v1/persons`` **DEPRECATED**
      * GET[Cost:10] ``v2/persons``

    Get all persons collection.
      * GET[Cost:10] ``v1/persons/collection`` **DEPRECATED**

    Search persons.

      * GET[Cost:40] ``v1/persons/search`` **DEPRECATED**
      * GET[Cost:20] ``v2/persons/search``

    Get details of a person.

      * GET[Cost:2] ``v1/persons/{id}`` **DEPRECATED**
      * GET[Cost:1] ``v2/persons/{id}``

    List activities associated with a person.

      * GET[Cost:20] ``v1/persons/{id}/activities`` **DEPRECATED**

    List updates about person field values.

      * GET[Cost:20] ``v1/persons/{id}/changelog``

    List deals associated with a person.

      * GET[Cost:20] ``v1/persons/{id}/deals`` **DEPRECATED**

    List files attached to a person.

      * GET[Cost:20] ``v1/persons/{id}/files``

    List updates about a person.

      * GET[Cost:40] ``v1/persons/{id}/flow``

    List followers of a person.

      * GET[Cost:20] ``v1/persons/{id}/followers`` **DEPRECATED**
      * GET[Cost:10] ``v2/persons/{id}/followers``

    List mail messages associated with a person.

      * GET[Cost:20] ``v1/persons/{id}/mailMessages``

    List permitted users.

      * GET[Cost:10] ``v1/persons/{id}/permittedUsers``

    List products associated with a person.

      * GET[Cost:20] ``v1/persons/{id}/products``

    List followers changelog of a person.

      * GET[Cost:10] ``v2/persons/{id}/followers/changelog``

    Add a person.

      * POST[Cost:10] ``v1/persons`` **DEPRECATED**
      * POST[Cost:5]  ``v2/persons``

    Add a follower to a person.

      * POST[Cost:10] ``v1/persons/{id}/followers`` **DEPRECATED**
      * POST[Cost:5]  ``v2/persons/{id}/followers``

    Add person picture.

      * POST[Cost:10] ``v1/persons/{id}/picture``

    Update a person.

      * PUT[Cost:10]  ``v1/persons/{id}`` **DEPRECATED**
      * PATCH[Cost:5] ``v2/persons/{id}``

    Merge two persons.

      * PUT[Cost:40] ``v1/persons/merge``

    Delete multiple persons in bulk.

      * DELETE[Cost:10] ``v1/persons`` **DEPRECATED**

    Delete a person.

      * DELETE[Cost:6] ``v1/persons/{id}`` **DEPRECATED**
      * DELETE[Cost:3] ``v2/persons/{id}``

    Delete a follower from a person.

      * DELETE[Cost:6] ``v1/persons/{id}/followers/{follower_id}`` **DEPRECATED**
      * DELETE[Cost:3] ``v2/persons/{id}/followers/{follower_id}``

    Delete person picture.

      * DELETE[Cost:6] ``v1/persons/{id}/picture``
    """

    id             = F.IntegerField("id", readonly=True)
    name           = F.TextField("name")
    first_name     = F.TextField("first_name")
    last_name      = F.TextField("last_name")
    add_time       = F.DatetimeField("add_time", readonly=True)
    update_time    = F.DatetimeField("update_time", readonly=True)
    visible_to     = F.IntegerField("visible_to")
    owner_id       = F.IntegerField("owner_id", readonly=True)
    label_ids      = F.LabelIdsField("label_ids")
    org_id         = F.IntegerField("org_id", readonly=True)
    is_deleted     = F.BooleanField("is_deleted", readonly=True)
    picture_id     = F.IntegerField("picture_id", readonly=True)
    phones         = F.PhonesField("phones")
    emails         = F.EmailsField("emails")
    im             = F.ImField("im")
    postal_address = F.AddressField("postal_address")
    notes          = F.TextField("notes")
    job_title      = F.TextField("job_title")
    birthday       = F.DateField("birthday")
    custom_fields  = F.CustomFieldsField("custom_fields")

    class Meta:
        entity_name = "persons"
        version     = V2

    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("Persons.batch_delete() not allowed.")

    @classmethod
    def search(cls, term: str = None, params: Dict = {}) -> List[ItemSearch]:
        """
        Searches all persons by name, email, phone, notes and/or custom fields. 
        This endpoint is a wrapper of /v2/itemSearch with a narrower OAuth scope. 
        Found persons can be filtered by organization ID.

        Allowed query parameters:

            - ``fields`` (str): A comma-separated string array. The fields to 
              perform the search from. Defaults to all of them. Only the 
              following custom field types are searchable: `address`, `varchar`, 
              `text`, `varchar_auto`, `double`, `monetary` and `phone`. Read 
              more about `searching by custom fields <https://support.pipedrive.com/en/article/search-finding-what-you-need#searching-by-custom-fields>`_.
            - ``exact_match`` (bool): When enabled, only full exact matches 
              against the given term are returned. It is not case sensitive.
            - ``organization_id`` (int): Will filter persons by the provided 
              organization ID. The upper limit of found persons associated with 
              the organization is 2000.
            - ``include_fields`` (str): Supports including optional fields in 
              the results which are not provided by default. Values: 
              `person.picture`.
            - ``limit`` (int): For pagination, the limit of entries to be 
              returned. If not provided, 100 items will be returned. Please 
              note that a maximum value of 500 is allowed.
            - ``cursor`` (str): For pagination, the marker (an opaque string 
              value) representing the first item on the next page.

        Args:
            term: The search term to look for. Minimum 2 characters (or 1 if 
            using `exact_match`). Please note that the search term has to be 
            URL encoded.
            params: Query params passed to the API (copied internally).
        Returns:
            List of ItemSearch objects.
        """
        return ItemSearch.search(term=term, item_types=["person"], params=params)

    @warn_endpoint_legacy
    def changelog(self, params: Dict = {}) -> List[Dict]:
        """
        V1 endpoint. Lists updates about field values of a person.

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
        uri = f"{self._get_meta("entity_name")}/{self.id}/changelog"
        params={k:v for k,v in params.items() if k in ["cursor", "limit"]}
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def files(self, params: Dict = {}) -> List[Files]:
        """
        Lists files associated with a person.

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
        Lists updates about a person. If a company uses the Campaigns product, 
        then this endpoint's response will also include updates for the 
        `marketing_status` field.

        See `campaigns in Pipedrive API <https://pipedrive.readme.io/docs/campaigns-in-pipedrive-api>`_.

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
        Lists users who are following the person.

        Allowed query params:

            - ``limit`` (int): Amount of results to return. Default: 100.
              Max: 500.
            - ``cursor`` (str): For pagination, the marker (an opaque string 
              value) representing the first item on the next page.

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
        List mail messages associated with a person.

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
        Lists the users permitted to access a person.

        Returns:
            List of permitted users data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/permittedUsers"
        return self.get_api(version=V1).get(uri=uri).to_dict()

    def products(self, params: Dict = {}) -> List[Dict]:
        """
        List products attached to a deal.

        Allowed query params:

            - ``limit`` (int): Amount of results to return. Default: 100. 
              Max: 500.
            - ``cursor`` (str): For pagination, the marker (an opaque string 
              value) representing the first item on the next page.
            - ``sort_by`` (str): Field to sort by. Default "id". Values: "id", 
              "add_time", "update_time", "order_nr".
            - ``sort_direction`` (str): Sort direction. Default "asc".

        Args:
            params: Query params passed to the API (copied internally).
        Returns:
            List of products data.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/products"
        return self.get_api(version=V1).all(uri=uri, params=params).to_dict()

    def followers_changelog(self, params: Dict = {}) -> Dict:
        """
        Lists changelogs about users have followed the person.

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
    def add_picture(
        self,
        data: bytes,
        file_name: str,
        content_type: str,
        params: Dict = {}) -> Dict:
        """
        Adds a picture to a person. If a picture is already set, the old 
        picture will be replaced. Added image (or the cropping parameters 
        supplied with the request) should have an equal width and height and 
        should be at least 128 pixels. GIF, JPG and PNG are accepted. All 
        added images will be resized to 128 and 512 pixel wide squares.

        Allowed query params:

            - ``file`` (binary): One image supplied in the multipart/form-data 
              encoding.
            - ``crop_x`` (int): X coordinate to where start cropping form (in px).
            - ``crop_y`` (int): Y coordinate to where start cropping form (in px).
            - ``crop_width`` (int): The width of the cropping area (in pixels).
            - ``crop_height`` (int): The height of the cropping area (in pixels).
        
        Args:
            data: The binary data of the image file.
            file_name: The name of the image file.
            content_type: The MIME type of the image file.
            params: Additional query parameters.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(data, bytes), "`data` must be bytes"
        assert isinstance(file_name, str), "`file_name` must be a string"
        assert isinstance(content_type, str), "`content_type` must be a string"

        files = {
            "file": build_multipart_file_tuple(
                data         = data,
                file_name    = file_name,
                content_type = content_type,
            )
        }
        uri = f"{self._get_meta('entity_name')}/{self.id}/picture"
        response = self.get_api(version=V1).post(uri=uri, files=files, params=params)
        return response.to_dict()

    @warn_endpoint_legacy
    def merge(self, merge_with_id: int) -> Dict:
        """
        Merges a person with another person. For more information, see the 
        tutorial for `merging two persons <https://pipedrive.readme.io/docs/merging-two-persons>`_.

        If the person doesn't exist defined in `merge_with_id`, a 403 error 
        code is returned.

        Args:
            merge_with_id: The ID of the person to merge into this person.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(merge_with_id, int), "`merge_with_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/merge"
        body = {"merge_with_id": merge_with_id}
        return self.get_api(version=V1).put(uri=uri, json=body).to_dict()

    def delete_follower(self, follower_id: int) -> Dict:
        """
        Deletes a user follower from the person.

        Args:
            follower_id: The ID of the follower to delete.
        Returns:
            The API response data as a dictionary.
        """
        assert isinstance(follower_id, int), "`follower_id` must be an integer."
        uri = f"{self._get_meta('entity_name')}/{self.id}/followers/{follower_id}"
        return self.get_api(version=V2).delete(uri=uri).to_dict()

    @warn_endpoint_legacy
    def delete_picture(self) -> Dict:
        """
        Deletes the picture of a person.

        Returns:
            The API response data as a dictionary.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/picture"
        return self.get_api(version=V1).delete(uri=uri).to_dict()