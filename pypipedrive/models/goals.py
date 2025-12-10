from typing import Dict, List, Optional, Union
from typing_extensions import Self
from datetime import date
from pypipedrive.api import V1
from pypipedrive.api.api import ApiResponse
from pypipedrive.utils import warn_endpoint_legacy
from pypipedrive.orm.model import Model, SaveResult
from pypipedrive.orm import fields as F


class Goals(Model):
    """
    Goals help your team meet your sales targets. There are three types of 
    goals - company, team and user.

    See `Goals API reference <https://developers.pipedrive.com/docs/api/v1/Goals>`_.

    Find goals.

      * GET[Cost:20] ``v1/goals/find``

    Get result of a goal.

      * GET[Cost:20] ``v1/goals/{id}/results``

    Add a new goal.

      * POST[Cost:10] ``v1/goals``

    Update an existing goal.

      * PUT[Cost:10] ``v1/goals/{id}``

    Delete existing goal.

      * DELETE[Cost:6] ``v1/goals/{id}``
    """

    id               = F.TextField("id", readonly=True)
    owner_id         = F.IntegerField("owner_id")
    title            = F.TextField("title")
    interval         = F.TextField("interval")
    is_active        = F.BooleanField("is_active")
    type             = F.TypeField("type")
    assignee         = F.AssigneeField("assignee")
    duration         = F.GoalDurationField("duration")
    expected_outcome = F.ExpectedOutcomeField("expected_outcome")
    report_ids       = F.LabelIdsField("report_ids")
    seasonality      = F.SeasonalityField("seasonality")
    # Indicates the Goal's progress for the specified period. Not None only
    # when calling Goal(id=...).results()
    progress         = F.NumberField("progress", readonly=True)

    class Meta:
        entity_name = "goals"
        version     = V1

    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs) -> any:
        raise NotImplementedError("Goals.get() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def all(cls, *args, **kwargs) -> any:
        raise NotImplementedError("Goals.all() is not allowed.")

    @warn_endpoint_legacy
    def save(self, *args, **kwargs) -> SaveResult:
        """
        Adds a new goal. Along with adding a new goal, a report is created to 
        track the progress of your goal.

        Fields to create a Goal:

            - ``title`` (str): The title of the goal.
            - ``assignee`` (object): Who this goal is assigned to. It requires 
              the following JSON structure: ``{ "id": "1", "type": "person" }``. 
              ``type`` can be either ``person``, ``company`` or ``team``. ID of 
              the assignee person, company or team.
            - ``type`` (object): The type of the goal. It requires the 
              following JSON structure: ``{ "name": "deals_started", "params": 
              { "pipeline_id": [1, 2], "activity_type_id": [9] } }``. Type can 
              be one of: ``deals_won``, ``deals_progressed``, 
              ``activities_completed``, ``activities_added``, ``deals_started`` 
              or ``revenue_forecast``. ``params`` can include ``pipeline_id``, 
              ``stage_id`` or ``activity_type_id``. ``stage_id`` is related to 
              only ``deals_progressed`` type of goals and ``activity_type_id`` 
              to ``activities_completed`` or ``activities_added`` types of goals. 
              The ``pipeline_id`` and ``activity_type_id`` need to be given as 
              an array of integers. To track the goal in all pipelines, set 
              ``pipeline_id`` as ``null`` and similarly, to track the goal for 
              all activities, set ``activity_type_id`` as ``null``.
            - ``expected_outcome`` (object): The expected outcome of the goal. 
              Expected outcome can be tracked either by ``quantity`` or by 
              ``sum``. It requires the following JSON structure: ``{ "target": 
              "50", "tracking_metric": "quantity" }`` or ``{ "target": "50", 
              "tracking_metric": "sum", "currency_id": 1 }``. ``currency_id`` 
              should only be added to ``sum`` type of goals.
            - ``duration`` (object): The date when the goal starts and ends. 
              It requires the following JSON structure: 
              ``{ "start": "2019-01-01", "end": "2022-12-31" }``. Date in 
              format of YYYY-MM-DD. "end" can be set to ``null`` for an 
              infinite, open-ended goal.
            - ``interval`` (str): The interval of the goal. Values: 
              ``weekly``, ``monthly``, ``quarterly``, ``yearly``.
        
        Returns:
            A SaveResult object containing the created Goal.
        """
        return super().save(*args, **kwargs)

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs) -> any:
        raise NotImplementedError("Goals.batch_delete() is not allowed.")

    @warn_endpoint_legacy
    @classmethod
    def find(cls, params: Dict = {}) -> List[Self]:
        """
        Returns data about goals based on criteria. For searching, append 
        ``{searchField}={searchValue}`` to the URL, where ``searchField`` can be 
        any one of the lowest-level fields in dot-notation (e.g. 
        ``type.params.pipeline_id``; ``title``). ``searchValue`` should be the 
        value you are looking for on that field. Additionally, 
        ``is_active=<true|false>`` can be provided to search for only 
        active/inactive goals. When providing ``period.start``, ``period.end`` 
        must also be provided and vice versa.

        Allowed query parameters:

            - ``type.name`` (str): The type of the goal. If provided, everyone's 
              goals will be returned. Values: deals_won, deals_progressed,
              activities_completed, activities_added, deals_started.
            - ``title`` (str): The title of the goal.
            - ``is_active`` (bool): Whether the goal is active or not. Default:
              true.
            - ``assignee.id`` (int): The ID of the user who's goal to fetch. 
              When omitted, only your goals will be returned.
            - ``assignee.type`` (str): The type of the goal's assignee. If 
              provided, everyone's goals will be returned. Values: person,
              company, team.
            - ``expected_outcome.target`` (number): The numeric value of the 
              outcome. If provided, everyone's goals will be returned.
            - ``expected_outcome.tracking_metric`` (str): The tracking metric 
              of the expected outcome of the goal. If provided, everyone's 
              goals will be returned. Values: quantity, sum.
            - ``expected_outcome.currency_id`` (int): The numeric ID of the 
              goal's currency. Only applicable to goals with 
              expected_outcome.tracking_metric with value sum. If provided, 
              everyone's goals will be returned.
            - ``type.params.pipeline_id`` (int): An array of pipeline IDs or 
              null for all pipelines. If provided, everyone's goals will be 
              returned.
            - ``type.params.stage_id`` (int): The ID of the stage. Applicable 
              to only deals_progressed type of goals. If provided, everyone's 
              goals will be returned.
            - ``type.params.activity_type_id`` (int): An array of IDs or null 
              for all activity types. Only applicable for ``activities_completed`` 
              and/or ``activities_added`` types of goals. If provided, everyone's 
              goals will be returned.
            - ``period.start`` (str): The start date of the period for which to 
              find the goal's progress. Format: YYYY-MM-DD. This date must be 
              the same or after the goal duration start date.
            - ``period.end`` (str): The end date of the period for which to 
              find the goal's progress. Format: YYYY-MM-DD. This date must be 
              the same or before the goal duration end date.

        Args:
            params: Additional search parameters.
        Returns:
            A dictionary containing the goals found.
        """
        uri = f"{cls._get_meta('entity_name')}/find"
        response: ApiResponse = cls.get_api(version=V1).get(uri, params=params)
        return [cls(**goal) for goal in response.data.get("goals") or []]

    @warn_endpoint_legacy
    def results(
        self,
        period_start: Union[str, date],
        period_end: Union[str, date]) -> Optional[Self]:
        """
        Gets the progress of a goal for the specified period.

        Mandatory query parameters:

            - ``period.start`` (str): The start date of the period for which to 
              find the goal's progress. Format: YYYY-MM-DD. This date must be 
              the same or after the goal duration start date.
            - ``period.end`` (str): The end date of the period for which to 
              find the goal's progress. Format: YYYY-MM-DD. This date must be 
              the same or before the goal duration end date.

        Returns:
            A dictionary containing the goals found.
        """
        assert isinstance(period_start, (str, date)), \
            "`period_start` must be a string or date."
        assert isinstance(period_end, (str, date)), \
            "`period_end` must be a string or date."
        if isinstance(period_start, date):
            period_start = period_start.isoformat()
        if isinstance(period_end, date):
            period_end = period_end.isoformat()
        uri = f"{self._get_meta('entity_name')}/{self.id}/results"
        params = {"period.start": period_start, "period.end": period_end}
        response = self.get_api(version=V1).get(uri, params=params)
        goal = response.data.get("goal")
        if goal:
            return Goals(**goal, progress=response.data.get("progress"))
        return None