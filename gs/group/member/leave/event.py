# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014 OnlineGroups.net and Contributors.
#
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
from __future__ import absolute_import, unicode_literals
from zope.component.interfaces import ObjectEvent
from zope.component.interfaces import IObjectEvent
from zope.interface import Attribute, implements


class IGSLeaveGroupEvent(IObjectEvent):
    """An event issued after someone has left a group."""
    groupInfo = Attribute('The group that is being joined')
    memberInfo = Attribute('The new group member')


class GSLeaveGroupEvent(ObjectEvent):
    implements(IGSLeaveGroupEvent)

    def __init__(self, context, groupInfo, memberInfo):
        ObjectEvent.__init__(self, context)
        self.groupInfo = groupInfo
        self.memberInfo = memberInfo
