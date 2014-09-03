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
from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.content.email.base import GroupEmail, TextMixin
from gs.group.privacy.interfaces import IGSGroupVisibility
UTF8 = 'utf-8'


class LeveHTMLNotification(GroupEmail):

    def __init__(self, group, request):
        super(LeveHTMLNotification, self).__init__(group, request)
        self.group = group

    def get_support_email(self, user):
        subj = 'Left a group'
        uu = '{}{}'.format(self.siteInfo.url, user.url)
        msg = 'Hello,\n\nI left the group {group} '\
              'and...\n\n--\nThese links may help you:\n  '\
              'Group          {url}\n  Me             {userUrl}\n'
        body = msg.format(group=self.groupInfo.name, url=self.groupInfo.url,
                          userUrl=uu)
        m = 'mailto:{to}?Subject={subj}&body={body}'
        retval = m.format(to=self.siteInfo.get_support_email(),
                          subj=quote(subj), body=quote(body.encode(UTF8)))
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
