# coding=utf-8
'''The code that removes a group member from the group'''
from zope.component import createObject
from gs.profile.notify.interfaces import IGSNotifyUser
from Products.XWFCore.XWFUtils import getOption
from Products.GSGroup.utils import is_secret
from gs.group.member.base.utils import user_member_of_group, member_id
from gs.group.member.manage.utils import removeAllPositions
from gs.group.member.leave.audit import LeaveAuditor, LEAVE

class GroupLeaver(object):
    def __init__(self, groupInfo, userInfo):
        self.groupInfo = groupInfo
        self.userInfo = userInfo

    def __bool__(self):
        return bool(self.isMember)

    def __nonzero__(self):
        return self.__bool__()

    @property
    def isMember(self):
        return user_member_of_group(self.userInfo, self.groupInfo)
    
    def removeMember(self):
        retval = []
        if not self.isMember:
            return retval
        removingUserInfo = createObject('groupserver.LoggedInUser', self.groupInfo.groupObj)
        adminsToNotify, nDict = self.adminNotification()
        gId = self.groupInfo.id
        usergroupName = member_id(gId)
        self.userInfo.user.del_groupWithNotification(usergroupName)
        if not self.isMember:
            retval = removeAllPositions(self.groupInfo, self.userInfo)
            auditor = LeaveAuditor(self.groupInfo.groupObj, self.userInfo, self.groupInfo)
            auditor.info(LEAVE)
            for admin in adminsToNotify:
                admin.send_notification('leave_group_admin', gId, nDict)
            retval.append('removed from the group')
        return retval

    def adminNotification(self):
        siteInfo = self.groupInfo.siteInfo
        admins = [ IGSNotifyUser(a) for a in self.groupInfo.group_admins ]
        nDict = {
          'siteInfo'      : siteInfo,
          'groupInfo'     : self.groupInfo,
          'userInfo'      : self.userInfo 
        }
        retval = (admins, nDict)
        return retval
