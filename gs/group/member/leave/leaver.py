# coding=utf-8
'''The code that removes a group member from the group'''
from zope.component import createObject
from gs.profile.notify.interfaces import IGSNotifyUser
from Products.XWFCore.XWFUtils import getOption
from Products.GSGroup.utils import is_secret
from Products.GSGroup.joining import GSGroupJoining
from gs.group.member.base.utils import user_member_of_group, member_id
from gs.group.member.leave.audit import LeaveAuditor, REMOVE, LEAVE

class GroupLeaver(object):
    def __init__(self, userInfo, groupInfo):
        self.userInfo = userInfo
        self.groupInfo = groupInfo
        self.siteInfo = groupInfo.siteInfo

    def __bool__(self):
        return bool(self.isMember)

    def __nonzero__(self):
        return self.__bool__()

    @property
    def isMember(self):
        return user_member_of_group(self.userInfo, self.groupInfo)
    
    def removeUser(self):
        rejoinAdvice = GSGroupJoining(self.groupInfo.groupObj).rejoin_advice
        rejoinAdvice = rejoinAdvice[0].upper() + rejoinAdvice[1:] 
        status = u'You have left %s. %s.' % (self.groupInfo.name, rejoinAdvice)
        removingUserInfo = createObject('groupserver.LoggedInUser', self.groupInfo.groupObj)
        ptnCoach, nDict = self.ptnCoachNotification()
        gId = self.groupInfo.id
        usergroupName = member_id(gId)
        self.userInfo.user.del_groupWithNotification(usergroupName)
        if self.isMember:
            self.errors = True
            status = u'Oops! Something went wrong. Please try again.'
            return status
        auditor = LeaveAuditor(self.groupInfo.groupObj, self.userInfo, self.groupInfo)
        if self.userInfo.id!=removingUserInfo.id:
            auditor.info(REMOVE)
        else:
            auditor.info(LEAVE)
        if ptnCoach and ptnCoach.id!=removingUserInfo.id:
            notifyPtn = IGSNotifyUser(ptnCoach)
            notifyPtn.send_notification('leave_group_admin', gId, nDict)
        return status

    def ptnCoachNotification(self):
        nDict = None
        ptnCoach = self.groupInfo.ptn_coach
        if ptnCoach:
            nDict = {
              'siteInfo'      : self.siteInfo,  # These three info classes are
              'groupInfo'     : self.groupInfo, # enough, but it will take time
              'userInfo'      : self.userInfo,  # to change the notifications. 
              'groupId'       : self.groupInfo.id,
              'groupName'     : self.groupInfo.name,
              'siteName'      : self.siteInfo.name,
              'canonical'     : getOption(self.groupInfo.groupObj, 'canonicalHost'),
              'supportEmail'  : getOption(self.siteInfo.siteObj, 'supportEmail'),
              'memberId'      : self.userInfo.id,
              'memberName'    : self.userInfo.name
            }
        retval = (ptnCoach, nDict)
        return retval
        