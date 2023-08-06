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
This module contains various handy utilities.
"""

__author__  = "Honza Mach <honza.mach.ml@gmail.com>"


import os


APP_ROOT_PATH = os.getenv('APP_ROOT_PATH', '/')


def get_resource_path(fs_path, *more_chunks):
    """
    Return filesystem path to application resource with ``APP_ROOT_PATH`` taken
    into consideration. If ``fs_path`` is absolute the ``APP_ROOT_PATH`` will
    be ignored as usual.
    """
    return os.path.join(APP_ROOT_PATH, fs_path, *more_chunks)


def get_resource_path_fr(fs_path, *more_chunks):
    """
    Force given application filesystem path to be relative to ``APP_ROOT_PATH``.
    """
    return os.path.join(APP_ROOT_PATH, fs_path.strip(os.sep), *more_chunks)
