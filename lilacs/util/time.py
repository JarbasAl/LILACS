# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.tz import gettz, tzlocal


def default_timezone(use_local=True):
    """ Get the default timezone

    Based on user location settings location.timezone.code or
    the default system value if no setting exists.

    Returns:
        (datetime.tzinfo): Definition of the default timezone
    """
    if use_local:
        # Just go with system default timezone
        return tzlocal()
    try:
        # Obtain from user's configurated settings (e.g. "America/Chicago")
        from lilacs.settings import TIMEZONE_CODE
        return gettz(TIMEZONE_CODE)
    except Exception:
        default_timezone(use_local=True)


def now_utc():
    """ Retrieve the current time in UTC

    Returns:
        (datetime): The current time in Universal Time, aka GMT
    """
    return datetime.utcnow()


def now_local(tz=None):
    """ Retrieve the current time

    Args:
        tz (datetime.tzinfo, optional): Timezone, default to user's settings

    Returns:
        (datetime): The current time
    """
    if not tz:
        tz = default_timezone()
    return datetime.now(tz)


def to_utc(dt):
    """ Convert a datetime with timezone info to a UTC datetime

    Args:
        dt (datetime): A datetime (presumably in some local zone)
    Returns:
        (datetime): time converted to UTC
    """
    tzUTC = gettz("UTC")
    if dt.tzinfo:
        return dt.astimezone(tzUTC)
    else:
        return dt.replace(tzinfo=gettz("UTC")).astimezone(tzUTC)


def to_local(dt):
    """ Convert a datetime to the user's local timezone

    Args:
        dt (datetime): A datetime (if no timezone, defaults to UTC)
    Returns:
        (datetime): time converted to the local timezone
    """
    tz = default_timezone()
    if dt.tzinfo:
        return dt.astimezone(tz)
    else:
        return dt.replace(tzinfo=gettz("UTC")).astimezone(tz)


def get_timedelta(dt, anchor=None):
    """ Get a datetime object or a int() Epoch timestamp and return a timedelta"""
    anchor = anchor or now_local()
    if type(dt) is int:
        dt = datetime.fromtimestamp(dt, tz=default_timezone())
    if type(anchor) is int:
        anchor = datetime.fromtimestamp(anchor)
    anchor = to_local(anchor)
    dt = to_local(dt)
    return anchor - dt
