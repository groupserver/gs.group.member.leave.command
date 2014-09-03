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
from gs.content.email.base import GroupEmail, TextMixin
UTF8 = 'utf-8'


class LeftHTMLNotification(GroupEmail):

    def __init__(self, group, request):
        super(LeftHTMLNotification, self).__init__(group, request)
        self.group = group

    def get_support_email(self, user, admin):
        subj = 'A member left my group'
        uu = '{}{}'.format(self.siteInfo.url, user.url)
        au = '{}{}'.format(self.siteInfo.url, admin.url)
        msg = 'Hello,\n\nA member left my group, {group}, '\
              'and...\n\n--\nThese links may be useful:\n  '\
              'Group   {url}\n  Me      {adminUrl}\n  Member  {userUrl}\n'
        body = msg.format(group=self.groupInfo.name, url=self.groupInfo.url,
                          adminUrl=au, userUrl=uu)
        m = 'mailto:{to}?Subject={subj}&body={body}'
        retval = m.format(to=self.siteInfo.get_support_email(),
                          subj=quote(subj), body=quote(body.encode(UTF8)))
        return retval


class LeftTXTNotification(LeftHTMLNotification, TextMixin):

    def __init__(self, group, request):
        super(LeftTXTNotification, self).__init__(group, request)
        filename = 'left-{0}-{1}.txt'.format(self.siteInfo.id,
                                             self.groupInfo.id)
        self.set_header(filename)
