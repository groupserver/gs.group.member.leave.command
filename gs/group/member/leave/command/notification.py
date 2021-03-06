# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from zope.i18n import translate
from gs.content.email.base import (SiteEmail, TextMixin)
from . import GSMessageFactory as _
UTF8 = 'utf-8'


class NotAMemberHTMLNotification(SiteEmail):
    '''The notification to the sender that he or she is not a member of the group.'''
    def __init__(self, context, request):
        super(NotAMemberHTMLNotification, self).__init__(context, request)

    def get_support_email(self, userInfo, emailAddress, groupUrl):
        subject = _('support-notification-not-member-subject',
                    'Not a member')
        translatedSubject = translate(subject)
        purl = '{0}{1}'.format(self.siteInfo.url, userInfo.url)
        body = _('support-notifiation-not-member-body',
                 'Hello,\n\nI tried to leave a group and I got a message '
                 'back saying that I\nwas not a member, and...\n\n--\n'
                 'These links may help you:\n'
                 '  Group     ${groupUrl}\n'
                 '  Me        ${profileUrl}\n'
                 '  My email  ${email}\n',
                 mapping={'groupUrl': groupUrl, 'profileUrl': purl, 'email': emailAddress})
        translatedBody = translate(body)
        retval = self.mailto(self.siteInfo.get_support_email(),
                             translatedSubject, translatedBody)
        return retval


class NotAMemberTXTNotification(NotAMemberHTMLNotification, TextMixin):

    def __init__(self, context, request):
        super(NotAMemberTXTNotification, self).__init__(context, request)
        filename = 'not-a-member-{0}.txt'.format(self.siteInfo.id)
        self.set_header(filename)


class NoProfileHTMLNotification(SiteEmail):
    '''The notification to the sender that his or her email address is totally unrecognised.'''
    def __init__(self, context, request):
        super(NoProfileHTMLNotification, self).__init__(context, request)

    def get_support_email(self, emailAddress, groupUrl):
        subject = _('support-notification-no-profile-subject',
                    'Not a member (no profile)')
        translatedSubject = translate(subject)
        body = _('support-notifiation-no-profile-body',
                 '''Hello,

I tried to leave a group and I got a message back saying that my
profile could not be found, and...

--
These links may help you:\n
  Group  ${groupUrl}
  Me     ${email}\n''', mapping={'groupUrl': groupUrl, 'email': emailAddress})
        translatedBody = translate(body)
        retval = self.mailto(self.siteInfo.get_support_email(),
                             translatedSubject, translatedBody)
        return retval


class NoProfileTXTNotification(NoProfileHTMLNotification, TextMixin):

    def __init__(self, context, request):
        super(NoProfileTXTNotification, self).__init__(context, request)
        filename = 'no-profile-{0}.txt'.format(self.siteInfo.id)
        self.set_header(filename)
