#! /usr/bin/python
# -*- coding: utf-8 -*-

# templates.py file is part of sbo-templates.

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

import urllib2

bg = "\x1b[48;5;4m"
fg = "\x1b[38;5;7m"
cl = bg + fg

try:
    doinst_sh = urllib2.urlopen("http://slackbuilds.org/templates/doinst.sh")
    doinst = doinst_sh.read()
except urllib2.URLError as err:
    doinst = str(err)
doinst_begin = [
    cl + "#####################################################################"
    "##########",
    cl + "#             COPY A TEMPLATE AND PASTE IT INTO THE TEXT EDITOR      "
    "         #",
    cl + "#                          PRESS \"q or Q\" TO EXIT                  "
    "           #",
    cl + "#####################################################################"
    "##########",
    cl + ""
]
doinst_end = [
    cl + "#####################################################################"
    "##########",
]
doinst_sh_template = doinst_begin + doinst.splitlines() + doinst_end
