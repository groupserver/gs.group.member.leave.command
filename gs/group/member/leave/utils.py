# coding=utf-8
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from Products.GSGroupMember.groupmembershipstatus import GSGroupMembershipStatus
from gs.group.member.manage.utils import removePtnCoach, removeAdmin, unmoderate
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

