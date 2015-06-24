# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, print_function, unicode_literals
from email.parser import Parser
from gs.group.list.command.tests.faux import FauxGroup  # lint:ok


class FauxSiteInfo(object):
    name = 'An Example Site'
    id = b'example'


class FauxGroupInfo(object):
    name = 'An Example Group'
    id = b'example_group'
    url = 'https://lists.example.com/groups/example_group'
    siteInfo = FauxSiteInfo()
    groupObj = 'This is not a folder'
    aq_parent = "This is not the parent"


class FauxUserInfo(object):
    name = 'An Example user'
    id = b'exampleuser'


class FauxVisibility(object):
    groupInfo = FauxGroupInfo()


def faux_email(subject='leave'):
    retval = Parser().parsestr(
        b'From: <member@example.com>\n'
        b'To: <group@example.com>\n'
        b'Subject: {0}\n'
        b'\n'
        b'Body would go here\n'.format(subject))
    return retval
