from datetime import date
from typing import Dict, Union
from pypipedrive.api import V1, V2
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Pipelines(Model):
    """
    Pipelines are essentially ordered collections of stages.

    Pipedrive API reference: https://developers.pipedrive.com/docs/api/v1/Pipelines

    Get all pipelines.
    GET[Cost:10] v1/pipelines DEPRECATED
    GET[Cost:5]  v2/pipelines

    Get one pipeline.
    GET[Cost:2] v1/pipelines/{id} DEPRECATED
    GET[Cost:1] v2/pipelines/{id}

    Get deals conversion rates in pipeline.
    GET[Cost:40] v1/pipelines/{id}/conversion_statistics

    Get deals in a pipeline.
    GET[Cost:20] v1/pipelines/{id}/deals DEPRECATED

    Get deals movements in pipeline.
    GET[Cost:40] v1/pipelines/{id}/movement_statistics

    Add a new pipeline.
    POST[Cost:10] v1/pipelines DEPRECATED
    POST[Cost:5]  v2/pipelines
    
    Update a pipeline.
    PUT[Cost:10]  v1/pipelines/{id} DEPRECATED
    PATCH[Cost:5] v2/pipelines/{id}

    Delete a pipeline.
    DELETE[Cost:6] v1/pipelines/{id} DEPRECATED
    DELETE[Cost:3] v2/pipelines/{id}
    """

    id                          = F.IntegerField("id", readonly=True)
    name                        = F.TextField("name")
    order_nr                    = F.IntegerField("order_nr")
    is_deleted                  = F.BooleanField("is_deleted", readonly=True)
    is_deal_propability_enabled = F.BooleanField("is_deal_probability_enabled")
    add_time                    = F.DatetimeField("add_time", readonly=True)
    update_time                 = F.DatetimeField("update_time", readonly=True)
    is_selected                 = F.BooleanField("is_selected", readonly=True)

    class Meta:
        entity_name = "pipelines"
        version     = V2

    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("Pipelines.batch_delete() is not allowed.")

    @warn_endpoint_legacy
    def _stastistics(
        self,
        stats_type: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        user_id: int = None) -> Dict:
        """
        Helper method for conversion and movements statistics.

        Args:
            start_date: Start date in format YYYY-MM-DD.
            end_date:   End date in format YYYY-MM-DD.
            user_id:    Optional user ID to filter statistics.
        """
        assert stats_type in ["conversion", "movement"], \
            "`stats_type` must be 'conversion' or 'movement'"
        assert isinstance(start_date, (str, date)), "`start_date` must be str or date"
        assert isinstance(end_date, (str, date)), "`end_date` must be str or date"
        if isinstance(start_date, date):
            start_date = start_date.isoformat()
        if isinstance(end_date, date):
            end_date = end_date.isoformat()
        params = {"start_date": start_date, "end_date": end_date}
        if user_id is not None:
            params.update({"user_id": user_id})
        uri = f"{self._get_meta('entity_name')}/{self.id}/{stats_type}_statistics"
        return self.get_api(version=V1).get(uri=uri, params=params).to_dict()

    @warn_endpoint_legacy
    def conversion_statistics(
        self,
        start_date: Union[str, date],
        end_date: Union[str, date],
        user_id: int = None) -> Dict:
        """
        Returns all stage-to-stage conversion and pipeline-to-close rates for 
        the given time period.

        Args:
            start_date: Start date in format YYYY-MM-DD.
            end_date:   End date in format YYYY-MM-DD.
            user_id:    Optional user ID to filter statistics.
        Returns:
            A dictionary with conversion statistics.
        """
        return self._stastistics("conversion", start_date, end_date, user_id)

    def movement_statistics(
        self,
        start_date: Union[str, date],
        end_date: Union[str, date],
        user_id: int = None) -> Dict:
        """
        Returns statistics for deals movements for the given time period.

        Args:
            start_date: Start date in format YYYY-MM-DD.
            end_date:   End date in format YYYY-MM-DD.
            user_id:    Optional user ID to filter statistics.
        Returns:
            A dictionary with movement statistics.
        """
        return self._stastistics("movement", start_date, end_date, user_id)