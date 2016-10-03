# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import pytz


########################################################################
def now():
    return datetime.datetime.now(tz=pytz.UTC)


########################################################################
def today():
    return datetime.date.today()


########################################################################
def timedelta(datetime_obj, days=0, hours=0, seconds=0):
    return datetime_obj - datetime.timedelta(days=days, hours=hours, seconds=seconds)


########################################################################
def generate_datetime(year, month, day, hour, minute, second, tzinfo):
    return datetime.datetime(year, month, day, hour, minute, second, tzinfo=tzinfo)
