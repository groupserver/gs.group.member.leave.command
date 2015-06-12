# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2010, 2011, 2012, 2013, 2014 OnlineGroups.net and
# Contributors.
#
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
from . import GSMessageFactory as _
from .fields import LeaveFields
from .leaver import GroupLeaver
from .utils import leave_group


class LeaveForm(SiteForm):
    pageTemplateFileName = 'browser/templates/leave.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    @Lazy
    def groupLeaver(self):
        retval = GroupLeaver(self.groupInfo, self.loggedInUser)
        return retval

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
    def label(self):
        retval = _('left', 'Left group')
        if self.groupLeaver:
            retval = _('changed', 'Change subscription to ${groupName}',
                       mapping={'groupName': self.groupInfo.name})
        return retval

    def setUpWidgets(self, ignore_request=False):
        self.widgets = form.setUpWidgets(self.form_fields, self.prefix,
                                         self.context, self.request,
                                         form=self,
                                         ignore_request=ignore_request)
        self.widgets['changeSubscription']._displayItemForMissingValue =\
            False

    @form.action(label=_('change', 'Change'),
                 failure='handle_change_action_failure')
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
        success = _('leave-success',
                    'You have left ${groupName}. ${rejoin}.',
                    mapping={'groupName': self.groupInfo.name,
                             'rejoin': rejoinAdvice})
        failure = _('leave-fail',
                    'Something went wrong. Please try again.')

        left = leave_group(self.groupInfo, self.loggedInUser, self.request)
        retval = success if left else failure
        self.errors = not left
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
            status = _('change-digest',
                       'The posts from ${groupName} will now be delivered'
                       'to you in the form of a daily digest of topics.',
                       mapping={'groupName': self.groupInfo.name})
        elif change == web:
            user.set_disableDeliveryByKey(self.groupInfo.id)
            status = _('change-web-only',
                       'You will no longer receive any posts from '
                       '${groupName} via email.',
                       mapping={'groupName': self.groupInfo.name})
        return status
