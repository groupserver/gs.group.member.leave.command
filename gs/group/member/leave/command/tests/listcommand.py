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
from mock import patch
from unittest import TestCase
from gs.group.member.leave.command.listcommand import (LeaveCommand)
import gs.group.member.leave.command.listcommand  # lint:ok
from gs.group.list.command.result import CommandResult
from .faux import (FauxGroup, FauxGroupInfo, FauxUserInfo, faux_email)


class TestUnsubscribeCommand(TestCase):

    @patch.object(LeaveCommand, 'groupInfo')
    @patch.object(LeaveCommand, 'get_user')
    @patch.object(gs.group.member.leave.command.listcommand.LeaveAuditor,
                  'info')
    @patch.object(gs.group.member.leave.command.listcommand, 'leave_group')
    def test_member(self, lg, a, g_u, gi):
        'Test a member sending an "Unsubscribe" command'
        fauxGroup = FauxGroupInfo()
        gi.return_value = fauxGroup

        u = FauxUserInfo()
        g_u.return_value = u

        lc = LeaveCommand(fauxGroup)
        e = faux_email('Unsubscribe')
        r = lc.process(e, None)

        self.assertEqual(CommandResult.commandStop, r)
        g_u.assert_called_once_with(e)
        self.assertEqual(1, gs.group.member.leave.command.listcommand.leave_group.call_count)

    @patch.object(LeaveCommand, 'groupInfo')
    @patch.object(LeaveCommand, 'get_user')
    @patch.object(gs.group.member.leave.command.listcommand.LeaveAuditor,
                  'info')
    @patch.object(gs.group.member.leave.command.listcommand, 'leave_group')
    @patch.object(gs.group.member.leave.command.listcommand, 'NotMemberNotifier')
    def test_non_member(self, nmn, lg, a, g_u, gi):
        'Test a member sending an "Unsubscribe" command'
        fauxGroup = FauxGroupInfo()
        gi.return_value = fauxGroup
        g_u.return_value = None

        lc = LeaveCommand(fauxGroup)
        e = faux_email('Unsubscribe')
        r = lc.process(e, None)

        self.assertEqual(CommandResult.commandStop, r)
        g_u.assert_called_once_with(e)
        self.assertEqual(0, gs.group.member.leave.command.listcommand.leave_group.call_count)
