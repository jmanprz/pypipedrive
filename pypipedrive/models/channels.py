from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Channels(Model):
    """
    Channels API allows you to integrate your existing messaging channels into 
    Pipedrive through Messaging app extension. It enables you to manage and 
    interact with the channel's conversations, participants and messages inside 
    Pipedrive Messaging inbox: get the historical conversation, receive and 
    send new messages. These endpoints are accessible only through Messengers 
    integration OAuth scope together with Messaging manifest in building the 
    Messaging app extension.

    See `Channels API reference <https://developers.pipedrive.com/docs/api/v1/Channels>`_.

    Overall, this entity is fully deprecated and will be removed in future.

    Adds a new messaging channel, only admins are able to register new channels.

      * POST[Cost:10] ``v1/channels`` **DEPRECATED**

    Receives an incoming message

      * POST[Cost:10] ``v1/channels/messages/receive`` **DEPRECATED**

    Deletes an existing messenger's channel and all related entities.

      * DELETE[Cost:6] ``v1/channels/{id}`` **DEPRECATED**

    Deletes an existing conversation.

      * DELETE[Cost:6] ``v1/channels/{channel-id}/conversations/{conversation-id}`` **DEPRECATED**
    """

    id                    = F.TextField("id", readonly=True)
    name                  = F.TextField("name")
    avatar_url            = F.TextField("avatar_url")
    provider_channel_id   = F.TextField("provider_channel_id")
    marketplace_client_id = F.TextField("marketplace_client_id")
    pd_company_id         = F.IntegerField("pd_company_id")
    pd_user_id            = F.IntegerField("pd_user_id")
    created_at            = F.DatetimeField("created_at", readonly=True)
    provider_type         = F.TextField("provider_type")
    template_support      = F.BooleanField("template_support")

    class Meta:
        entity_name = "channels"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError("Channels.get() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def all(cls, *args, **kwargs):
        raise NotImplementedError("Channels.all() is not allowed.")

    @warn_endpoint_legacy
    def save(self, *args, **kwargs):
        """
        Adds a new messaging channel, only admins are able to register new 
        channels. It will use the getConversations endpoint to fetch 
        conversations, participants and messages afterward. To use the 
        endpoint, you need to have Messengers integration OAuth scope enabled 
        and the Messaging manifest ready for the Messaging app extension.
        """
        raise NotImplementedError("Channels.save() is not allowed.")
    
    @warn_endpoint_legacy
    def delete(self, *args, **kwargs):
        """
        Deletes an existing messenger's channel and all related entities 
        (conversations and messages). To use the endpoint, you need to have 
        Messengers integration OAuth scope enabled and the Messaging manifest 
        ready for the Messaging app extension.
        """
        raise NotImplementedError("Channels.delete() is not allowed.")
    
    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("Channels.batch_delete() is not allowed.")