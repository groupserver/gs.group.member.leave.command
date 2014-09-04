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
SUBSYSTEM = 'gs.group.member.leave'
from logging import getLogger
log = getLogger(SUBSYSTEM)
UNKNOWN = '0'  # Unknown is always "0"
LEAVE = '1'
LEAVE_COMMAND = '2'


@implementer(IFactory)
class LeaveAuditEventFactory(object):
    """A Factory for group leaving events.
    """

    title = 'GroupServer Leave Group Audit Event Factory'
    description = 'Creates a GroupServer event auditor for leaving groups'

    def __call__(self, context, event_id, code, date, userInfo,
                 instanceUserInfo, siteInfo, groupInfo, instanceDatum='',
                 supplementaryDatum='', subsystem=''):
        """Create an event"""
        assert subsystem == SUBSYSTEM, 'Subsystems do not match'

        if (code == LEAVE):
            event = LeaveEvent(context, event_id, date, userInfo,
                               instanceUserInfo, siteInfo, groupInfo)
        elif (code == LEAVE_COMMAND):
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
class LeaveEvent(BasicAuditEvent):
    ''' An audit-trail event representing a user being removed
        from a group'''

    def __init__(self, context, id, d, userInfo, instanceUserInfo,
                 siteInfo, groupInfo):
        """Create a leave event"""
        super(LeaveEvent, self).__init__(context, id, LEAVE, d, userInfo,
                                         instanceUserInfo, siteInfo,
                                         groupInfo, None, None, SUBSYSTEM)

    @property
    def adminRemoved(self):
        retval = False
        if (self.userInfo.id and
           (self.userInfo.id != self.instanceUserInfo.id)):
            retval = True
        return retval

    def __unicode__(self):
        if self.adminRemoved:
            r = '{0} ({1}) was removed from {2} ({3}) on {4} ({5}) by {6} '\
                '({7}).'
            retval = r.format(
                self.instanceUserInfo.name,
                self.instanceUserInfo.id, self.groupInfo.name,
                self.groupInfo.id, self.siteInfo.name,
                self.siteInfo.id, self.userInfo.name,
                self.userInfo.id)
        else:
            retval = '%s (%s) left %s (%s) on %s (%s).' % (
                self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.groupInfo.name, self.groupInfo.id,
                self.siteInfo.name, self.siteInfo.id)
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event groupserver-group-member-%s' % self.code
        retval = ''
        # --=mpj17=-- Sometimes this is false. I do not know why.
        if self.groupInfo.id:
            retval = '<span class="%s">Left %s</span>' % \
                (cssClass, groupInfo_to_anchor(self.groupInfo))

            if self.adminRemoved:
                retval = '%s &#8212; removed by %s' % \
                    (retval, userInfo_to_anchor(self.userInfo))
                retval = '%s (%s)' % \
                    (retval, munge_date(self.context, self.date))
        return retval


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
        cssClass = 'audit-event groupserver-group-member-%s' % self.code
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
