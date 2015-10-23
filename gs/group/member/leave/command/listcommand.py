# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from email.utils import parseaddr
from zope.component import createObject
from gs.group.list.command import CommandResult, CommandABC
from gs.group.member.base import user_member_of_group
from gs.group.member.leave.base import leave_group
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .audit import (LeaveAuditor, LEAVE_COMMAND, LEAVE_COMMAND_NOT_MEMBER,
                    LEAVE_COMMAND_NO_PROFILE, )
from .notifier import (NotMemberNotifier, NoProfileNotifier)


class LeaveCommand(CommandABC):
    'The ``unsubscribe`` command.'

    def process(self, email, request):
        'Process the email command ``unsubscribe``'
        components = self.get_command_components(email)
        if components[0] != 'unsubscribe':
            m = 'Not a unsubscribe command: {0}'.format(email['Subject'])
            raise ValueError(m)
        addr = self.get_email_addr(email)

        retval = CommandResult.notACommand
        if (len(components) == 1):
            userInfo = self.get_user(email)  # May be None. The auditor will deal.
            auditor = LeaveAuditor(self.group, userInfo, self.groupInfo)
            if userInfo:
                if user_member_of_group(userInfo, self.groupInfo):
                    auditor.info(LEAVE_COMMAND, addr)
                    leave_group(self.groupInfo, userInfo, request)
                else:  # Not a member
                    auditor.info(LEAVE_COMMAND_NOT_MEMBER, addr)
                    context = self.group.aq_parent
                    notifier = NotMemberNotifier(context, request)
                    notifier.notify(self.groupInfo, userInfo, addr)
            else:  # No profile
                auditor.info(LEAVE_COMMAND_NO_PROFILE, addr)
                context = self.group.aq_parent
                notifier = NoProfileNotifier(context, request)
                notifier.notify(self.groupInfo, addr)
            retval = CommandResult.commandStop
        return retval

    @property
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.group)
        return retval

    @staticmethod
    def get_email_addr(emailMessage):
        retval = parseaddr(emailMessage['From'])[1]
        return retval

    def get_user(self, email):
        retval = None
        sr = self.group.site_root()
        addr = self.get_email_addr(email)
        user = sr.acl_users.get_userByEmail(addr)
        if user:
            retval = IGSUserInfo(user)
        return retval
