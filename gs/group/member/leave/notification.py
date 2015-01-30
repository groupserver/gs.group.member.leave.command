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
from zope.cachedescriptors.property import Lazy
from zope.i18n import translate
from gs.content.email.base import (GroupEmail, SiteEmail, TextMixin)
from gs.group.privacy.interfaces import IGSGroupVisibility
from . import GSMessageFactory as _
UTF8 = 'utf-8'


class LeveHTMLNotification(GroupEmail):
    'The notification to the past member that he or she has left the group.'

    def __init__(self, group, request):
        super(LeveHTMLNotification, self).__init__(group, request)
        self.group = group

    def get_support_email(self, user):
        subject = _('support-notification-leave-subject', 'Left a group')
        translatedSubject = translate(subject)
        uu = '{}{}'.format(self.siteInfo.url, user.url)
        body = _('support-notification-leave-body',
                 'Hello,\n\nI left the group ${groupName} and...\n\n--\n'
                 'These links may help you:\n'
                 '  Group  ${groupUrl}\n'
                 '  Me     ${userUrl}\n',
                 mapping={'groupName': self.groupInfo.name,
                          'groupUrl': self.groupInfo.url,
                          'userUrl': uu})
        translatedBody = translate(body)
        retval = self.mailto(self.siteInfo.get_support_email(),
                             translatedSubject, translatedBody)
        return retval

    @Lazy
    def visibility(self):
        retval = IGSGroupVisibility(self.groupInfo)
        return retval


class LeveTXTNotification(LeveHTMLNotification, TextMixin):

    def __init__(self, group, request):
        super(LeveTXTNotification, self).__init__(group, request)
        filename = 'left-{0}-{1}.txt'.format(self.siteInfo.id,
                                             self.groupInfo.id)
        self.set_header(filename)


class LeftHTMLNotification(GroupEmail):
    'The notification to the administrator that a member has left'

    def __init__(self, group, request):
        super(LeftHTMLNotification, self).__init__(group, request)
        self.group = group

    def get_support_email(self, user, admin):
        subject = _('support-notification-member-left-subject',
                    'A member left my group')
        translatedSubject = translate(subject)
        uu = '{}{}'.format(self.siteInfo.url, user.url)
        au = '{}{}'.format(self.siteInfo.url, admin.url)
        body = _('support-notification-member-left-body',
                 'Hello,\n\nA member left my group, ${groupName}, and...'
                 '\n\n--\nThese links may be useful:\n'
                 '  Group   ${groupUrl}\n'
                 '  Me      ${adminUrl}\n'
                 '  Member  ${userUrl}\n',
                 mapping={'groupName': self.groupInfo.name,
                          'groupUrl': self.groupInfo.url,
                          'adminUrl': au, 'userUrl': uu})
        translatedBody = translate(body)
        retval = self.mailto(self.siteInfo.get_support_email(),
                             translatedSubject, translatedBody)
        return retval


class LeftTXTNotification(LeftHTMLNotification, TextMixin):

    def __init__(self, group, request):
        super(LeftTXTNotification, self).__init__(group, request)
        filename = 'left-{0}-{1}.txt'.format(self.siteInfo.id,
                                             self.groupInfo.id)
        self.set_header(filename)


# Not a member


class NotAMemberHTMLNotification(SiteEmail):
    '''The notification to the sender that he or she is not a member of
    the group.'''

    def __init__(self, context, request):
        super(NotAMemberHTMLNotification, self).__init__(context, request)

    def get_support_email(self, emailAddress, groupUrl):
        print ('Here')
        subject = _('support-notification-not-member-subject',
                    'Not a member')
        translatedSubject = translate(subject)
        body = _('support-notifiation-not-member-body',
                 'Hello,\n\nI tried to leave a group and I got a message '
                 'back saying that I\nwas not a member, and...\n\n--\n'
                 'These links may help you:\n'
                 '  Group  ${groupUrl}\n'
                 '  Me     ${email}\n',
                 mapping={'groupUrl': groupUrl, 'email': emailAddress})
        translatedBody = translate(body)
        retval = self.mailto(self.siteInfo.get_support_email(),
                             translatedSubject, translatedBody)
        return retval


class NotAMemberTXTNotification(NotAMemberHTMLNotification, TextMixin):

    def __init__(self, context, request):
        super(NotAMemberTXTNotification, self).__init__(context, request)
        filename = 'not-a-member-{0}.txt'.format(self.siteInfo.id)
        self.set_header(filename)
