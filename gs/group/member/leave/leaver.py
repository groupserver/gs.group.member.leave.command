# coding=utf-8
'''The code that removes a group member from the group'''
from zope.component import createObject
from zope.event import notify
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from Products.GSGroupMember.groupmembershipstatus import GSGroupMembershipStatus
from gs.profile.notify.interfaces import IGSNotifyUser
from gs.group.member.base.utils import member_id
from gs.group.member.leave.utils import removeAllPositions
from gs.group.member.leave.audit import LeaveAuditor, LEAVE
from event import GSLeaveGroupEvent

class GroupLeaver(object):
    def __init__(self, context, groupInfo, userInfo):
        self.context = context
        self.groupInfo = groupInfo
        self.userInfo = userInfo

    def __bool__(self):
        return bool(self.isMember)

    def __nonzero__(self):
        return self.__bool__()

    @property
    def isMember(self):
        membersInfo = GSGroupMembersInfo(self.groupInfo.groupObj)
        status = GSGroupMembershipStatus(self.userInfo, membersInfo)
        return status
    
    def removeMember(self):
        retval = []
        if not self.isMember:
            return retval
        adminsToNotify, nDict = self.adminNotification()
        gId = self.groupInfo.id
        usergroupName = member_id(gId)
        retval = removeAllPositions(self.groupInfo, self.userInfo)
        self.userInfo.user.del_groupWithNotification(usergroupName)
        groupObj = self.groupInfo.groupObj
        if not self.isMember:
            auditor = LeaveAuditor(groupObj, self.userInfo, self.groupInfo)
            auditor.info(LEAVE)
            for admin in adminsToNotify:
                admin.send_notification('leave_group_admin', gId, nDict)
            retval.append('removed from the group')
        notify(GSLeaveGroupEvent(groupObj, self.groupInfo, self.userInfo))
        return retval

    def adminNotification(self):
        siteInfo = self.groupInfo.siteInfo
        admins = [ IGSNotifyUser(a) for a in self.groupInfo.group_admins 
                  if a.id != self.userInfo.id ]
        nDict = {
          'siteInfo'      : siteInfo,
          'groupInfo'     : self.groupInfo,
          'userInfo'      : self.userInfo 
        }
        retval = (admins, nDict)
        return retval

