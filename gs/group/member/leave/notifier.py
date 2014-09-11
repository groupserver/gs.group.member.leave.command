# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.component import createObject, getMultiAdapter
from gs.profile.notify import MessageSender, NotifierABC
UTF8 = 'utf-8'


class LeaveNotifier(NotifierABC):
    htmlTemplateName = 'gs-group-member-leave-notification.html'
    textTemplateName = 'gs-group-member-leave-notification.txt'

    def __init__(self, context, request):
        super(LeaveNotifier, self).__init__(context, request)
        self.__updated = False
        self.htmlTemplate = None
        self.textTemplate = None

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Failed to create the GroupInfo from %s' % \
            self.context
        return retval

    def update(self, groupInfo, userInfo):
        '''Because the user may not have permission to see the group after
he or she has left this ``update`` method allows the notification to be
pre-rendered before it is sent off.'''
        self.subject = 'You have left {}'.format(groupInfo.name)
        htmlTemplate = getMultiAdapter((self.context, self.request),
                                       name=self.htmlTemplateName)
        self.html = htmlTemplate(userInfo=userInfo)
        textTemplate = getMultiAdapter((self.context, self.request),
                                       name=self.textTemplateName)
        self.text = textTemplate(userInfo=userInfo)

    def notify(self, userInfo):
        sender = MessageSender(self.context, userInfo)
        sender.send_message(self.subject, self.text, self.html)
        self.reset_content_type()


class LeftNotifier(LeaveNotifier):
    htmlTemplateName = 'gs-group-member-leave-left.html'
    textTemplateName = 'gs-group-member-leave-left.txt'

    def update(self, groupInfo, userInfo, adminInfo):
        '''Because the user may not have permission to see the group after
he or she has left this ``update`` method allows the notification to be
pre-rendered before it is sent off.'''
        self.adminInfo = adminInfo
        self.subject = '{0} has left {1}'.format(userInfo.name,
                                                 groupInfo.name)
        htmlTemplate = getMultiAdapter((self.context, self.request),
                                       name=self.htmlTemplateName)
        self.html = htmlTemplate(userInfo=userInfo, adminInfo=adminInfo)
        textTemplate = getMultiAdapter((self.context, self.request),
                                       name=self.textTemplateName)
        self.text = textTemplate(userInfo=userInfo, adminInfo=adminInfo)

    def notify(self):
        sender = MessageSender(self.context, self.adminInfo)
        sender.send_message(self.subject, self.text, self.html)
        self.reset_content_type()
