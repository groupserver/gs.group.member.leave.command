# coding=utf-8
'''The form that allows a group member to leave a group'''
from zope.formlib import form
from zope.formlib.form import Fields
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.radio import radio_widget
from Products.GSGroup.groupInfo import GSGroupInfo
from Products.GSGroup.joining import GSGroupJoining
from gs.content.form.form import SiteForm
from leaver import GroupLeaver
from fields import LeaveFields

class LeaveForm(SiteForm):
    pageTemplateFileName = 'browser/templates/leave.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    
    @Lazy
    def groupInfo(self):
        groupId = self.request.form['groupId']
        return GSGroupInfo(self.context, groupId)
    
    @Lazy
    def leaveFields(self):
        return LeaveFields(self.groupInfo)
    
    @Lazy
    def form_fields(self):
        retval = Fields(self.leaveFields.fields)
        retval['changeSubscription'].custom_widget = radio_widget
        return retval

    @Lazy
    def groupLeaver(self):
        return GroupLeaver(self.context, self.groupInfo, self.loggedInUser)

    @Lazy
    def label(self):
        retval = u'Left Group'
        if self.groupLeaver:
            retval = u'Change Subscription to %s' % (self.groupInfo.name)
        return retval
    
    def setUpWidgets(self, ignore_request=False):
        self.widgets = form.setUpWidgets(self.form_fields, self.prefix, 
            self.context, self.request, form=self, 
            ignore_request=ignore_request)
        self.widgets['changeSubscription']._displayItemForMissingValue = False
    
    @form.action(label=u'Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        change = data['changeSubscription']
        if change == 'leave':
            status = self.leaveGroup()
        else:
            status = self.setDelivery(change)
        self.status = status
        
    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
    
    def leaveGroup(self):
        rejoinAdvice = GSGroupJoining(self.groupInfo.groupObj).rejoin_advice
        rejoinAdvice = rejoinAdvice[0].upper() + rejoinAdvice[1:]
        success = u'You have left %s. %s.' % (self.groupInfo.name, rejoinAdvice)
        failure = u'Oops! Something went wrong. Please try again.'
        self.groupLeaver.removeMember()
        retval = self.groupLeaver.isMember and failure or success
        if retval == failure:
            self.errors = True
        return retval
    
    def setDelivery(self, change):
        web = 'web'
        digest = 'digest'
        assert change in [web, digest], \
          'Subscription change must be to web or digest'
        user = self.loggedInUser.user
        if change == digest:
            user.set_enableDigestByKey(self.groupInfo.id)
            status = u'The posts from %s will now be delivered '\
              'to you in the form of a daily digest of topics.' % \
               self.groupInfo.name
        elif change == web:
            user.set_disableDeliveryByKey(self.groupInfo.id)
            status = u'You will no longer receive any posts from %s via email.' % \
              self.groupInfo.name
        return status

