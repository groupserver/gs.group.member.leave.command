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
from zope.component import getMultiAdapter
from zope.i18n import translate
from gs.email import send_email
from gs.content.email.base import (AnonymousNotifierABC, GroupNotifierABC)
from gs.profile.notify import MessageSender
from . import GSMessageFactory as _


class LeaveNotifier(GroupNotifierABC):
    htmlTemplateName = 'gs-group-member-leave-notification.html'
    textTemplateName = 'gs-group-member-leave-notification.txt'

    def __init__(self, context, request):
        super(LeaveNotifier, self).__init__(context, request)
        self.__updated = False
        self.htmlTemplate = None
        self.textTemplate = None

    def update(self, groupInfo, userInfo):
        '''Because the user may not have permission to see the group after
he or she has left this ``update`` method allows the notification to be
pre-rendered before it is sent off.'''
        subject = _('leave-notification-subject',
                    'You have left ${groupName}',
                    mapping={'groupName': groupInfo.name})
        self.subject = translate(subject)
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
        subject = _('member-left-subject',
                    '${userName} has left ${groupName}',
                    mapping={'userName': userInfo.name,
                             'groupName': groupInfo.name})
        self.subject = translate(subject)
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


class NotMemberNotifier(AnonymousNotifierABC):
    htmlTemplateName = 'gs-group-member-leave-not-a-member.html'
    textTemplateName = 'gs-group-member-leave-not-a-member.txt'

    def notify(self, groupInfo, toEmailAddress):
        fromAddr = self.fromAddr(groupInfo.siteInfo)
        subject = _('leave-request-problem-subject',
                    'Request to leave ${groupName}',
                    mapping={'groupName': groupInfo.name})
        translatedSubject = translate(subject)
        html = self.htmlTemplate(emailAddress=toEmailAddress,
                                 groupName=groupInfo.name,
                                 groupURL=groupInfo.url)
        text = self.textTemplate(emailAddress=toEmailAddress,
                                 groupName=groupInfo.name,
                                 groupURL=groupInfo.url)

        message = self.create_message(toEmailAddress, fromAddr,
                                      translatedSubject, text, html)
        send_email(groupInfo.siteInfo.get_support_email(),
                   toEmailAddress, message)
        self.reset_content_type()
