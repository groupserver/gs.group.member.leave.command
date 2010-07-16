# coding=utf-8
'''The form that allows a group member to leave a group'''
try:
    from five.formlib.formbase import PageForm
except ImportError:
    from Products.Five.formlib.formbase import PageForm

from zope.formlib import form
from zope.formlib.form import Fields
from zope.component import createObject
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFCore.XWFUtils import getOption
from Products.GSContent.interfaces import IGSSiteInfo
from gs.profile.notify.interfaces import IGSNotifyUser
from Products.GSGroup.interfaces import IGSGroupInfo
from Products.GSGroup.changebasicprivacy import radio_widget
from Products.GSGroupMember.groupmembership import user_member_of_group, member_id
from gs.group.member.leave.fields import LeaveFields
from gs.group.member.leave.audit import LeaveAuditor, LEAVE

class LeaveForm(PageForm):
    pageTemplateFileName = 'browser/templates/leave.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    
    def __init__(self, context, request):
        PageForm.__init__(self, context, request)
        self.siteInfo = IGSSiteInfo(context)
        self.groupInfo = IGSGroupInfo(context)
        self.label = u'Change Subscription to %s' % (self.groupInfo.name)
        self.leaveFields = LeaveFields(self.groupInfo)
        self.form_fields = Fields(self.leaveFields.fields)
        self.form_fields['changeSubscription'].custom_widget = radio_widget
        
    def setUpWidgets(self, ignore_request=False):
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self,
            ignore_request=ignore_request)
        self.widgets['changeSubscription']._displayItemForMissingValue = False
    
    @property
    def userInfo(self):
        return createObject('groupserver.LoggedInUser', self.groupInfo.groupObj)
    
    @property
    def isMember(self):
        return user_member_of_group(self.userInfo, self.groupInfo)
    
    @form.action(label=u'Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        change = data['changeSubscription']
        if change == 'leave':
            status = self.removeUser()
        else:
            status = self.setDelivery(change)
        self.status = status
        
    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
    
    def setDelivery(self, change):
        web = 'web'
        digest = 'digest'
        assert change in [web, digest], \
          'Subscription change must be to web or digest'
        user = self.userInfo.user
        if change == digest:
            user.set_enableDigestByKey(self.groupInfo.id)
            status = u'You will now receive posts from %s as a '\
              u'digest of topics (maximum one email per day).' %\
              self.groupInfo.name
        elif change == web:
            user.set_disableDeliveryByKey(self.groupInfo.id)
            status = u'You will no longer receive posts from %s '\
              u'via email.' % self.groupInfo.name
        return status
    
    def removeUser(self):
        usergroupName = member_id(self.groupInfo.id)
        self.userInfo.user.del_groupWithNotification(usergroupName)
        if self.isMember:
            self.errors = True
            status = u'Oops! Something went wrong. Please try again.'
        else:
            auditor = LeaveAuditor(self.groupInfo.groupObj, self.userInfo)
            auditor.info(LEAVE)
            ptnCoach = self.groupInfo.ptn_coach
            if ptnCoach and ptnCoach.id!=self.userInfo.id: #Unlikely, but possible
                notifyPtn = IGSNotifyUser(ptnCoach)
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
                notifyPtn.send_notification('leave_group_admin', self.groupInfo.id, nDict)
            rejoinAdvice = self.leaveFields.rejoinAdvice[0].upper() + self.leaveFields.rejoinAdvice[1:] 
            status = u'You have left %s. %s.' % (self.groupInfo.name, rejoinAdvice)
        return status

        