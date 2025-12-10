from typing import Any, List
from pypipedrive.api import V2
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F
from .activity_fields import ActivityFields
from .activity_types import ActivityTypes


class Activities(Model):
    """
    Activities are appointments/tasks/events on a calendar that can be 
    associated with a deal, a lead, a person  and an organization. Activities 
    can be of different type (such as call, meeting, lunch or a custom type - 
    see ActivityTypes object) and can be assigned to a particular user. Note that activities can also be created without a specific date/time.

    See `Activities API reference <https://developers.pipedrive.com/docs/api/v1/Activities>`_.

    Get all activities (BETA) activities/collection.

      * GET[Cost:20] ``v1/activities`` **DEPRECATED**
      * GET[Cost:10] ``api/v2/activities``

    Returns all activities.

      * GET[Cost:10] ``v1/activities/collection`` **DEPRECATED**

    Get details of an activity.

      * GET[Cost:2] ``v1/activities/{id}`` **DEPRECATED**
      * GET[Cost:1] ``api/v2/activities/{id}``
    
    Add an activity.

      * POST[Cost:10] ``v1/activities`` **DEPRECATED**
      * POST[Cost:5]  ``api/v2/activities``

    Update an activity.

      * PUT[Cost:10]  ``v1/activities/{id}`` **DEPRECATED**
      * PATCH[Cost:5] ``api/v2/activities/{id}``

    Delete multiple activities in bulk.

      * DELETE[Cost:10] ``v1/activities`` **DEPRECATED**

    Delete an activity.

      * DELETE[Cost:6] ``v1/activities/{id}`` **DEPRECATED**
      * DELETE[Cost:3] ``api/v2/activities/{id}``
    """

    id                        = F.IntegerField("id", readonly=True)
    subject                   = F.TextField("subject")
    type                      = F.TextField("type")
    owner_id                  = F.IntegerField("owner_id")
    creator_user_id           = F.IntegerField("creator_user_id")
    is_deleted                = F.BooleanField("is_deleted", readonly=True)
    add_time                  = F.DatetimeField("add_time", readonly=True)
    update_time               = F.DatetimeField("update_time", readonly=True)
    deal_id                   = F.IntegerField("deal_id")
    lead_id                   = F.TextField("lead_id")
    person_id                 = F.IntegerField("person_id")
    org_id                    = F.IntegerField("org_id")
    project_id                = F.IntegerField("project_id")
    due_date                  = F.DateField("due_date")
    due_time                  = F.TimeField("due_time")
    duration                  = F.DurationField("duration")
    done                      = F.BooleanField("done")
    busy                      = F.BooleanField("busy")
    marked_as_done_time       = F.DatetimeField("marked_as_done_time", readonly=True)
    location                  = F.AddressField("location")
    participants              = F.ParticipantField("participants")
    attendees                 = F.AttendeeField("attendees")
    conference_meeting_client = F.TextField("conference_meeting_client", readonly=True)
    conference_meeting_url    = F.TextField("conference_meeting_url", readonly=True)
    conference_meeting_id     = F.TextField("conference_meeting_id", readonly=True)
    public_description        = F.TextField("public_description")
    priority                  = F.IntegerField("priority")
    note                      = F.TextField("note")

    class Meta:
        entity_name = "activities"
        version     = V2

    @warn_endpoint_legacy
    @classmethod
    def fields(cls) -> List[ActivityFields]:
        """
        Returns the list of field names for the Activities model.
        """
        return ActivityFields.all()
    
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> Any:
        """
        Delete multiple activities in bulk.
        """
        raise NotImplementedError("ActivityFields.batch_delete() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def types(cls) -> List[ActivityTypes]:
        """
        Returns the list of field types for the Activities model.
        """
        return ActivityTypes.all()