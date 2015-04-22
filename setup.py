#! /usr/bin/python
# -*- coding: utf-8 -*-

# setup.py file is part of sbo-templates.

# Copyright 2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# SBo tool for managing templates.

# https://github.com/dslackw/sbo-templates

# sbo-templates is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from sbo_templates.__metadata__ import (
    __prog__,
    __version__,
    __author__,
    __email__,
    __website__,
)

setup(
    name=__prog__,
    packages=["sbo_templates"],
    scripts=["bin/sbo-templates"],
    version=__version__,
    description="SBo tool for managing templates.",
    keywords=["sbo", "templates", "slackbuild"],
    author=__author__,
    author_email=__email__,
    url=__website__,
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    install_requires=['python2-pythondialog>=3.2.2'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Classifier: Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later "
        "(GPLv3+)",
        "Classifier: Operating System :: Unix",
        "Classifier: Programming Language :: Python",
        "Classifier: Programming Language :: Python :: 2.5",
        "Classifier: Programming Language :: Python :: 2.6",
        "Classifier: Programming Language :: Python :: 2.7",
        ],
    long_description=open("README.rst").read()
)
