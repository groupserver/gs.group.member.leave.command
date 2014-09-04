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
from .leaver import GroupLeaver
from .notifier import LeaveNotifier, LeftNotifier


def leave_group(groupInfo, userInfo, request):
    '''Leave the group sending the appropriate notifications

:param groupInfo: The group that the person is leaving.
:type groupInfo: :class:`Products.GSGroup.interfaces.IGSGroupInfo`
:param userInfo: The person that is leaving the group,
:type userInfo: :class:`Products.CustomUserFolder.interfaces.IGSUserInfo`
:param request: The HTTP request.
:returns: ``True`` if the person left, ``False`` otherwise.'''
    notifier = LeaveNotifier(groupInfo.groupObj, request)
    notifier.update(groupInfo, userInfo)
    adminNotifiers = []
    for admin in groupInfo.group_admins:
        if admin.id != userInfo.id:
            an = LeftNotifier(groupInfo.groupObj, request)
            an.update(groupInfo, userInfo, admin)
            adminNotifiers.append(an)

    leaver = GroupLeaver(groupInfo, userInfo)
    leaver.removeMember()

    left = not leaver.isMember
    if left:
        notifier.notify(userInfo)
        for adminNotifier in adminNotifiers:
            adminNotifier.notify()
    return left
