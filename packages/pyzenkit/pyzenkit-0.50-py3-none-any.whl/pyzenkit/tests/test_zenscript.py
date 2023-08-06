#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of PyZenKit package.
#
# Copyright (C) since 2016 CESNET, z.s.p.o (http://www.ces.net/)
# Copyright (C) since 2015 Honza Mach <honza.mach.ml@gmail.com>
# Use of this package is governed by the MIT license, see LICENSE file.
#
# This project was initially written for personal use of the original author. Later
# it was developed much further and used for project of author`s employer.
#-------------------------------------------------------------------------------


"""
Unit test module for testing the :py:mod:`pyzenkit.zenscript` module.
"""

__author__ = "Honza Mach <honza.mach.ml@gmail.com>"


import unittest

import os
import shutil
import datetime

import pyzenkit.baseapp
import pyzenkit.zenscript


#
# Global variables
#
SCR_NAME      = 'test-zenscript.py'              # Name of the script process
CFG_FILE_NAME = '/tmp/{}.conf'.format(SCR_NAME)  # Name of the script configuration file
CFG_DIR_NAME  = '/tmp/{}'.format(SCR_NAME)       # Name of the script configuration directory


class TestPyzenkitZenScript(unittest.TestCase):
    """
    Unit test class for testing the :py:class:`pyzenkit.zenscript.ZenScript` class.
    """

    def setUp(self):
        pyzenkit.baseapp.BaseApp.json_save(CFG_FILE_NAME, {'test': 'x'})
        try:
            os.mkdir(CFG_DIR_NAME)
        except FileExistsError:
            pass

        self.obj = pyzenkit.zenscript.DemoZenScript(
            name        = SCR_NAME,
            description = 'TestZenScript - Testing script'
        )
    def tearDown(self):
        os.remove(CFG_FILE_NAME)
        shutil.rmtree(CFG_DIR_NAME)

    def test_01_plugin(self):
        """
        Perform the basic operativity tests.
        """
        self.maxDiff = None

        self.obj.plugin()

    def test_02_calc_int_thrs(self):
        """
        Perform tests of interval thresholds calculations.
        """
        self.maxDiff = None

        self.obj.plugin()

        # Test the interval threshold calculations
        timestamps_utc = [
            1454934691,
            '2016-02-08T12:31:31Z',
            datetime.datetime.utcfromtimestamp(1454934691),
        ]
        self.assertEqual(timestamps_utc[2].isoformat(), '2016-02-08T12:31:31')

        for ts_utc in timestamps_utc:
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = 'daily'),
                (datetime.datetime(2016, 2, 7, 12, 31, 31), datetime.datetime(2016, 2, 8, 12, 31, 31))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = 'daily', adjust = True),
                (datetime.datetime(2016, 2, 7, 1, 0), datetime.datetime(2016, 2, 8, 1, 0))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '12_hourly', adjust = True),
                (datetime.datetime(2016, 2, 7, 13, 0), datetime.datetime(2016, 2, 8, 1, 0))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '6_hourly', adjust = True),
                (datetime.datetime(2016, 2, 8, 1, 0), datetime.datetime(2016, 2, 8, 7, 0))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '4_hourly', adjust = True),
                (datetime.datetime(2016, 2, 8, 5, 0), datetime.datetime(2016, 2, 8, 9, 0))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '3_hourly', adjust = True),
                (datetime.datetime(2016, 2, 8, 7, 0), datetime.datetime(2016, 2, 8, 10, 0))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '2_hourly', adjust = True),
                (datetime.datetime(2016, 2, 8, 9, 0), datetime.datetime(2016, 2, 8, 11, 0))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = 'hourly', adjust = True),
                (datetime.datetime(2016, 2, 8, 11, 0), datetime.datetime(2016, 2, 8, 12, 0))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '30_minutes', adjust = True),
                (datetime.datetime(2016, 2, 8, 12, 0), datetime.datetime(2016, 2, 8, 12, 30))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '20_minutes', adjust = True),
                (datetime.datetime(2016, 2, 8, 12, 0), datetime.datetime(2016, 2, 8, 12, 20))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '15_minutes', adjust = True),
                (datetime.datetime(2016, 2, 8, 12, 15), datetime.datetime(2016, 2, 8, 12, 30))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '10_minutes', adjust = True),
                (datetime.datetime(2016, 2, 8, 12, 20), datetime.datetime(2016, 2, 8, 12, 30))
            )
            self.assertEqual(
                self.obj.calculate_interval_thresholds(time_high = ts_utc, interval = '5_minutes', adjust = True),
                (datetime.datetime(2016, 2, 8, 12, 25), datetime.datetime(2016, 2, 8, 12, 30))
            )

    def test_03_calc_upper_thrs(self):
        """
        Perform tests of upper threshold calculations.
        """
        self.maxDiff = None

        self.obj.plugin()

        # Test the interval threshold calculations
        timestamps_utc = [
            1454934691,
            '2016-02-08T12:31:31Z',
            datetime.datetime.utcfromtimestamp(1454934691),
        ]
        self.assertEqual(timestamps_utc[2].isoformat(), '2016-02-08T12:31:31')

        for ts_utc in timestamps_utc:
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = 'daily'),
                datetime.datetime(2016, 2, 8, 12, 31, 31)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = 'daily', adjust = True),
                datetime.datetime(2016, 2, 8, 1, 0)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '12_hourly', adjust = True),
                datetime.datetime(2016, 2, 8, 1, 0)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '6_hourly', adjust = True),
                datetime.datetime(2016, 2, 8, 7, 0)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '4_hourly', adjust = True),
                datetime.datetime(2016, 2, 8, 9, 0)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '3_hourly', adjust = True),
                datetime.datetime(2016, 2, 8, 10, 0)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '2_hourly', adjust = True),
                datetime.datetime(2016, 2, 8, 11, 0)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = 'hourly', adjust = True),
                datetime.datetime(2016, 2, 8, 12, 0)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '30_minutes', adjust = True),
                datetime.datetime(2016, 2, 8, 12, 30)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '20_minutes', adjust = True),
                datetime.datetime(2016, 2, 8, 12, 20)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '15_minutes', adjust = True),
                datetime.datetime(2016, 2, 8, 12, 30)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '10_minutes', adjust = True),
                datetime.datetime(2016, 2, 8, 12, 30)
            )
            self.assertEqual(
                self.obj.calculate_upper_threshold(time_high = ts_utc, interval = '5_minutes', adjust = True),
                datetime.datetime(2016, 2, 8, 12, 30)
            )


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
