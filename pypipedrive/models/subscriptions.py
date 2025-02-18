from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Subscriptions(Model):
    """
    Subscriptions represent the revenue that is occurring over time with 
    payments of varying amounts and payment dates (installment subscription) 
    or over fixed intervals of time with payments of the same amount (recurring subscription).

    https://developers.pipedrive.com/docs/api/v1/Subscriptions

    Cost: 2.
    """
    id             = F.IntegerField("id")
    user_id        = F.IntegerField("user_id")
    deal_id        = F.IntegerField("deal_id")
    is_active      = F.BooleanField("is_active")
    cycle_amount   = F.FloatField("cycle_amount")
    cycles_count   = F.IntegerField("cycle_count")
    infinite       = F.BooleanField("infinite")
    currency       = F.TextField("currency")
    start_date     = F.DateField("start_date")
    end_date       = F.DateField("end_date")
    description    = F.TextField("description")
    add_time       = F.DatetimeField("add_time")
    update_time    = F.DatetimeField("update_time")
    lifetime_value = F.FloatField("lifetime_value")
    cadence_type   = F.TextField("cadence_type")
    final_status   = F.TextField("final_status")

    class Meta:
        id_name     = "id"
        entity_name = "subscriptions"
        version     = "v1"

    @classmethod
    def all(cls, *args, **kwargs) -> None:
        raise NotImplementedError("Subscriptions.all() is not allowed. Use Subscriptions.get().")