# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from zope.formlib.form import Fields
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.core import to_ascii
from gs.content.form.base import radio_widget, SiteForm
from Products.GSGroup.groupInfo import GSGroupInfo
from Products.GSGroup.joining import GSGroupJoining
from .fields import LeaveFields
from .leaver import GroupLeaver
from .notifier import LeaveNotifier, LeftNotifier


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
        return GroupLeaver(self.groupInfo, self.loggedInUser)

    @Lazy
    def label(self):
        retval = u'Left Group'
        if self.groupLeaver:
            retval = u'Change Subscription to %s' % (self.groupInfo.name)
        return retval

    def setUpWidgets(self, ignore_request=False):
        self.widgets = form.setUpWidgets(self.form_fields, self.prefix,
                                         self.context, self.request,
                                         form=self,
                                         ignore_request=ignore_request)
        self.widgets['changeSubscription']._displayItemForMissingValue =\
            False

    @form.action(label='Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        change = data['changeSubscription']
        if change == 'leave':
            status = self.leaveGroup()
        else:
            status = self.setDelivery(change)
        self.status = status

    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
        else:
            self.status = '<p>There are errors:</p>'

    def leaveGroup(self):
        rejoinAdvice = GSGroupJoining(self.groupInfo.groupObj).rejoin_advice
        rejoinAdvice = rejoinAdvice[0].upper() + rejoinAdvice[1:]
        success = 'You have left %s. %s.' % (self.groupInfo.name,
                                             rejoinAdvice)
        failure = 'Oops! Something went wrong. Please try again.'

        notifier = LeaveNotifier(self.groupInfo.groupObj, self.request)
        notifier.update(self.groupInfo, self.loggedInUser)
        adminNotifiers = []
        for admin in self.groupInfo.group_admins:
            if admin.id != self.loggedInUser.id:
                an = LeftNotifier(self.groupInfo.groupObj, self.request)
                an.update(self.groupInfo, self.loggedInUser, admin)
                adminNotifiers.append(an)
        self.groupLeaver.removeMember()
        retval = success if not self.groupLeaver.isMember else failure
        if retval == failure:
            self.errors = True
        else:
            notifier.notify(self.loggedInUser)
            for adminNotifier in adminNotifiers:
                adminNotifier.notify()
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        to_ascii('text/html'))
        return retval

    def setDelivery(self, change):
        web = 'web'
        digest = 'digest'
        assert change in [web, digest], \
            'Subscription change must be to web or digest'
        user = self.loggedInUser.user
        if change == digest:
            user.set_enableDigestByKey(self.groupInfo.id)
            status = 'The posts from %s will now be delivered '\
                     'to you in the form of a daily digest of topics.' % \
                     self.groupInfo.name
        elif change == web:
            user.set_disableDeliveryByKey(self.groupInfo.id)
            s = 'You will no longer receive any posts from {0} via email.'
            status = s.format(self.groupInfo.name)
        return status
