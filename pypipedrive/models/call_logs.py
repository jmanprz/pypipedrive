from typing import Dict, List
from typing_extensions import Self
from pypipedrive.api import V1
from pypipedrive.utils import warn_endpoint_legacy, build_multipart_file_tuple
from pypipedrive.orm.model import Model, SaveResult
from pypipedrive.orm import fields as F


class CallLogs(Model):
    """
    Call logs describe the outcome of a phone call managed by an integrated 
    provider. Since these logs are also considered activities, they can be 
    associated with a deal or a lead, a person and/or an organization. Call 
    logs do differ from other activities, as they only receive the information 
    needed to describe the phone call.

    See `CallLogs API reference <https://developers.pipedrive.com/docs/api/v1/CallLogs>`_.

    Returns all call logs assigned to a particular user.

      * GET[Cost:20] ``v1/callLogs``

    Returns details of a specific call log.

      * GET[Cost:2] ``v1/callLogs/{id}``

    Adds a new call log.

      * POST[Cost:10] ``v1/callLogs``

    Attach an audio file to the call log.

      * POST[Cost:10] ``v1/callLogs/{id}/recording``

    Deletes a call log.

      * DELETE[Cost:6] ``v1/callLogs/{id}``
    """

    id                = F.TextField("id")
    activity_id       = F.IntegerField("activity_id")
    person_id         = F.IntegerField("person_id")
    org_id            = F.IntegerField("org_id")
    deal_id           = F.IntegerField("deal_id")
    subject           = F.TextField("subject")
    duration          = F.IntegerField("duration")
    # connected, no_answer, left_message, left_voicemail, wrong_number, busy
    outcome           = F.TextField("outcome") # TODO: add choice validation
    from_phone_number = F.TextField("from_phone_number")
    to_phone_number   = F.TextField("to_phone_number")
    has_recording     = F.BooleanField("has_recording")
    start_time        = F.DatetimeField("start_time")
    end_time          = F.DatetimeField("end_time")
    user_id           = F.IntegerField("user_id")
    company_id        = F.IntegerField("company_id")
    note              = F.TextField("note")

    class Meta:
        entity_name = "callLogs"
        version     = V1
    
    @warn_endpoint_legacy
    @classmethod
    def get(cls, *args, **kwargs) -> Self:
        """
        Returns details of a specific call log.
        """
        return super().get(*args, **kwargs)
    
    @warn_endpoint_legacy
    @classmethod
    def all(cls, *args, **kwargs) -> List[Self]:
        """
        Returns all call logs assigned to a particular user.

        Allowed query parameters:

            - ``start`` (int): Pagination start. Defaults: 0.
            - ``limit`` (int): For pagination, the limit of entries to be returned. 
              The upper limit is 50.

        Returns:
            A list of CallLog instances.
        """
        return super().all(*args, **kwargs)

    @warn_endpoint_legacy
    def save(self, *args, **kwargs) -> SaveResult:
        """
        Adds a new call log. Mandatory fields:

            - ``outcome`` (str): Describes the outcome of the call. Values: 
              connected, no_answer, left_message, left_voicemail, wrong_number, 
              busy.
            - ``to_phone_number`` (str): The number called.
            - ``start_time`` (str): The date and time of the start of the call 
              in UTC. Format: YYYY-MM-DD HH:MM:SS.
            - ``end_time`` (str): The date and time of the end of the call in 
              UTC. Format: YYYY-MM-DD HH:MM:SS.
        """
        return super().save(*args, **kwargs)

    @warn_endpoint_legacy
    def delete(self, *args, **kwargs) -> bool:
        return super().delete(*args, **kwargs)

    @warn_endpoint_legacy
    @classmethod
    def batch_delete(cls, *args, **kwargs):
        raise NotImplementedError("CallLogs.batch_delete() is not allowed.")

    @warn_endpoint_legacy
    def attach_audio_file(
        self,
        data: bytes,
        file_name: str,
        content_type: str) -> Dict:
        """
        Adds an audio recording to the call log. That audio can be played by 
        those who have access to the call log object.

        Args:
            data: The binary data of the audio file.
            file_name: The name of the audio file.
            content_type: The MIME type of the audio file.
        Returns:
            The API response as a dictionary ({success: true}).
        """
        assert isinstance(data, bytes), "data must be bytes"
        assert isinstance(file_name, str), "file_name must be a string"
        assert isinstance(content_type, str), "content_type must be a string"

        files = {
            "file": build_multipart_file_tuple(
                data         = data,
                file_name    = file_name,
                content_type = content_type,
            )
        }
        uri = f"{self._get_meta('entity_name')}/{self.id}/recordings"
        return self.get_api(version=V1).post(uri=uri, files=files).to_dict()