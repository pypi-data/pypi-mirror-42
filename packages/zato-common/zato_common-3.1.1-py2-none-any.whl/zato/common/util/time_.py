# -*- coding: utf-8 -*-

"""
Copyright (C) 2019, Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from datetime import datetime, timedelta
from time import time
import logging

# Arrow
import arrow

# tzlocal
from tzlocal import get_localzone

# Python 2/3 compatibility
from past.builtins import unicode

# ################################################################################################################################

logger = logging.getLogger(__name__)

# ################################################################################################################################

_epoch = datetime.utcfromtimestamp(0) # Start of UNIX epoch
local_tz = get_localzone()

# ################################################################################################################################

def datetime_to_ms(dt):
    """ Converts a datetime object to a number of milliseconds since UNIX epoch.
    """
    return (dt - _epoch).total_seconds() * 1000

# ################################################################################################################################

def utcnow_as_ms(_time=time):
    """ Returns current UTC time in milliseconds since epoch. As of now, uses time.time but may eventually choose
    to use alternative implementations on different systems.
    """
    return _time()

# ################################################################################################################################

def datetime_from_ms(ms, isoformat=True):
    """ Converts a number of milliseconds since UNIX epoch to a datetime object.
    """
    value = _epoch + timedelta(milliseconds=ms)
    return value.isoformat() if isoformat else value

# ################################################################################################################################

class TimeUtil(object):
    """ A thin layer around Arrow's date/time handling library customized for our needs.
    Default format is always taken from ISO 8601 (so it's sorted lexicographically)
    and default timezone is always UTC.
    """
    def __init__(self, kvdb):
        self.kvdb = kvdb

# ################################################################################################################################

    def get_format_from_kvdb(self, format):
        """ Returns format stored under a key pointed to by 'format' or raises
        ValueError if the key is missing/has no value.
        """
        key = 'kvdb:date-format:{}'.format(format[5:])
        format = self.kvdb.conn.get(key)
        if not format:
            msg = 'Key `{}` does not exist'.format(key)
            logger.error(msg)
            raise ValueError(msg)

        return format

# ################################################################################################################################

    def now(self, format='YYYY-MM-DD HH:mm:ss', tz=local_tz.zone, needs_format=True, delta=None):
        """ Returns now in a specified timezone.
        """
        now = arrow.now(tz=tz)
        if delta:
            now = now + delta
        if needs_format:
            return now.format(format)
        return now

# ################################################################################################################################

    def yesterday(self, format='YYYY-MM-DD HH:mm:ss', tz=local_tz.zone, needs_format=True):
        return self.now(format, tz, needs_format, delta=timedelta(days=-1))

# ################################################################################################################################

    def tomorrow(self, format='YYYY-MM-DD HH:mm:ss', tz=local_tz.zone, needs_format=True):
        return self.now(format, tz, needs_format, delta=timedelta(days=1))

# ################################################################################################################################

    def utcnow(self, format='YYYY-MM-DD HH:mm:ss', needs_format=True):
        """ Returns now in UTC formatted as given in 'format'.
        """
        return self.now(format, 'UTC', needs_format)

# ################################################################################################################################

    def today(self, format='YYYY-MM-DD', tz=local_tz.zone, needs_format=True):
        """ Returns current day in a given timezone.
        """
        now = arrow.now(tz=tz)
        today = arrow.Arrow(year=now.year, month=now.month, day=now.day)

        if tz != 'UTC':
            today = today.to(tz)

        if format.startswith('kvdb:'):
            format = self.get_format_from_kvdb(format)

        if needs_format:
            return today.format(format)
        else:
            return today

# ################################################################################################################################

    def isonow(self, tz=local_tz.zone, needs_format=True, _format='YYYY-MM-DDTHH:mm:ss.SSSSSS'):
        return self.now(_format, tz, needs_format)

# ################################################################################################################################

    def isoutcnow(self, needs_format=True, _format='YYYY-MM-DDTHH:mm:ss.SSSSSS'):
        return self.utc_now(_format, needs_format)

# ################################################################################################################################

    def reformat(self, value, from_, to):
        """ Reformats value from one datetime format to another, for instance
        from 23-03-2013 to 03/23/13 (MM-DD-YYYY to DD/MM/YY).
        """
        if from_.startswith('kvdb:'):
            from_ = self.get_format_from_kvdb(from_)

        if to.startswith('kvdb:'):
            to = self.get_format_from_kvdb(to)

        try:
            # Arrow compares to str, not basestring
            value = str(value) if isinstance(value, unicode) else value
            from_ = str(from_) if isinstance(from_, unicode) else from_
            return arrow.get(value, from_).format(to)
        except Exception:
            logger.error('Could not reformat value:`%s` from:`%s` to:`%s`',
                value, from_, to)
            raise

# ################################################################################################################################
