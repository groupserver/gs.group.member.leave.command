# coding=utf-8
'''The form that allows a group member to leave a group'''
from zope.formlib import form
from zope.formlib.form import Fields
from Products.Five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.GSContent.interfaces import IGSSiteInfo
from Products.GSGroup.interfaces import IGSGroupInfo
from Products.GSGroup.changebasicprivacy import radio_widget
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
        self.form_fields = Fields(LeaveFields(self.groupInfo).fields)
        self.form_fields['changeSubscription'].custom_widget = radio_widget
        
    @form.action(label=u'Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        status = u'Something changed!'
        self.status = status

    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
            