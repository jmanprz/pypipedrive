from typing import Any, Dict, List, Optional
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model, SaveResult
from pypipedrive.orm import fields as F


class MailThreads(Model):
    """
    Mailbox was designed to be the email control hub inside Pipedrive. 
    Pipedrive supports all major providers (including Gmail, Outlook and also 
    custom IMAP/SMTP). There are 2 options for syncing user emails: 2-way 
    sync: Mail Connection is established with the mail provider (example Gmail). 
    There can be only 1 active Mail Connection per user in company. 1-way 
    sync: SmartBCC feature which stores the copies of email messages to 
    Pipedrive by adding the SmartBCC specific address to mail recipients.

    The Mailbox represents the threads. Therefore, querying Mailbox.get will
    return a specific mail thread whereas Mailbox.all will return a list of 
    mail threads.

    See `Mailbox API reference <https://developers.pipedrive.com/docs/api/v1/Mailbox>`_.

    Get one mail thread.

      * GET[Cost:20] ``/v1/mailbox/mailThreads/{id}``

    Get mail threads.

      * GET[Cost:20] ``/v1/mailbox/mailThreads``

    Get all mail messages of mail thread.

      * GET[Cost:20] ``/v1/mailbox/mailThreads/{id}/mailMessages``

    Get one mail message.

      * GET[Cost:2] ``/v1/mailbox/mailMessages/{id}``

    Update mail thread details.

      * PUT[Cost:10] ``/v1/mailbox/mailThreads/{id}``

    Delete mail thread.

      * DELETE[Cost:6] ``/v1/mailbox/mailThreads/{id}``
    """

    id                              = F.IntegerField("id", readonly=True)
    parties                         = F.PartiesField("parties")
    drafts_parties                  = F.LabelIdsField("drafts_parties")
    folders                         = F.LabelIdsField("drafts_parties")
    account_id                      = F.TextField("account_id")
    user_id                         = F.IntegerField("user_id")
    version                         = F.IntegerField("version")
    subject                         = F.TextField("subject")
    snippet                         = F.TextField("snippet")
    snippet_draft                   = F.TextField("snippet_draft")
    snippet_sent                    = F.TextField("snippet_sent")
    message_count                   = F.IntegerField("message_count")
    has_attachments_flag            = F.BooleanField("has_attachments_flag")
    has_inline_attachments_flag     = F.BooleanField("has_inline_attachments_flag")
    has_real_attachments_flag       = F.BooleanField("has_real_attachments_flag")
    has_draft_flag                  = F.BooleanField("has_draft_flag")
    has_sent_flag                   = F.BooleanField("has_sent_flag")
    archived_flag                   = F.BooleanField("archived_flag")
    deleted_flag                    = F.BooleanField("deleted_flag")
    shared_flag                     = F.BooleanField("shared_flag")
    synced_flag                     = F.BooleanField("synced_flag")
    read_flag                       = F.BooleanField("read_flag")
    external_deleted_flag           = F.BooleanField("external_deleted_flag")
    smart_bcc_flag                  = F.BooleanField("smart_bcc_flag")
    first_message_to_me_flag        = F.BooleanField("first_message_to_me_flag")
    mail_tracking_status            = F.TextField("mail_tracking_status")
    mail_link_tracking_enabled_flag = F.BooleanField("mail_link_tracking_enabled_flag")
    last_message_timestamp          = F.DatetimeField("last_message_timestamp")
    first_message_timestamp         = F.DatetimeField("first_message_timestamp")
    last_message_sent_timestamp     = F.DatetimeField("last_message_sent_timestamp")
    last_message_received_timestamp = F.DatetimeField("last_message_received_timestamp")
    add_time                        = F.DatetimeField("add_time")
    update_time                     = F.DatetimeField("update_time")
    deal_id                         = F.IntegerField("deal_id")
    deal_status                     = F.TextField("deal_status")
    all_messages_sent_flag          = F.BooleanField("all_messages_sent_flag")

    class Meta:
        entity_name = "mailbox/mailThreads"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def all(cls, folder: str, params: Dict = {}) -> List[Self]:
        """
        Returns mail threads in a specified folder ordered by the most recent 
        message within.

        Allowed query params:

            - ``start`` (int): Pagination start. Default is 0.
            - ``limit`` (int): Items shown per page.

        Args:
            folder: The folder to get mail threads from. Possible values are: 
            inbox, drafts, sent, archive.
        """
        assert folder in ["inbox", "drafts", "sent", "archive"], \
            "folder must be one of: inbox, drafts, sent, archive"
        uri = f"{cls._get_meta('entity_name')}/mailThreads"
        params.update({"folder": folder})
        response = cls.get_api(version=V1).get(uri, params=params)
        return [cls(**item) for item in response.data]

    @warn_endpoint_legacy
    def update(self) -> SaveResult:
        """
        Updates the properties of a mail thread. Only the update method is
        allowed. Hence, the `id` field must be set.

        Allowed fields to update:

            - ``deal_id`` (int): The deal ID this thread is associated with.
            - ``lead_id`` (str): The lead ID (UUID) this thread is associated with.
            - ``shared_flag`` (int): Whether this thread is shared with other 
              users in your company. Values: 0, 1.
            - ``read_flag`` (int): Whether this thread is read or unread.
              Values: 0, 1.
            - ``archived_flag`` (int): Whether this thread is archived or not. 
              You can only archive threads that belong to Inbox folder. 
              Archived threads will disappear from Inbox. Values: 0, 1.

        Returns:
            The result of the save operation.
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "deal_id": self.deal_id,
            # "lead_id": self.lead_id,  # No lead_id field defined in API docs.
            "shared_flag": int(self.shared_flag) if self.shared_flag is not None else None,
            "read_flag": int(self.read_flag) if self.read_flag is not None else None,
            "archived_flag": int(self.archived_flag) if self.archived_flag is not None else None,
        }
        uri = f"{self._get_meta('entity_name')}/{self.id}"
        _ = self.get_api(version=V1).put(uri=uri, data=data, headers=headers)
        return SaveResult(
            id          = self.id,
            created     = False,
            updated     = True,
            field_names = set(data.keys())
        )

    @warn_endpoint_legacy
    def save(self, *args, **kwargs) -> Any:
        raise NotImplementedError("MailThreads.save() is not allowed (use update()).")

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Any:
        raise NotImplementedError("MailThreads.batch_delete() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def mail_message(cls, message_id: int, params: Dict = {}) -> Optional[Dict]:
        """
        Returns data about a specific mail message.

        Allowed query params:

            - ``include_body`` (number): Whether to include the full message 
              body or not. ``0`` = Don't include, ``1`` = Include.

        Args:
            message_id: The ID of the mail message to fetch.
        """
        uri = f"mailbox/mailMessages/{message_id}"
        response = cls.get_api(version=V1).get(uri, params=params)
        return cls(**response.data)

    @warn_endpoint_legacy
    @classmethod
    def mail_messages(self) -> List[Dict]:
        """
        Returns all the mail messages inside a specified mail thread.

        Returns:
            A list of mail messages.
        """
        uri = f"{self._get_meta('entity_name')}/{self.id}/mailMessages"
        return self.get_api(version=V1).get(uri).data