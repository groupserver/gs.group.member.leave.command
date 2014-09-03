# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
from email.utils import parseaddr
from zope.component import createObject
from gs.group.list.command import CommandResult, CommandABC
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .leaver import GroupLeaver


class LeaveCommand(CommandABC):
    'The ``unsubscribe`` command.'

    def process(self, email, request):
        'Process the email command ``unsubscribe``'
        components = self.get_command_components(email)
        if components[0] != 'unsubscribe':
            m = 'Not a unsubscribe command: {0}'.format(email['Subject'])
            raise ValueError(m)

        retval = CommandResult.notACommand
        if (len(components) == 1):
            self.leave(email)
            retval = CommandResult.commandStop
        return retval

    def leave(self, email):
        userInfo = self.get_user(email)
        if userInfo:
            groupInfo = createObject('groupserver.GroupInfo', self.group)
            # TODO: Create a notification. This has to be done *before* the
            #       member leaves the group, or a big fat permission denied
            #       error will be raised.
            leaver = GroupLeaver(groupInfo, userInfo)
            leaver.removeMember()

    def get_user(self, email):
        retval = None
        addr = parseaddr(email['From'])[1]
        sr = self.group.site_root()
        user = sr.acl_users.get_userByEmail(addr)
        if user:
            retval = IGSUserInfo(user)
        return retval
