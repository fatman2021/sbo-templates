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
import pydoc
import locale
import hashlib
import subprocess
from datetime import date
from dialog import Dialog
from templates import (
    SlackBuilds,
    doinst
)
from __metadata__ import __version__


locale.setlocale(locale.LC_ALL, '')


class SBoTemplates(object):
    """SlackBuild Templates Class
    """
    def __init__(self):
        self.year = date.today().year
        self.d = Dialog(dialog="dialog")
        self.d.set_background_title("SlackBuild.org Templates {0}".format(
            __version__))

        self.args = sys.argv
        self.args.pop(0)
        self.__cli()

        self.source = ""
        self.chk_md5 = ""
        self.pwd = ""
        self.slack_desc_text = []
        self.slack_desc_data = []
        # appname.info
        self._version = '""'
        self._homepage = '""'
        self._download = '""'
        self._md5sum = '""'
        self._download_x86_64 = '""'
        self._md5sum_x86_64 = '""'
        self._requires = '""'
        # appname.desktop
        self._name = self.args[0]
        self._comment = ""
        self._exec = "/usr/bin/{0}".format(self.args[0])
        self._icon = "/usr/share/pixmaps/{0}.png".format(self.args[0])
        self._terminal = "false"
        self._type = ""
        self._categories = ""
        self._genericname = ""

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
            self.args = ['appname']

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
        self.live = ""
        self.editor = "nano"
        self.HOME = os.getenv("HOME") + "/"
        self.filename = "{0}.sbo-maintainer".format(self.HOME)
        self.__maintainerInit()
        self.choises = [
            ("Info", "Create {0}.info file".format(self.app)),
            ("README", "Create README file"),
            ("Desktop", "Create {0}.desktop file".format(self.app)),
            ("Doinst.sh", "Create doinst.sh script"),
            ("Slack desc", "Create slack-desc file"),
            ("SlackBuild", "Create {0}.SlackBuild script".format(self.app)),
            ("Maintainer", "Maintainer data"),
            ("Directory", "Change directory"),
            ("Help", "Where to get help"),
            ("Exit", "Exit the program")
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
                    if line.startswith("LIVE"):
                        self.live = line.split("=")[1]
                    if line.startswith("EDITOR"):
                        self.editor = line.split("=")[1]

    def menu(self):
        """Dialog.menu(text, height=None, width=None, menu_height=None,
        choices=[], **kwargs)
        Display a menu dialog box.
        """
        self.__templatesInit()  # reset all data
        code, tag = self.d.menu("Choose an option or press ESC or <Cancel> to "
                                "Exit.", height=15, width=70,
                                menu_height=len(self.choises),
                                choices=self.choises)
        if code == self.d.CANCEL or code == self.d.ESC or tag[0] == "0":
            os.system("clear")
            sys.exit(0)
        case = {
            "Info": self.infoFile,
            "Slack desc": self.slackDesc,
            "Desktop": self.desktopFile,
            "Doinst.sh": self.doinst_sh,
            "SlackBuild": self.SlackBuild,
            "README": self.README,
            "Maintainer": self.maintainerData,
            "Directory": self.__updateDirectory,
            "Help": self.getHelp,
            "Exit": self.exit,
        }
        case[tag]()

    def exit(self):
        os.system("clear")
        sys.exit(0)

    def getHelp(self):
        """get help from slackbuilds.org
        """
        self.msg = ("For additional assistance, visit: http://www.slackbuilds."
                    "org/guidelines/")
        self.width = len(self.msg) + 4
        self.height = 7
        self.messageBox()
        self.menu()

    def __updateDirectory(self):
        """update working direcroty
        """
        self.height = 10
        self.comments = "Current directory: {0}".format(self.pwd)
        field_length = 90
        input_length = 90
        attributes = '0x0'
        self.elements = [
            ("Directory=", 1, 1, "", 1, 11, field_length, input_length,
             attributes),
        ]
        self.mixedform()
        if self.fields:
            self.pwd = self.fields[0].strip()
            if self.pwd and not self.pwd.endswith("/"):
                self.pwd = self.pwd + "/"
            self.width = 60
            self.height = 6
            self.msg = "Current directory: {0}".format(self.pwd)
            self.messageBox()
        self.menu()

    def maintainerData(self):
        """Maintainer data handler
        """
        cache_dir = self.pwd
        self.pwd = ""
        self.height = 15
        self.filename = "{0}.sbo-maintainer".format(self.HOME)
        self.comments = ("Enter the details of the maintainer and change "
                         "editor, \ndefault is 'nano'.")
        self.width = 90
        field_length = 90
        input_length = 90
        attributes = '0x0'
        text = ["MAINTAINER=", "EMAIL=", "LIVE=", "EDITOR="]
        self.elements = [
            (text[0], 1, 1, self.maintainer, 1, 12, field_length, input_length,
             attributes),
            (text[1], 2, 1, self.email, 2, 7, field_length, input_length,
             attributes),
            (text[2], 3, 1, self.live, 3, 6, field_length, input_length,
             attributes),
            (text[3], 4, 1, self.editor, 4, 8, field_length, input_length,
             attributes)
        ]
        self.mixedform()
        if self.fields:
            self.maintainer = self.fields[0]
            self.email = self.fields[1]
            self.live = self.fields[2]
            self.editor = self.fields[3]
        for item, line in zip(text, self.fields):
            self.data.append(item + line)
        self.choose()
        self.pwd = cache_dir

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
        self.elements = []
        self.__slackDeskRead()
        if not self.slack_desc_data[0]:     # check description
            self.elements = [
                ("{0}:".format(self.app), 1, 1, ' {0} ()'.format(self.app), 1,
                 len(self.app) + 2, field_length, input_length, attributes)
            ]
        for i, line in zip(range(2, 12), self.slack_desc_data):
            self.elements += [("{0}:".format(self.app), i, 1, line, i,
                               len(self.app) + 2, field_length, input_length,
                               attributes)]
        self.mixedform()
        self.handy_ruler = 0
        self.__slackDescComments()
        for line in self.comments.splitlines():
            self.data.append(line)
        for line in self.fields:
            if line:
                self.slack_desc_text.append("{0}".format(line.strip()))
            self.data.append("{0}:{1}".format(self.app, line))
        self.slack_desc_text = self.slack_desc_text[1:]
        self.choose()

    def __slackDeskRead(self):
        """grab slack-desc text if exist
        """
        line_count = 0
        if os.path.isfile(self.pwd + self.filename):
            with open(self.pwd + self.filename, "r") as info:
                for line in info:
                    line_count += 1
                    if line_count > 8 and line_count < 20:
                        self.slack_desc_data.append(
                            line[len(self.app) + 1:].rstrip())
        else:
            self.slack_desc_data = [""] * 11

    def infoFile(self):
        """<application>.info file handler
        """
        self.filename = "{0}.info".format(self.app)
        self.width = 90
        self.height = 20
        self.comments = self.filename
        field_length = 90
        input_length = 90
        attributes = '0x0'
        text = ["PRGNAM=", "VERSION=", "HOMEPAGE=", "DOWNLOAD=", "MD5SUM=",
                "DOWNLOAD_x86_64=", "MD5SUM_x86_64=", "REQUIRES=",
                "MAINTAINER=", "EMAIL="]
        self.__infoFileRead(text)
        self.elements = [
            (text[0], 1, 1, '"{0}"'.format(self.app), 1, 8, field_length,
             input_length, attributes),
            (text[1], 2, 1, self._version, 2, 9, field_length, input_length,
             attributes),
            (text[2], 3, 1, self._homepage, 3, 10, field_length * 4,
             input_length * 4, attributes),
            (text[3], 4, 1, self._download, 4, 10, field_length * 4,
             input_length * 4, attributes),
            (text[4], 5, 1, self._md5sum, 5, 8, field_length + 8,
             input_length + 8, attributes),
            (text[5], 6, 1, self._download_x86_64, 6, 17, field_length * 4,
             input_length * 4, attributes),
            (text[6], 7, 1, self._md5sum_x86_64, 7, 15, field_length * 4,
             input_length * 4, attributes),
            (text[7], 8, 1, self._requires, 8, 10, field_length * 4,
             input_length * 4, attributes),
            (text[8], 9, 1, '"{0}"'.format(self.maintainer), 9, 12,
             field_length, input_length, attributes),
            (text[9], 10, 1, '"{0}"'.format(self.email), 10, 7, field_length,
             input_length, attributes)
        ]
        self.mixedform()
        if self.fields:
            self._version = self.fields[1]
            self._homepage = self.fields[2]
            self._download = self.fields[3]
            self._md5sum = self.fields[4]
            if self._download:
                self.source = self._download.replace('"', '').split("/")[-1]
                self.chk_md5 = self._md5sum
                self.checksum()
            self._download_x86_64 = self.fields[5]
            self._md5sum_x86_64 = self.fields[6]
            if self._download_x86_64:
                self.source = self._download_x86_64.replace(
                    '"', '').split("/")[-1]
                self.chk_md5 = self._md5sum_x86_64
                self.checksum()
            self._requires = self.fields[7]
        for item, line in zip(text, self.fields):
            self.data.append(item + line)
        self.choose()

    def __infoFileRead(self, text):
        """read data for <application>.info file if exist
        """
        if os.path.isfile(self.pwd + self.filename):
            with open(self.pwd + self.filename, "r") as info:
                for line in info:
                    fd = line.split("=")[1].strip()
                    if line.startswith(text[1]):
                        self._version = fd
                    if line.startswith(text[2]):
                        self._homepage = fd
                    if line.startswith(text[3]):
                        self._download = fd
                    if line.startswith(text[4]):
                        self._md5sum = fd
                    if line.startswith(text[5]):
                        self._download_x86_64 = fd
                    if line.startswith(text[6]):
                        self._md5sum_x86_64 = fd
                    if line.startswith(text[7]):
                        self._requires = fd

    def desktopFile(self):
        """<application>.desktop file handler
        """
        self.filename = "{0}.desktop".format(self.app)
        self.width = 90
        self.height = 20
        self.comments = self.filename
        field_length = 90
        input_length = 90
        attributes = '0x0'
        text = ["[Desktop Entry]", "Name=", "Comment=", "Exec=", "Icon=",
                "Terminal=", "Type=", "Categories=", "GenericName="]
        self.__desktopFileRead(text)
        self.elements = [
            (text[0], 1, 1, '', 1, 1, field_length, input_length, 0x1),
            (text[1], 2, 1, self._name, 2, 6, field_length,
             input_length, attributes),
            (text[2], 3, 1, self._comment, 3, 9, field_length, input_length,
             attributes),
            (text[3], 4, 1, self._exec, 4, 6, field_length, input_length,
             attributes),
            (text[4], 5, 1, self._icon, 5, 6, field_length, input_length,
             attributes),
            (text[5], 6, 1, self._terminal, 6, 10, field_length, input_length,
             attributes),
            (text[6], 7, 1, self._type, 7, 6, field_length, input_length,
             attributes),
            (text[7], 8, 1, self._categories, 8, 12, field_length, input_length,
             attributes),
            (text[8], 9, 1, self._genericname, 9, 13, field_length,
             input_length, attributes),
        ]
        self.mixedform()
        if self.fields:
            self._name = self.fields[1]
            self._comment = self.fields[2]
            self._exec = self.fields[3]
            self._icon = self.fields[4]
            self._terminal = self.fields[5]
            self._type = self.fields[6]
            self._categories = self.fields[7]
            self._genericname = self.fields[8]
        for item, line in zip(text, self.fields):
            self.data.append(item + line)
        self.choose()

    def __desktopFileRead(self, text):
        """read data for <application>.info file if exist
        """
        if os.path.isfile(self.pwd + self.filename):
            with open(self.pwd + self.filename, "r") as info:
                for line in info:
                    if line.startswith(text[1]):
                        self._name = line.split("=")[1].strip()
                    if line.startswith(text[2]):
                        self._comment = line.split("=")[1].strip()
                    if line.startswith(text[3]):
                        self._exec = line.split("=")[1].strip()
                    if line.startswith(text[4]):
                        self._icon = line.split("=")[1].strip()
                    if line.startswith(text[5]):
                        self._terminal = line.split("=")[1].strip()
                    if line.startswith(text[6]):
                        self._type = line.split("=")[1].strip()
                    if line.startswith(text[7]):
                        self._categories = line.split("=")[1].strip()
                    if line.startswith(text[8]):
                        self._genericname = line.split("=")[1].strip()

    def doinst_sh(self):
        """doinst.sh handler file
        """
        os.system("clear")
        temp = "\n".join(doinst.splitlines())
        pydoc.pipepager(temp, cmd='less -R')
        self.filename = "doinst.sh"
        self.edit()
        self.menu()

    def README(self):
        """README handler file
        """
        self.filename = "README"
        if self.slack_desc_text:
            yesno = self.d.yesno("Import description from <slack-desc> file ?")
            if yesno == "ok":
                self.data = self.slack_desc_text
                self.write()
        self.edit()
        self.menu()

    def SlackBuild(self):
        """SlackBuild handler file
        """
        self.filename = "{0}.info".format(self.app)
        text = ["x", "VERSION="] + (["x"] * 6)
        self.__infoFileRead(text)   # get version for .info file
        self.filename = "{0}.SlackBuild".format(self.app)
        if not os.path.isfile(self.pwd + self.filename):
            version = self._version.replace('"', '')
            height = 20
            width = 80
            choices = [
                ("autotools-template", "autotools-template.SlackBuild", False),
                ("cmake-template", "cmake-template.SlackBuild", False),
                ("perl-template", "perl-template.SlackBuild", False),
                ("python-template", "python-template.SlackBuild", False),
                ("rubygem-template", "rubygem-template.SlackBuild", False)
            ]
            code, tag = self.d.radiolist("{0}".format(self.filename), height,
                                         width, list_height=0, choices=choices)
            self.msg = "{0} script created.".format(self.filename)
            self.height = 7
            self.width = len(self.msg) + 4
            if tag == "autotools-template":
                self.data = SlackBuilds(
                    self.app, version, self.year, self.maintainer,
                    self.live).autotools().splitlines()
                self.write()
                self.messageBox()
            elif tag == "cmake-template":
                self.data = SlackBuilds(
                    self.app, version, self.year, self.maintainer,
                    self.live).cmake().splitlines()
                self.write()
                self.messageBox()
            elif tag == "perl-template":
                self.data = SlackBuilds(
                    self.app, version, self.year, self.maintainer,
                    self.live).perl().splitlines()
                self.write()
                self.messageBox()
            elif tag == "python-template":
                self.data = SlackBuilds(
                    self.app, version, self.year, self.maintainer,
                    self.live).python().splitlines()
                self.write()
                self.messageBox()
            elif tag == "rubygem-template":
                self.data = SlackBuilds(
                    self.app, version, self.year, self.maintainer,
                    self.live).rubygem().splitlines()
                self.write()
                self.messageBox()
        self.edit()
        self.menu()

    def mixedform(self):
        """Dialog.mixedform(text, elements, height=0, width=0, form_height=0,
        **kwargs)
        Display a form consisting of labels and fields.
        """
        self.code, self.fields = self.d.mixedform(self.comments, self.elements,
                                                  self.height, self.width)

    def edit(self):
        """editor handler
        """
        subprocess.call([self.editor, self.pwd + self.filename])

    def messageBox(self):
        """view messages
        """
        self.d.msgbox(self.msg, self.height, self.width)

    def choose(self):
        """Choosing if write to file or exit
        """
        if self.code == self.d.OK:
            self.__ifFileExist()
            self.write()
            self.messageBox()
            self.menu()
        elif self.code == self.d.CANCEL:
            self.menu()
        elif self.code == self.d.ESC:
            self.menu()

    def __ifFileExist(self):
        """check if file exist
        """
        self.width = 60
        self.height = 6
        if os.path.isfile(self.pwd + self.filename):
            self.msg = "File {0} modified.".format(self.filename)
        else:
            self.msg = "File {0} is created.".format(self.filename)

    def checksum(self):
        """checksum sources
        """
        self.height = 7
        self.width = 90
        self.chk_md5 = "".join(self.chk_md5.replace('"', ''))
        if os.path.isfile(self.pwd + self.source):
            with open(self.pwd + self.source) as f:
                data = f.read()
                if self.chk_md5 != hashlib.md5(data).hexdigest():
                    self.msg = "MD5SUM check for {0} FAILED".format(self.source)
                    self.messageBox()
            self.infoFile()

    def touch(self):
        """create empty file
        """
        with open(self.pwd + self.filename, "w") as f:
            f.close()

    def write(self):
        """write handler
        """
        with open(self.pwd + self.filename, "w") as f:
            for line in self.data:
                f.write(line + "\n")


def main():

    SBoTemplates().menu()

if __name__ == "__main__":
    main()
