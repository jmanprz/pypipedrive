from typing import Union
from datetime import datetime, date, time, timedelta


def datetime_to_iso_str(value: datetime) -> str:
    """
    Convert ``datetime`` object into a ISO 8601 string e.g. "2014-09-05T12:34:56.000Z"

    Args:
        value: datetime object
    """
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def datetime_from_iso_str(value: str) -> datetime:
    """
    Convert an ISO 8601 datetime string into a ``datetime`` object.

    Args:
        value: datetime string, e.g. "2014-09-05T07:00:00.000Z"
    """
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def date_to_iso_str(value: Union[date, datetime]) -> str:
    """
    Convert a ``date`` or ``datetime`` into a ISO 8601 string

    Args:
        value: date or datetime object, e.g. "2014-09-05"
    """
    return value.strftime("%Y-%m-%d")


def date_from_iso_str(value: str) -> date:
    """
    Convert ISO 8601 date string into a ``date`` object.

    Args:
        value: date string, e.g. "2014-09-05"
    """
    return datetime.strptime(value, "%Y-%m-%d").date()


def time_to_iso_str(value: str) -> time:
    """
    Convert an ISO 8601 time object into a ``time`` string.

    Args:
        value: time string, e.g. "12:34"
    """
    return datetime.strftime(value, "%H:%M")


def time_from_iso_str(value: str) -> time:
    """
    Convert an ISO 8601 time string into a ``time`` object.

    Args:
        value: time string, e.g. "12:34"
    """
    return datetime.strptime(value, "%H:%M")


def duration_to_hh_ss_str(value: str) -> str:
    """
    Convert an ISO 8601 time object into a ``duration`` string HH:SS.

    Args:
        value: time string, e.g. "00:15" (15 minutes)
    """
    total_minutes = int(value.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02}:{minutes:02}"


def duration_from_hh_ss_str(value: str) -> str:
    """
    Convert an ISO 8601 time string HH:SS into a ``duration`` object.

    Args:
        value: time string, e.g. "00:15" (15 minutes)
    """
    hours, minutes = map(int, value.split(":"))
    return timedelta(hours=hours, minutes=minutes)