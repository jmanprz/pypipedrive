from typing import Dict, List
from typing_extensions import Self
from pypipedrive.api import V1, V2
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Stages(Model):
    """
    Stage is a logical component of a pipeline, and essentially a bucket that 
    can hold a number of deals. In the context of the pipeline a stage belongs 
    to, it has an order number which defines the order of stages in that pipeline.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/Stages

    Get all stages.
    GET[Cost:10] v1/stages DEPRECATED
    GET[Cost:5]  v2/stages

    Get one stage.
    GET[Cost:2] v1/stages/{id} DEPRECATED
    GET[Cost:1] v2/stages/{id}

    Get deals in a stage.
    GET[Cost:20] v1/stages/{id}/deals DEPRECATED

    Add a new stage.
    POST[Cost:10] v1/stages DEPRECATED
    POST[Cost:5]  v2/stages

    Update stage details.
    PUT[Cost:10]  v1/stages/{id} DEPRECATED
    PATCH[Cost:5] v2/stages/{id}

    Delete multiple stages in bulk.
    DELETE[Cost:10] v1/stages DEPRECATED

    Delete a stage.
    DELETE[Cost:6] v1/stages/{id} DEPRECATED
    DELETE[Cost:3] v2/stages/{id}
    """

    id                  = F.IntegerField("id")
    order_nr            = F.IntegerField("order_nr")
    name                = F.TextField("name")
    is_deleted          = F.BooleanField("is_deleted")
    deal_probability    = F.NumberField("deal_probability")
    pipeline_id         = F.IntegerField("pipeline_id")
    is_deal_rot_enabled = F.BooleanField("is_deal_rot_enabled")
    days_to_rotten      = F.IntegerField("days_to_rotten")
    add_time            = F.DatetimeField("add_time")
    update_time         = F.DatetimeField("update_time")

    class Meta:
        entity_name = "stages"
        version     = V2
    
    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("Stages.batch_delete() is not allowed.")
    
    @classmethod
    def all(cls, params: Dict = {}) -> List[Self]:
        """
        Returns data about all stages. Allowed query parameters:
            - pipeline_id (int): The ID of the pipeline to fetch stages for. If 
                                 omitted, stages for all pipelines will be fetched.
            - sort_by (str): The field to sort by. Supported fields: 
                             `id` (default), `update_time`, `add_time`, `order_nr`.
            - sort_direction (str): The sorting direction. Supported 
                                    values: `asc` (default), `desc`.
            - limit (int): For pagination, the limit of entries to be returned. 
                           If not provided, 100 items will be returned. Please 
                           note that a maximum value of 500 is allowed.
            - cursor (str): For pagination, the marker (an opaque string value) 
                            representing the first item on the next page.
        """
        return super().all(params=params)