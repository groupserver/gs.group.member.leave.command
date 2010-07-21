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
from Products.GSContent.interfaces import IGSSiteInfo
from gs.profile.notify.interfaces import IGSNotifyUser
from Products.GSGroup.groupInfo import GSGroupInfo
from Products.GSGroup.interfaces import IGSGroupInfo
from Products.GSGroup.changebasicprivacy import radio_widget
from gs.group.member.leave.leaver import GroupLeaver
from gs.group.member.leave.fields import LeaveFields
from gs.group.member.leave.audit import LeaveAuditor, LEAVE

class LeaveForm(PageForm):
    pageTemplateFileName = 'browser/templates/leave.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    
    def __init__(self, context, request):
        PageForm.__init__(self, context, request)
        self.context = context
        self.siteInfo = IGSSiteInfo(context)
        groupId = request.form['groupId']
        self.groupInfo = GSGroupInfo(context, groupId)
        self.leaveFields = LeaveFields(self.groupInfo)
        self.form_fields = Fields(self.leaveFields.fields)
        self.form_fields['changeSubscription'].custom_widget = radio_widget

    @property
    def userInfo(self):
        return createObject('groupserver.LoggedInUser', self.context)

    @property
    def groupLeaver(self):
        return GroupLeaver(self.userInfo, self.groupInfo)

    @property
    def label(self):
        retval = u'Left Group'
        if self.groupLeaver:
            retval = u'Change Subscription to %s' % (self.groupInfo.name)
        return retval
    
    def setUpWidgets(self, ignore_request=False):
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self,
            ignore_request=ignore_request)
        self.widgets['changeSubscription']._displayItemForMissingValue = False
    
    @form.action(label=u'Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        change = data['changeSubscription']
        if change == 'leave':
            status = self.groupLeaver.removeUser()
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
            status = u'The posts from %s will now be delivered '\
              'to you in the form of a daily digest of topics.' %\
               self.groupInfo.name
        elif change == web:
            user.set_disableDeliveryByKey(self.groupInfo.id)
            status = u'You will not receive any posts from %s.' %\
              self.groupInfo.name
        return status
    