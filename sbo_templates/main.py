#! /usr/bin/python
# -*- coding: utf-8 -*-

# main.py file is part of sbo-templates.

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

from __future__ import unicode_literals
import os
import sys
import locale
from dialog import Dialog
from __metadata__ import __version__

locale.setlocale(locale.LC_ALL, '')


class SBoTemplates(object):
    """SlackBuild Templates Class
    """
    def __init__(self):
        self.d = Dialog(dialog="dialog")
        self.d.set_background_title("SlackBuild.org Templates {0}".format(
            __version__))
        self.args = sys.argv
        self.args.pop(0)
        self.__cli()
        self.__templatesInit()

    def __cli(self):
        """command line interface
        """
        if len(self.args) > 1:
            self.__usage()
        elif len(self.args) == 1 and self.args[0] == "--help":
            self.__usage()
        elif len(self.args) == 1 and self.args[0] == "--version":
            self.__version()
        elif len(self.args) < 1:
            self.args = ['application']

    def __version(self):
        """version info
        """
        print("Version: {0}".format(__version__))
        sys.exit(0)

    def __usage(self):
        """optional arguments
        """
        args = [
            "Usage: sbo-templates <application>\n",
            "Optional arguments:",
            "  --help           display this help and exit",
            "  --version        print version and exit",
        ]
        for opt in args:
            print("{0}".format(opt))
        sys.exit(0)

    def __templatesInit(self):
        """Initialiazation templates data
        """
        self.filename = ""
        self.msg = ""
        self.data = []
        self.height = 30
        self.width = 80
        self.app = self.args[0]
        self.handy_ruler = 1
        self.__slackDescComments()
        self.maintainer = ""
        self.email = ""
        self.HOME = os.getenv("HOME") + "/"
        self.filename = "{0}.sbo-maintainer".format(self.HOME)
        self.__maintainerInit()
        self.choises = [
            ("1 Info", "Create {0}.info file".format(self.app)),
            ("2 Slack desc", "Create slack-desc file"),
            ("3 Desktop", "Create {0}.desktop file".format(self.app)),
            ("4 Maintainer", "Maintainer data"),
            ("0 Exit", "Exit the program")
        ]

    def __maintainerInit(self):
        """Initialization maintainer data
        """
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as f:
                r = f.read()
                for line in r.splitlines():
                    if line.startswith("MAINTAINER"):
                        self.maintainer = line.split("=")[1]
                    if line.startswith("EMAIL"):
                        self.email = line.split("=")[1]

    def menu(self):
        """Dialog.menu(text, height=None, width=None, menu_height=None,
        choices=[], **kwargs)
        Display a menu dialog box.
        """
        code, tag = self.d.menu("Choose an option or press ESC or <Cancel> to "
                                "Exit.", height=15, width=70,
                                menu_height=len(self.choises),
                                choices=self.choises)
        if code == self.d.CANCEL or code == self.d.ESC or tag[0] == "0":
            os.system("clear")
            sys.exit(0)
        if tag[0] == "1":
            self.infoFile()
        elif tag[0] == "2":
            self.slackDesc()
        elif tag[0] == "3":
            self.desktopFile()
        elif tag[0] == "4":
            self.maintainerData()

    def mixedform(self):
        """Dialog.mixedform(text, elements, height=0, width=0, form_height=0,
        **kwargs)
        Display a form consisting of labels and fields.
        """
        self.code, self.fields = self.d.mixedform(self.comments, self.elements,
                                                  self.height, self.width)

    def maintainerData(self):
        """Maintainer data handler
        """
        self.filename = "{0}.sbo-maintainer".format(self.HOME)
        self.comments = self.filename
        self.width = 90
        field_length = 90
        input_length = 90
        attributes = '0x0'
        text = ["MAINTAINER=", "EMAIL="]
        self.elements = [
            (text[0], 1, 1, self.maintainer, 1, 12, field_length, input_length,
             attributes),
            (text[1], 2, 1, self.email, 2, 7, field_length, input_length,
             attributes)
        ]
        self.mixedform()
        if self.fields:
            self.maintainer = self.fields[0]
            self.email = self.fields[1]
        for item, line in zip(text, self.fields):
            self.data.append(item + line)
        self.choose()

    def __slackDescComments(self):
        """slack-desc file comments
        """
        self.comments = (
            "# HOW TO EDIT THIS FILE:\n"
            '# The "handy ruler" below makes it easier to edit a package '
            'description.\n'
            "# Line up the first '|' above the ':' following the base package "
            "name, and\n"
            "# the '|' on the right side marks the last column you can put a "
            "character in.\n"
            "# You must make exactly 11 lines for the formatting to be correct"
            ".  It's also\n"
            "# customary to leave one space after the ':' except on otherwise "
            "blank lines.\n\n"
            "{0}|-----handy-ruler---------------------------------------------"
            "---------|".format(' ' * (len(self.app) + self.handy_ruler))
        )

    def slackDesc(self):
        """slack-desc file handler
        """
        self.__slackDescComments()
        self.filename = "slack-desc"
        self.width = 80 + len(self.app)
        field_length = 70
        input_length = 70
        attributes = '0x0'
        self.elements = [
            ("{0}:".format(self.app), 1, 1, ' {0} ()'.format(self.app), 1,
             len(self.app) + 2, field_length, input_length, attributes),
            ("{0}:".format(self.app), 2, 1, '', 2, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 3, 1, '', 3, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 4, 1, '', 4, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 5, 1, '', 5, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 6, 1, '', 6, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 7, 1, '', 7, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 8, 1, '', 8, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 9, 1, '', 9, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 10, 1, '', 10, len(self.app) + 2,
             field_length, input_length, attributes),
            ("{0}:".format(self.app), 11, 1, '', 11, len(self.app) + 2,
             field_length, input_length, attributes)
        ]
        self.mixedform()
        self.handy_ruler = 0
        self.__slackDescComments()
        for line in self.comments.splitlines():
            self.data.append(line)
        for line in self.fields:
            self.data.append("{0}:{1}".format(self.app, line))
        self.choose()

    def infoFile(self):
        """<application>.info file handler
        """
        self.filename = "{0}.info".format(self.app)
        self.width = 90
        self.comments = self.filename
        field_length = 90
        input_length = 90
        attributes = '0x0'
        text = ["PRGNAM=", "VERSION=", "HOMEPAGE=", "DOWNLOAD=", "MD5SUM=",
                "DOWNLOAD_x86_64=", "MD5SUM_x86_64=", "REQUIRES=",
                "MAINTAINER=", "EMAIL="]
        self.elements = [
            (text[0], 1, 1, '"{0}"'.format(self.app), 1, 8, field_length,
             input_length, attributes),
            (text[1], 2, 1, '""', 2, 9, field_length, input_length,
             attributes),
            (text[2], 3, 1, '""', 3, 10, field_length * 4, input_length * 4,
             attributes),
            (text[3], 4, 1, '""', 4, 10, field_length * 4, input_length * 4,
             attributes),
            (text[4], 5, 1, '""', 5, 8, field_length + 8, input_length + 8,
             attributes),
            (text[5], 6, 1, '""', 6, 17, field_length * 4,
             input_length * 4, attributes),
            (text[6], 7, 1, '""', 7, 15, field_length * 4,
             input_length * 4, attributes),
            (text[7], 8, 1, '""', 8, 10, field_length * 4, input_length * 4,
             attributes),
            (text[8], 9, 1, '"{0}"'.format(self.maintainer), 9, 12,
             field_length, input_length, attributes),
            (text[9], 10, 1, '"{0}"'.format(self.email), 10, 7, field_length,
             input_length, attributes)
        ]
        self.mixedform()
        for item, line in zip(text, self.fields):
            self.data.append(item + line)
        self.choose()

    def desktopFile(self):
        """<application>.desktop file handler
        """
        self.filename = "{0}.desktop".format(self.app)
        self.width = 90
        self.comments = self.filename
        field_length = 90
        input_length = 90
        attributes = '0x0'
        text = ["[Desktop Entry]", "Name=", "Comment=", "Exec=", "Icon=",
                "Terminal=", "Type=", "Categories=", "GenericName="]
        self.elements = [
            (text[0], 1, 1, '', 1, 1, field_length, input_length, 0x1),
            (text[1], 2, 1, '{0}'.format(self.app), 2, 6, field_length,
             input_length, attributes),
            (text[2], 3, 1, '', 3, 9, field_length * 4, input_length * 4,
             attributes),
            (text[3], 4, 1, '/usr/bin/{0}'.format(self.app), 4, 6,
             field_length * 4, input_length * 4, attributes),
            (text[4], 5, 1, '/usr/share/pixmaps/{0}.png'.format(self.app), 5, 6,
             field_length + 8, input_length + 8, attributes),
            (text[5], 6, 1, 'false', 6, 10, field_length * 4,
             input_length * 4, attributes),
            (text[6], 7, 1, '', 7, 6, field_length * 4,
             input_length * 4, attributes),
            (text[7], 8, 1, '', 8, 12, field_length * 4, input_length * 4,
             attributes),
            (text[8], 9, 1, '', 9, 13, field_length, input_length,
             attributes),
        ]
        self.mixedform()
        for item, line in zip(text, self.fields):
            self.data.append(item + line)
        self.choose()

    def messageBox(self):
        self.d.msgbox(self.msg, width=50, height=7)

    def choose(self):
        """Choosing if write to file or exit
        """
        if self.code == self.d.OK:
            self.write()
            self.msg = "File {0} is created.".format(self.filename)
            self.messageBox()
            self.__templatesInit()  # reset all data after write
            self.menu()
        elif self.code == self.d.CANCEL:
            self.__templatesInit()  # reset all data after browse
            self.menu()
        elif self.code == self.d.ESC:
            self.__templatesInit()  # reset all data after browse
            self.menu()

    def write(self):
        """write handler
        """
        with open(self.filename, "w") as f:
            for line in self.data:
                f.write(line + "\n")


def main():

    SBoTemplates().menu()

if __name__ == "__main__":
    main()
