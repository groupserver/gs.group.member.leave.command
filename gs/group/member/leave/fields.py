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
from zope.schema import Choice
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.GSGroup.joining import GSGroupJoining


class LeaveFields(object):
    def __init__(self, groupInfo):
        self.groupInfo = groupInfo

    @Lazy
    def fields(self):
        retval = Choice(
            __name__='changeSubscription',
            title='Want less email?',
            description='These options are shown to a group member wishing '
                        'to leave the group',
            vocabulary=self.vocab,
            default='leave',
            required=False)
        return retval

    @property
    def vocab(self):
        retval = SimpleVocabulary([
            self.leaveTerm,
            SimpleTerm('web', 'web', 'Read posts on the web (no email)'),
            SimpleTerm('digest', 'digest', 'Receive a digest of topics '
                       '(maximum one email per day)')])
        return retval

    @Lazy
    def leaveTerm(self):
        rejoinAdvice = GSGroupJoining(self.groupInfo.groupObj).rejoin_advice
        title = 'Leave %s (%s)' % (self.groupInfo.name, rejoinAdvice)
        retval = SimpleTerm('leave', 'leave', title)
        return retval
