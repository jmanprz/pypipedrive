from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Persons(Model):

    id             = F.IntegerField("id", readonly=True)
    name           = F.TextField("name")
    first_name     = F.TextField("first_name")
    last_name      = F.TextField("last_name")
    add_time       = F.DatetimeField("add_time", readonly=True)
    update_time    = F.DatetimeField("update_time", readonly=True)
    visible_to     = F.IntegerField("visible_to")
    owner_id       = F.IntegerField("owner_id", readonly=True)
    label_ids      = F.IntegerField("label_ids")
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

    class Meta:
        id_name       = "id"
        entity_name   = "persons"