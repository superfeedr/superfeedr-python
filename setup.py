#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2008 Nathanael C. Fritz
# All Rights Reserved
#
# This software is licensed as described in the README file,
# which you should have received as part of this distribution.
#

# from ez_setup import use_setuptools
from distutils.core import setup
import sys

# if 'cygwin' in sys.platform.lower():
#     min_version = '0.6c6'
# else:
#     min_version = '0.6a9'
#
# try:
#     use_setuptools(min_version=min_version)
# except TypeError:
#     # locally installed ez_setup won't have min_version
#     use_setuptools()
#
# from setuptools import setup, find_packages, Extension, Feature

VERSION          = '0.2'
DESCRIPTION      = 'Superfeedrpy'
LONG_DESCRIPTION = """
Superfeedrpy is a Superfeedr wrapper for SleekXMPP
SleekXMPP is an elegant Python library for XMPP (aka Jabber, Google Talk, etc).
"""

CLASSIFIERS      = [ 'Intended Audience :: Developers',
                     'License :: OSI Approved :: GPL v2.0',
                     'Programming Language :: Python',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                   ]

setup(
    name             = "superfeedrpy",
    version          = VERSION,
    description      = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    author       = 'Nathanael Fritz',
    author_email = 'fritzy [at] netflint.net',
    url          = 'http://code.google.com/p/sleekxmpp',
    license      = 'GPLv2',
    platforms    = [ 'any' ],
    packages     = [ 'superfeedrpy' ],
    requires     = [ 'sleekxmpp', 'tlslite' ],
    )

