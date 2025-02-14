from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Activities(Model):
    
    id                        = F.IntegerField("id", readonly=True)
    subject                   = F.TextField("subject")
    type                      = F.TextField("type")
    owner_id                  = F.IntegerField("owner_id")
    is_deleted                = F.BooleanField("is_deleted", readonly=True)
    add_time                  = F.DatetimeField("add_time", readonly=True)
    update_time               = F.DatetimeField("update_time", readonly=True)
    deal_id                   = F.IntegerField("deal_id")
    lead_id                   = F.IntegerField("lead_id")
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
    conference_meeting_id     = F.IntegerField("conference_meeting_id", readonly=True)
    public_description        = F.TextField("public_description")
    priority                  = F.IntegerField("priority")
    note                      = F.TextField("note")

    class Meta:
        id_name     = "id"
        entity_name = "activities"