# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import sys

import mock
import pytz
from six import with_metaclass


########################################################################
class DateTimeMocker(object):
    default = datetime.datetime(2012, 5, 22, 14, 54, 32, 72, tzinfo=pytz.UTC)

    ####################################################################
    def __init__(self, datetime_to_use=None, date_to_use=None, modules=None, search_for_modules=True):
        if datetime_to_use:
            self.datetime_to_use = datetime_to_use
            self.date_to_use = datetime_to_use.date()
        elif date_to_use:
            dt = datetime.datetime.now(tz=pytz.UTC)
            dt = dt.replace(year=date_to_use.year, month=date_to_use.month, day=date_to_use.day)
            self.datetime_to_use = dt
            self.date_to_use = date_to_use
        else:
            self.datetime_to_use = self.default
            self.date_to_use = self.datetime_to_use.date()
        self.original_datetime = datetime.datetime
        self.original_date = datetime.date
        self.modules = modules
        self.mock_datetime_module = make_mock_date_time_module(self.datetime_to_use, self.date_to_use)
        self.mock_datetime = make_mock_date_time(self.datetime_to_use)
        self.mock_date = make_mock_date(self.date_to_use)
        self.mocks = None

        if modules:
            self.mocks = []
            for module in modules:
                self.__add_mocking_to_module(module)
        elif search_for_modules:
            self.mocks = []
            my_module = sys.modules[__name__]
            for module in sys.modules.values():
                if module not in [datetime, my_module]:
                    self.__add_mocking_to_module(module)

    ####################################################################
    def __add_mocking_to_module(self, module):
        datetime_obj = datetime.datetime.now()
        date_obj = datetime.date.today()
        if hasattr(module, "datetime"):
            if module.datetime == datetime:
                self.mocks.append(mock.patch.object(module, "datetime", self.mock_datetime_module, spec=datetime_obj))
            elif module.datetime == datetime.datetime:
                self.mocks.append(mock.patch.object(module, "datetime", self.mock_datetime, spec=date_obj))
        if hasattr(module, "date"):
            if module.date == datetime.date:
                self.mocks.append(mock.patch.object(module, "date", self.mock_date, spec=date_obj))

    ####################################################################
    def __enter__(self):
        datetime_obj = datetime.datetime.now()
        if self.mocks is None:
            datetime.datetime = self.mock_datetime
            datetime.date = self.mock_date
        else:
            for m in self.mocks:
                m.start()

    ####################################################################
    def __exit__(self, type, value, traceback):
        if self.mocks is None:
            datetime.datetime = self.original_datetime
            datetime.date = self.original_date
        else:
            for m in self.mocks:
                m.stop()


########################################################################
def instance_check(mocked_class):
    ####################################################################
    class InstanceCheck(type):
        ################################################################
        def __instancecheck__(self, instance):
            if type(instance) == mocked_class:
                return True
            else:
                return super(self.__class__, self).__instancecheck__(instance)
    return InstanceCheck


########################################################################
def make_mock_date_time(date):
    ####################################################################
    class MockDateTime(with_metaclass(instance_check(datetime.datetime), datetime.datetime)):
        ################################################################
        @classmethod
        def now(cls, tz=None):
            return date

        ################################################################
        @classmethod
        def utcnow(cls, tz=None):
            return date

    return MockDateTime


########################################################################
def make_mock_date(date):
    ####################################################################
    class MockDate(with_metaclass(instance_check(datetime.date), datetime.date)):
        ################################################################
        @classmethod
        def today(cls):
            return date

    return MockDate


########################################################################
def make_mock_date_time_module(datetime_to_use, date_to_use=None):
    ####################################################################
    class MockDateTimeModule(object):
        pass

    MockDateTimeModule.datetime = make_mock_date_time(datetime_to_use)
    MockDateTimeModule.date = make_mock_date(date_to_use or datetime_to_use.date())
    MockDateTimeModule.timedelta = datetime.timedelta

    return MockDateTimeModule

