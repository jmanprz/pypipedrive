from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Pipelines(Model):

    id                          = F.IntegerField("id", readonly=True)
    name                        = F.TextField("name")
    order_nr                    = F.IntegerField("order_nr")
    is_deleted                  = F.BooleanField("is_deleted", readonly=True)
    is_deal_propability_enabled = F.BooleanField("is_deal_probablity_enabled")
    add_time                    = F.DatetimeField("add_time", readonly=True)
    update_time                 = F.DatetimeField("update_time", readonly=True)

    class Meta:
        id_name = "id"
        entity_name = "pipelines"