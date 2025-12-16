from typing import Dict, List
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.utils import build_multipart_file_tuple, warn_endpoint_legacy
from pypipedrive.orm.model import Model, SaveResult
from pypipedrive.orm import fields as F


class Files(Model):
    """
    Files are documents of any kind (images, spreadsheets, text files, etc.) 
    that are uploaded to Pipedrive, and usually associated with a particular 
    deal, person, organization, product, note or activity. Remote files can 
    only be associated with a particular deal, person or organization. Note 
    that the API currently does not support downloading files although it lets 
    you retrieve a file's meta-info along with a URL which can be used to 
    download the file by using a standard HTTP GET request.

    See `Files API reference <https://developers.pipedrive.com/docs/api/v1/Files>`_.

    Returns data about all files.

      * GET[Cost:20] ``v1/files``

    Returns data about a specific file.

      * GET[Cost:2] ``v1/files/{id}``

    Download one file.

      * GET[Cost:20] ``v1/files/{id}/download``

    Add file. See `adding files via Pipedrive API <https://developers.pipedrive.com/tutorials/adding-files-via-pipedrive-api>`_.

      * POST[Cost:10] ``v1/files``

    Create a remote file and link it to an item (Google Drive access required).

      * POST[Cost:10] ``v1/files/remote``

    Link a remote file to an item (Google Drive access required).

      * POST[Cost:10] ``v1/files/remoteLink``

    Update file details

      * PUT[Cost:10] ``v1/files/{id}``

    Marks a file as deleted.

      * DELETE[Cost:6] ``v1/files/{id}``
    """

    id              = F.IntegerField("id", readonly=True)
    user_id         = F.IntegerField("user_id", readonly=True)
    deal_id        = F.IntegerField("deal_id")
    person_id       = F.IntegerField("person_id")
    org_id          = F.IntegerField("org_id")
    product_id      = F.IntegerField("product_id")
    activity_id     = F.IntegerField("activity_id")
    lead_id         = F.TextField("lead_id")
    log_id          = F.IntegerField("log_id", readonly=True)
    add_time        = F.DatetimeField("add_time", readonly=True)
    update_time     = F.DatetimeField("update_time", readonly=True)
    file_name       = F.TextField("file_name")
    file_type       = F.TextField("file_type", readonly=True)
    file_size       = F.IntegerField("file_size", readonly=True)
    active_flag     = F.BooleanField("active_flag", readonly=True)
    inline_flag     = F.BooleanField("inline_flag", readonly=True)
    remote_location = F.TextField("remote_location", readonly=True)
    remote_id       = F.TextField("remote_id", readonly=True)
    cid             = F.TextField("cid", readonly=True)
    s3_bucket       = F.TextField("s3_bucket", readonly=True)
    mail_message_id = F.TextField("mail_message_id", readonly=True)
    mail_template_id= F.TextField("mail_template_id", readonly=True)
    deal_name       = F.TextField("deal_name", readonly=True)
    person_name     = F.TextField("person_name", readonly=True)
    lead_name       = F.TextField("lead_name", readonly=True)
    org_name        = F.TextField("org_name", readonly=True)
    product_name    = F.TextField("product_name", readonly=True)
    url             = F.TextField("url", readonly=True)
    name            = F.TextField("name")
    description     = F.TextField("description")
    content         = F.BytesField("content")

    class Meta:
        entity_name = "files"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def all(cls, params: Dict = {}) -> List[Self]:
        """
        Returns data about all files.

        Allowed query parameters:

            - ``start`` (int): Pagination start. Default: 0.
            - ``limit`` (int): Items shown per page. Please note that a 
              maximum value of 100 is allowed.
            - ``sort`` (str): Supported fields: `id`, `update_time`.

        Args:
            params: Dict: Query parameters as a dictionary.
        Returns:
            List of File objects.
        """
        return super().all(params=params)

    @warn_endpoint_legacy
    @classmethod
    def get(cls, id: int) -> Self:
        """
        Returns data about a specific file.

        Args:
            id: int: The ID of the file to retrieve.
        Returns:
            File object.
        """
        return super().get(id=id)

    @warn_endpoint_legacy
    @classmethod
    def save(
        cls, 
        data: bytes,
        file_name: str,
        content_type: str,
        params: Dict = {}) -> Self:
        """
        Lets you upload a file and associate it with a deal, person, organization, 
        activity, product or lead. For more information, see the tutorial for 
        `adding a file <https://pipedrive.readme.io/docs/adding-a-file>`_.

        Args:
            data: The binary content of the file to upload.
            file_name: The name of the file to upload.
            content_type: The MIME type of the file to upload.
            params: Additional parameters for the file upload.
        Returns:
            The uploaded File object (with `content` attached).
        """
        assert isinstance(data, bytes), "data must be bytes"
        assert isinstance(file_name, str), "file_name must be a string"
        assert isinstance(content_type, str), "content_type must be a string"

        files = {
            "file": build_multipart_file_tuple(
                data         = data,
                file_name    = file_name,
                content_type = content_type,
            )
        }
        uri = f"{cls._get_meta('entity_name')}"
        response = cls.get_api(version=V1).post(uri=uri, files=files, params=params)
        obj = cls(**response.data)
        obj.content = data
        return obj

    @warn_endpoint_legacy
    def update(self) -> SaveResult:
        """
        Updates the properties of a file. Only `name` (The visible name of the 
        file) and `description` (the description of the file) can be updated.

        NB: an update method is required (no usage of the Model.save) to modify 
        an existing instance because of the application/x-www-form-urlencoded
        required by the Pipedrive endpoint.

        Returns:
            The SaveResult of the update operation.
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"name": self.name, "description": self.description}
        uri = f"{self._get_meta('entity_name')}/{self.id}"
        _ = self.get_api(version=V1).put(uri=uri, data=data, headers=headers)
        return SaveResult(
            id          = self.id,
            created     = False,
            updated     = True,
            field_names = set(["name", "description"])
        )

    @warn_endpoint_legacy
    def delete(self) -> bool:
        """
        Marks a file as deleted. After 30 days, the file will be permanently 
        deleted.
        """
        return super().delete()

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("Files.batch_delete() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def remote_create(
        cls,
        file_type: str,
        title: str,
        item_type: str,
        item_id: int,
        remote_location: str = "googledrive") -> Self:
        """
        Creates a new empty file in the remote location (`googledrive`) that will 
        be linked to the item you supply. For more information, see the tutorial 
        for `adding a remote file <https://pipedrive.readme.io/docs/adding-a-remote-file>`_.

        NB: The user needs to have an activated Google Account in Pipedrive for 
        the files to be added successfully.
        See `https://{company-name}.pipedrive.com/settings/files <https://{company-name}.pipedrive.com/settings/files>`_.

        Args:
            file_type: The file type. Values `gdoc`, `gslides`, `gsheet`, 
            `gform`, `gdraw`.
            title: The title of the file.
            item_type: The item type. Values: Values: `deal`, `organisation`,
            `person`.
            item_id: The ID of the item to associate the file with.
            remote_location: The location type to send the file to. Only 
            `googledrive` is supported at the moment.
        Returns:
            The created and linked File object.
        """
        assert file_type in ["gdoc", "gslides", "gsheet", "gform", "gdraw"], \
            "file_type must be one of: gdoc, gslides, gsheet, gform, gdraw"
        assert isinstance(title, str), "`title` must be a string"
        assert item_type in ["deal", "organisation", "person"], \
            "`item_type` must be one of: deal, organisation, person"
        assert isinstance(item_id, int), "`item_id` must be an integer"
        assert remote_location == "googledrive", \
            "`remote_location` must be 'googledrive'"

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "file_type":       file_type,
            "title":           title,
            "item_type":       item_type,
            "item_id":         str(item_id),
            "remote_location": remote_location,
        }
        uri = f"{cls._get_meta('entity_name')}/remote"
        response = cls.get_api(version=V1).post(uri=uri, data=data, headers=headers)
        return cls(**response.data)

    @warn_endpoint_legacy
    @classmethod
    def remote_link(
        cls,
        item_type: str,
        item_id: int,
        remote_id: str,
        remote_location: str = "googledrive") -> Self:
        """
        Links an existing remote file (googledrive) to the item you supply. 
        For more information, see the tutorial for adding a remote file.
        See `adding a remote file <https://pipedrive.readme.io/docs/adding-a-remote-file>`_.

        NB: The user needs to have an activated Google Account in Pipedrive for 
        the files to be added successfully.
        See `https://{company-name}.pipedrive.com/settings/files <https://{company-name}.pipedrive.com/settings/files>`_.

        Args:
            item_type: The item type. Values: Values: `deal`, `organisation`,
            `person`.
            item_id: The ID of the item to associate the file with.
            remote_id: The remote item ID.
            remote_location: The location type to send the file to. Only 
            `googledrive` is supported at the moment.
        Returns:
            The linked File object.
        """
        assert isinstance(item_type, str), "`item_type` must be a string"
        assert isinstance(item_id, int), "`item_id` must be an integer"
        assert isinstance(remote_id, str), "`remote_id` must be a string"
        assert remote_location == "googledrive", \
            "`remote_location` must be 'googledrive'"
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "item_type":       item_type,
            "item_id":         str(item_id),
            "remote_id":       remote_id,
            "remote_location": remote_location,
        }
        uri = f"{cls._get_meta('entity_name')}/remoteLink"
        response = cls.get_api(version=V1).post(uri=uri, data=data, headers=headers)
        return cls(**response.data)

    @warn_endpoint_legacy
    def download(self) -> bytes:
        """
        Initializes a file download (attaches the content to the `content` 
        instance field).

        Returns:
            The binary content of the file.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/download"
        self.content = self.get_api().get(uri=uri).data.get("content")
        return self.content