from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Deals(Model):

    id                  = F.IntegerField("id", readonly=True)
    title               = F.TextField("title")
    creator_user_id     = F.IntegerField("creator_user_id", readonly=True)
    value               = F.IntegerField("value") # In field currency
    person_id           = F.IntegerField("person_id")
    org_id              = F.IntegerField("org_id")
    stage_id            = F.IntegerField("stage_id")
    currency            = F.TextField("currency") # Of field value
    add_time            = F.DatetimeField("add_time", readonly=True)
    update_time         = F.DatetimeField("update_time", readonly=True)
    status              = F.TextField("status")
    probability         = F.IntegerField("probability")
    lost_reason         = F.TextField("lost_reason")
    visible_to          = F.IntegerField("visible_to")
    close_time          = F.DatetimeField("close_time")
    pipeline_id         = F.IntegerField("pipeline_id")
    won_time            = F.DatetimeField("won_time")
    lost_time           = F.DatetimeField("lost_time")
    stage_change_time   = F.DatetimeField("stage_change_time")
    local_won_date      = F.DateField("local_won_date")
    local_lost_date     = F.DateField("local_lost_date")
    local_close_date    = F.DateField("local_close_date")
    expected_close_date = F.DateField("expected_close_date")
    owner_id            = F.IntegerField("owner_id")
    label_ids           = F.LabelIdsField("label_ids")
    is_deleted          = F.BooleanField("is_deleted", readonly=True)
    origin              = F.TextField("origin")
    origin_id           = F.IntegerField("origin_id")
    channel             = F.TextField("channel")
    channel_id          = F.IntegerField("channel_id")
    is_archived         = F.BooleanField("is_archived")
    archive_time        = F.DatetimeField("archive_time")

    class Meta:
        id_name       = "id"
        entity_name   = "deals"