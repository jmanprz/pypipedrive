from typing import Optional, Tuple, Union
from datetime import datetime, date, time, timedelta
from functools import wraps
import warnings


def datetime_to_iso_str(value: Optional[datetime]) -> Optional[str]:
    """
    Convert ``datetime`` object into a ISO 8601 string e.g. "2014-09-05T12:34:56.000Z"

    Args:
        value: datetime object
    """
    if value in [None, ""]:
        return None
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def datetime_from_iso_str(value: Optional[str]) -> Optional[datetime]:
    """
    Convert an ISO 8601 datetime string into a ``datetime`` object.

    Args:
        value: datetime string, e.g. "2014-09-05T07:00:00.000Z"
    """
    if value in [None, ""]:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def date_to_iso_str(value: Optional[Union[date, datetime]]) -> Optional[str]:
    """
    Convert a ``date`` or ``datetime`` into a ISO 8601 string

    Args:
        value: date or datetime object, e.g. "2014-09-05"
    """
    if value in [None, ""]:
        return None
    return value.strftime("%Y-%m-%d")


def date_from_iso_str(value: Optional[str]) -> Optional[date]:
    """
    Convert ISO 8601 date string into a ``date`` object.

    Args:
        value: date string, e.g. "2014-09-05"
    """
    if value in [None, ""]:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def time_to_iso_str(value: Optional[time]) -> Optional[str]:
    """
    Convert an ISO 8601 time object into a ``time`` string.

    Args:
        value: time string, e.g. "12:34"
    """
    if value in [None, ""]:
        return None
    return datetime.strftime(value, "%H:%M")


def time_from_iso_str(value: Optional[str]) -> Optional[time]:
    """
    Convert an ISO 8601 time string into a ``time`` object.

    Args:
        value: time string, e.g. "12:34"
    """
    if value in [None, ""]:
        return None
    return datetime.strptime(value, "%H:%M")


def duration_to_hh_ss_str(value: Optional[timedelta]) -> Optional[str]:
    """
    Convert an ISO 8601 time object into a ``duration`` string HH:SS.

    Args:
        value: time string, e.g. "00:15" (15 minutes)
    """
    if value in [None, ""]:
        return None
    total_minutes = int(value.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02}:{minutes:02}"


def duration_from_hh_ss_str(value: Optional[str]) -> Optional[timedelta]:
    """
    Convert an ISO 8601 time string HH:SS into a ``duration`` object.

    Args:
        value: time string, e.g. "00:15" (15 minutes)
    """
    if value in [None, ""]:
        return None
    hours, minutes = map(int, value.split(":"))
    return timedelta(hours=hours, minutes=minutes)


def build_multipart_file_tuple(
    data: bytes = None,
    file_name: str = None,
    content_type: str = None) -> Tuple[str, bytes, str]:
    """
    Build the multipart/form-data file tuple for uploading.
    
    Args:
        data: The binary data to upload.
        file_name: The name of the file.
        content_type: The MIME type of the file.
    Returns:
        A dictionary suitable for the `files` parameter in requests.
    """
    import mimetypes
    inferred_type = content_type
    if file_name:
        guessed_type, _ = mimetypes.guess_type(file_name)
        inferred_type = inferred_type or guessed_type

    if inferred_type is None:
        inferred_type = "application/octet-stream"
    return (file_name, data, inferred_type)


class BetaWarning(Warning):
    """Indicates a Pipedrive API endpoint that is still in beta."""


def _warn_decorator(func, message: str, warning_cls=DeprecationWarning):
    """
    Generic decorator to warn about specific features.
    """
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            warnings.warn(message, warning_cls, stacklevel=2)
            return function(*args, **kwargs)
        return wrapper

    if isinstance(func, classmethod):
        return classmethod(decorate(func.__func__))
    if isinstance(func, staticmethod):
        return staticmethod(decorate(func.__func__))
    return decorate(func)


def warn_endpoint_legacy(func, *args, **kwargs):
    """
    Decorator to warn about usage of legacy endpoints (v1) within migrated 
    v2 entities.
    """
    return _warn_decorator(
        func, 
        f"The endpoint used in {func.__qualname__} is using the v1 legacy "
        "entity model. It will be migrated to v2 and deprecated in the future.",
        DeprecationWarning
    )


def warn_endpoint_beta(func):
    """
    Decorator to warn about usage of a BETA endpoint (v2).
    """
    return _warn_decorator(
        func,
        f"The endpoint used in {func.__qualname__} is in BETA. It may change "
        "or be deprecated in the future. See Pipedrive API docs.",
        BetaWarning
    )