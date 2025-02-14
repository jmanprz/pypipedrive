from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Organizations(Model):

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
        id_name       = "id"
        entity_name   = "organizations"