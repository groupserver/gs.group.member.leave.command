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
from gs.content.email.base import AnonymousNotifierABC
from gs.profile.notify import MessageSender
from . import GSMessageFactory as _


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
