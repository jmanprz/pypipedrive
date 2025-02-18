from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Stages(Model):
    """
    Stage is a logical component of a pipeline, and essentially a bucket that can hold a number of deals. In the context of the pipeline a stage belongs to, it has an order number which defines the order of stages in that pipeline.

    https://developers.pipedrive.com/docs/api/v1/Stages
    
    Cost: 5.
    """
    id                  = F.IntegerField("id")
    order_nr            = F.IntegerField("order_nr")
    name                = F.TextField("name")
    is_deleted          = F.BooleanField("is_deleted")
    deal_probability    = F.FloatField("deal_probability")
    pipeline_id         = F.IntegerField("pipeline_id")
    is_deal_rot_enabled = F.BooleanField("is_deal_rot_enabled")
    days_to_rotten      = F.IntegerField("days_to_rotten")
    add_time            = F.DatetimeField("add_time")
    update_time         = F.DatetimeField("update_time")

    class Meta:
        id_name     = "id"
        entity_name = "stages"