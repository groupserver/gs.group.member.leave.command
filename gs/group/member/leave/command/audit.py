# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and
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
from pytz import UTC
from datetime import datetime
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.component.interfaces import IFactory
from zope.interface import implementer, implementedBy
from Products.XWFCore.XWFUtils import munge_date
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from Products.GSGroup.groupInfo import groupInfo_to_anchor
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, AuditQuery
from Products.GSAuditTrail.utils import event_id_from_data
SUBSYSTEM = 'gs.group.member.leave.command'
from logging import getLogger
log = getLogger(SUBSYSTEM)
UNKNOWN = '0'  # Unknown is always "0"
LEAVE_COMMAND = '1'


@implementer(IFactory)
class LeaveAuditEventFactory(object):
    """A Factory for group leaving events."""
    title = 'GroupServer Leave Group Audit Event Factory'
    description = 'Creates a GroupServer event auditor for leaving groups'

    def __call__(self, context, event_id, code, date, userInfo,
                 instanceUserInfo, siteInfo, groupInfo, instanceDatum='',
                 supplementaryDatum='', subsystem=''):
        """Create an event"""
        if subsystem != SUBSYSTEM:
            raise ValueError('Subsystems do not match')

        if (code == LEAVE_COMMAND):
            event = LeaveCommand(context, event_id, date, instanceUserInfo,
                                 groupInfo, siteInfo, instanceDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
                                    instanceUserInfo, instanceUserInfo,
                                    siteInfo, groupInfo, instanceDatum,
                                    supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


@implementer(IAuditEvent)
class LeaveCommand(BasicAuditEvent):
    'The audit-event for an email-command comming in.'

    def __init__(self, context, eventId, d, instanceUserInfo, groupInfo,
                 siteInfo, email):
        super(LeaveCommand, self).__init__(
            context, eventId, LEAVE_COMMAND, d, instanceUserInfo,
            instanceUserInfo, siteInfo, groupInfo, email, None, SUBSYSTEM)

    def __unicode__(self):
        r = 'Email-command to leave {0} ({1}) on {2} ({3}) recieved for '\
            '{4} ({5}) <{6}>.'
        retval = r.format(
            self.groupInfo.name, self.groupInfo.id,
            self.siteInfo.name, self.siteInfo.id,
            self.instanceUserInfo.name, self.instanceUserInfo.id,
            self.instanceDatum)
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event groupserver-group-member-leave-command-%s' % self.code
        r = '<span class="{0}">Sent an email in to leave {1}</span> ({2})'
        retval = r.format(cssClass, groupInfo_to_anchor(self.groupInfo),
                          munge_date(self.context, self.date))
        return retval


class LeaveAuditor(object):
    """An Auditor for leaving"""
    def __init__(self, context, instanceUserInfo, groupInfo=None):
        """Create a leaving auditor."""
        self.context = context
        self.instanceUserInfo = instanceUserInfo
        self.__groupInfo = groupInfo

    @Lazy
    def userInfo(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    @Lazy
    def groupInfo(self):
        retval = self.__groupInfo if self.__groupInfo is not None else \
            createObject('groupserver.GroupInfo', self.context)
        return retval

    @Lazy
    def factory(self):
        retval = LeaveAuditEventFactory()
        return retval

    @property
    def queries(self):
        retval = AuditQuery()
        return retval

    def info(self, code, instanceDatum='', supplementaryDatum=''):
        """Log an info event to the audit trail.
            * Creates an ID for the new event,
            * Writes the instantiated event to the audit-table, and
            * Writes the event to the standard Python log.
        """
        d = datetime.now(UTC)
        eventId = event_id_from_data(
            self.userInfo,
            self.instanceUserInfo, self.siteInfo, code, instanceDatum,
            '%s-%s' % (self.groupInfo.name, self.groupInfo.id))

        e = self.factory(self.context, eventId, code, d, self.userInfo,
                         self.instanceUserInfo, self.siteInfo,
                         self.groupInfo, instanceDatum, None, SUBSYSTEM)

        self.queries.store(e)
        log.info(e)
        return e
