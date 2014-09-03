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
from gs.core import to_ascii
from gs.profile.notify import MessageSender
UTF8 = 'utf-8'


class LeaveNotifier(object):
    htmlTemplateName = 'gs-group-member-leave-notification.html'
    textTemplateName = 'gs-group-member-leave-notification.txt'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        h = self.request.response.getHeader('Content-Type')
        self.oldContentType = to_ascii(h if h else 'text/html')
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

        self.request.response.setHeader(to_ascii('Content-Type'),
                                        to_ascii(self.oldContentType))
