# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from Products.GSGroupMember.groupmembershipstatus import \
    GSGroupMembershipStatus
from gs.group.member.manage.utils import removePtnCoach, removeAdmin,\
    unmoderate
from gs.group.member.manage.utils import removePostingMember, removeModerator


def removeAllPositions(groupInfo, userInfo):
    retval = []
    membersInfo = GSGroupMembersInfo(groupInfo.groupObj)
    status = GSGroupMembershipStatus(userInfo, membersInfo)
    if status.isPtnCoach:
        retval.append(removePtnCoach(groupInfo)[0])
    if status.isGroupAdmin:
        retval.append(removeAdmin(groupInfo, userInfo))
    if status.postingIsSpecial and status.isPostingMember:
        retval.append(removePostingMember(groupInfo, userInfo))
    if status.isModerator:
        retval.append(removeModerator(groupInfo, userInfo))
    if status.isModerated:
        retval.append(unmoderate(groupInfo, userInfo))
    return retval
