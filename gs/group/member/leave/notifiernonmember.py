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
from __future__ import absolute_import, unicode_literals
from email import message_from_string
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEMessage import MIMEMessage
from email.utils import (formataddr, parseaddr)
from zope.cachedescriptors.property import Lazy
from zope.component import (createObject, getMultiAdapter)
from gs.core import (to_ascii, to_unicode_or_bust)
from gs.email import send_email
UTF8 = 'utf-8'


class NotMemberNotifier(object):
    htmlTemplateName = 'gs-group-member-leave-not-a-member.html'
    textTemplateName = 'gs-group-member-leave-not-a-member.txt'

    def __init__(self, groups, request):
        self.context = self.groups = groups
        self.request = request

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.htmlTemplateName)
        return retval

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.textTemplateName)
        return retval

    @staticmethod
    def fromAddr(siteInfo):
        siteName = '{siteName} Support'.format(siteName=siteInfo.name)
        unicodeName = to_unicode_or_bust(siteName)
        headerName = Header(unicodeName, UTF8)
        encodedName = headerName.encode()
        addr = siteInfo.get_support_email()
        retval = formataddr((encodedName, addr))
        return retval

    def notify(self, groupInfo, toEmailAddress):
        fromAddr = self.fromAddr(groupInfo.siteInfo)
        subject = 'Request to leave {}'.format(groupInfo.name)
        html = self.htmlTemplate(emailAddress=toEmailAddress,
                                 groupName=groupInfo.name,
                                 groupURL=groupInfo.url)
        text = self.textTemplate(emailAddress=toEmailAddress,
                                 groupName=groupInfo.name,
                                 groupURL=groupInfo.url)

        message = self.create_message(toEmailAddress, fromAddr, 
                                      subject, text, html)
        send_email(groupInfo.siteInfo.get_support_email(),
                   toEmailAddress, message)

    @staticmethod
    def create_message(toAddr, fromAddr, subject, txtMessage, htmlMessage):
        container = MIMEMultipart('alternative')
        container['Subject'] = str(Header(subject, UTF8))
        container['To'] = toAddr
        container['From'] = fromAddr

        txt = MIMEText(txtMessage.encode(UTF8), 'plain', UTF8)
        container.attach(txt)

        html = MIMEText(htmlMessage.encode(UTF8), 'html', UTF8)
        container.attach(html)

        retval = container.as_string()
        assert retval
        return retval
