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


class Templates(object):

    def __init__(self):
        self.bg = "\x1b[48;5;4m"
        self.fg = "\x1b[38;5;7m"
        self.cl = self.bg + self.fg

    def doinst_sh(self):
        try:
            url = urllib2.urlopen("http://slackbuilds.org/templates/doinst.sh")
            doinst = url.read()
        except urllib2.URLError as err:
            doinst = str(err)
        doinst_begin = [
            self.cl + "#######################################################"
            "########################",
            self.cl + "#             COPY A TEMPLATE AND PASTE IT INTO THE TEX"
            "T EDITOR               #",
            self.cl + "#                          PRESS \"q or Q\" TO EXIT    "
            "                         #",
            self.cl + "#######################################################"
            "########################",
            self.cl + ""
        ]
        doinst_end = [
            self.cl + "#######################################################"
            "########################",
        ]
        return doinst_begin + doinst.splitlines() + doinst_end

doinst = """

config() {
  NEW="$1"
  OLD="$(dirname $NEW)/$(basename $NEW .new)"
  # If there's no config file by that name, mv it over:
  if [ ! -r $OLD ]; then
    mv $NEW $OLD
  elif [ "$(cat $OLD | md5sum)" = "$(cat $NEW | md5sum)" ]; then
    # toss the redundant copy
    rm $NEW
  fi
  # Otherwise, we leave the .new copy for the admin to consider...
}

preserve_perms() {
  NEW="$1"
  OLD="$(dirname $NEW)/$(basename $NEW .new)"
  if [ -e $OLD ]; then
    cp -a $OLD ${NEW}.incoming
    cat $NEW > ${NEW}.incoming
    mv ${NEW}.incoming $NEW
  fi
  config $NEW
}

schema_install() {
  SCHEMA="$1"
  GCONF_CONFIG_SOURCE="xml::etc/gconf/gconf.xml.defaults" \\
  chroot . gconftool-2 --makefile-install-rule \\
    /etc/gconf/schemas/$SCHEMA \\
    1>/dev/null
}

schema_install blah.schemas
preserve_perms etc/rc.d/rc.INIT.new
config etc/configfile.new

if [ -x /usr/bin/update-desktop-database ]; then
  /usr/bin/update-desktop-database -q usr/share/applications >/dev/null 2>&1
fi

if [ -x /usr/bin/update-mime-database ]; then
  /usr/bin/update-mime-database usr/share/mime >/dev/null 2>&1
fi

if [ -e usr/share/icons/hicolor/icon-theme.cache ]; then
  if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache usr/share/icons/hicolor >/dev/null 2>&1
  fi
fi

if [ -e usr/share/glib-2.0/schemas ]; then
  if [ -x /usr/bin/glib-compile-schemas ]; then
    /usr/bin/glib-compile-schemas usr/share/glib-2.0/schemas >/dev/null 2>&1
  fi
fi

# If needed -- be sure to sed @LIBDIR@ inside the build script
chroot . /usr/bin/gio-querymodules @LIBDIR@/gio/modules/ 1> /dev/null 2> /dev/null

if [ -x /usr/bin/install-info ]; then
  chroot . /usr/bin/install-info --info-dir=/usr/info /usr/info/blah.gz 2> /dev/null
fi
"""
