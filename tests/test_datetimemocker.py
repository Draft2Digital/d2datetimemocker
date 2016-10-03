# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
from unittest import TestCase

import pytz

from datetimemocker.datetimemocker import DateTimeMocker
from . import datetimemocker_examples as example


########################################################################
class TestDateTimeMocker(TestCase):
    ####################################################################
    @classmethod
    def setUpClass(cls):
        cls.datetime_to_use = datetime.datetime(2016, 1, 1, tzinfo=pytz.UTC)
        cls.date_to_use = cls.datetime_to_use.date()

    ####################################################################
    def setUp(self):
        self.pre_now = datetime.datetime.now(tz=pytz.UTC)

    ####################################################################
    def test_now__with_datetime_to_use(self):
        """If datetime obj is passed in for 'datetime_to_use' argument,
        the datetime.datetime.now() function should return
        the datetime_to_use object instead.
        """
        # mocked
        with DateTimeMocker(modules=[example], datetime_to_use=self.datetime_to_use):
            self.assertEqual(self.datetime_to_use, example.now())
            self.assertGreater(self.pre_now, example.now())

        # not mocked
        self.assertGreater(example.now(), self.datetime_to_use)
        self.assertGreater(example.now(), self.pre_now)

    ####################################################################
    def test_now__with_date_to_use(self):
        """If date obj is passed in for 'date_to_use' argument,
        the datetime.datetime.now() function should return
        the current value for datetime.datetime.now(), replaced with
        the mock date values (year, month, day).
        """
        # mocked
        with DateTimeMocker(modules=[example], date_to_use=self.date_to_use):
            self.assertEqual(self.date_to_use, example.today())
            self.assertGreater(self.pre_now, example.now())
            self.assertGreater(example.now(), self.datetime_to_use.replace(hour=self.pre_now.hour,
                                                                           minute=self.pre_now.minute,
                                                                           second=self.pre_now.second,
                                                                           microsecond=self.pre_now.microsecond))

        # not mocked
        self.assertGreater(example.now(), self.datetime_to_use)
        self.assertGreater(example.now(), self.pre_now)

    ####################################################################
    def test_today__with_datetime_to_use(self):
        """If datetime obj is passed in for 'datetime_to_use' argument,
        the datetime.date.today() function should return
        the today() value of the passed in datetime obj.
        """
        # mocked
        with DateTimeMocker(modules=[example], datetime_to_use=self.datetime_to_use):
            self.assertEqual(self.datetime_to_use.date(), example.today())
            self.assertGreater(self.pre_now.date(), example.today())

        # not mocked
        self.assertNotEqual(self.datetime_to_use.date(), example.today())
        self.assertEqual(example.today(), datetime.date.today())

    ####################################################################
    def test_today__with_date_to_use(self):
        """If date obj is passed in for 'date_to_use' argument,
        the datetime.date.today() function should return
        the today() value of the passed in datetime obj.
        """
        # mocked
        with DateTimeMocker(modules=[example], date_to_use=self.date_to_use):
            self.assertEqual(self.date_to_use, example.today())
            self.assertGreater(self.pre_now.date(), example.today())

        # not mocked
        self.assertNotEqual(self.date_to_use, example.today())
        self.assertEqual(datetime.date.today(), example.today())

    ####################################################################
    def test_timedelta__with_datetime_to_use(self):
        """The timedelta method should be unaffected when mocked. The returned object
        should be identical whether mocked or not.
        """
        # set up a couple of datetime objects and timedelta objects to test
        expected = self.datetime_to_use - datetime.timedelta(days=1, hours=5, seconds=30)

        other_dt_obj = datetime.datetime(1982, 7, 8, 8, 7, tzinfo=pytz.UTC)
        other_expected = other_dt_obj - datetime.timedelta(days=9, hours=2, seconds=1)

        # mocked with datetime_to_use
        with DateTimeMocker(modules=[example], datetime_to_use=self.datetime_to_use):
            self.assertEqual(expected, example.timedelta(self.datetime_to_use, days=1, hours=5, seconds=30))
            self.assertEqual(other_expected, example.timedelta(other_dt_obj, days=9, hours=2, seconds=1))

        # not mocked
        self.assertEqual(expected, example.timedelta(self.datetime_to_use, days=1, hours=5, seconds=30))
        self.assertEqual(other_expected, example.timedelta(other_dt_obj, days=9, hours=2, seconds=1))

    ####################################################################
    def test_timedelta__date_to_use(self):
        """The timedelta method should be unaffected when mocked. The returned object
        should be identical whether mocked or not.
        """
        # set up a couple of datetime objects and timedelta objects to test
        expected = self.datetime_to_use - datetime.timedelta(days=1, hours=5, seconds=30)

        other_dt_obj = datetime.datetime(1982, 7, 8, 8, 7, tzinfo=pytz.UTC)
        other_expected = other_dt_obj - datetime.timedelta(days=9, hours=2, seconds=1)

        # mocked with date_to_use
        with DateTimeMocker(modules=[example], date_to_use=self.date_to_use):
            self.assertEqual(expected, example.timedelta(self.datetime_to_use, days=1, hours=5, seconds=30))
            self.assertEqual(other_expected, example.timedelta(other_dt_obj, days=9, hours=2, seconds=1))

        # not mocked
        self.assertEqual(expected, example.timedelta(self.datetime_to_use, days=1, hours=5, seconds=30))
        self.assertEqual(other_expected, example.timedelta(other_dt_obj, days=9, hours=2, seconds=1))

    ####################################################################
    def test_specific_date(self):
        """Non-relative dates should be unaffected by mock. If a datetime object is
        constructed using datetime.datetime(), it should not be changed by DateTimeMocker.
        """
        expected = datetime.datetime(2016, 5, 15, 12, 0, 0, tzinfo=pytz.UTC)

        # mocked
        with DateTimeMocker(modules=[example], datetime_to_use=self.datetime_to_use):
            self.assertEqual(expected, example.generate_datetime(2016, 5, 15, 12, 0, 0, pytz.UTC))

        # not mocked
        self.assertEqual(expected, example.generate_datetime(2016, 5, 15, 12, 0, 0, pytz.UTC))
