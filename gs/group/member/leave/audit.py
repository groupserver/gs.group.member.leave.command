# coding=utf-8
from pytz import UTC
from datetime import datetime
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.XWFCore.XWFUtils import munge_date
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from Products.GSGroup.groupInfo import groupInfo_to_anchor
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, AuditQuery
from Products.GSAuditTrail.utils import event_id_from_data

SUBSYSTEM = 'gs.group.member.leave'
import logging
log = logging.getLogger(SUBSYSTEM)

UNKNOWN = '0'  # Unknown is always "0"
LEAVE = '1'


class LeaveAuditEventFactory(object):
    """A Factory for group leaving events.
    """
    implements(IFactory)

    title = u'GroupServer Leave Group Audit Event Factory'
    description = u'Creates a GroupServer event auditor for leaving groups'

    def __call__(self, context, event_id, code, date,
        userInfo, instanceUserInfo, siteInfo, groupInfo,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        """Create an event
        """
        assert subsystem == SUBSYSTEM, 'Subsystems do not match'

        if (code == LEAVE):
            event = LeaveEvent(context, event_id, date,
              userInfo, instanceUserInfo, siteInfo, groupInfo)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
              userInfo, instanceUserInfo, siteInfo, groupInfo,
              instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


class LeaveEvent(BasicAuditEvent):
    ''' An audit-trail event representing a user being removed
        from a group
    '''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo,
                  siteInfo, groupInfo):
        """Create a leave event
        """
        BasicAuditEvent.__init__(self, context, id, LEAVE, d, userInfo,
          instanceUserInfo, siteInfo, groupInfo, None, None, SUBSYSTEM)

    @property
    def adminRemoved(self):
        retval = False
        if self.userInfo.id and self.userInfo.id != self.instanceUserInfo.id:
            retval = True
        return retval

    def __str__(self):
        if self.adminRemoved:
            r = u'{0} ({1}) was removed from {2} ({3}) on {4} ({5}) by {6} '\
                u'({7}).'
            retval = r.format(self.instanceUserInfo.name,
                        self.instanceUserInfo.id, self.groupInfo.name,
                        self.groupInfo.id, self.siteInfo.name,
                        self.siteInfo.id, self.userInfo.name,
                        self.userInfo.id)
        else:
            retval = u'%s (%s) left %s (%s) on %s (%s).' % (
                self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.groupInfo.name, self.groupInfo.id,
                self.siteInfo.name, self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event groupserver-group-member-%s' % \
          self.code
        retval = ''
        # --=mpj17=-- Sometimes this is false. I do not know why.
        if self.groupInfo.id:
            retval = u'<span class="%s">Left %s</span>' % \
                (cssClass, groupInfo_to_anchor(self.groupInfo))

            if self.adminRemoved:
                retval = u'%s &#8212; removed by %s' % \
                            (retval, userInfo_to_anchor(self.userInfo))
                retval = u'%s (%s)' % \
                          (retval, munge_date(self.context, self.date))
        return retval


class LeaveAuditor(object):
    """An Auditor for leaving
    """
    def __init__(self, context, instanceUserInfo, groupInfo=None):
        """Create a leaving auditor.
        """
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
        eventId = event_id_from_data(self.userInfo,
          self.instanceUserInfo, self.siteInfo, code, instanceDatum,
          '%s-%s' % (self.groupInfo.name, self.groupInfo.id))

        e = self.factory(self.context, eventId, code, d,
          self.userInfo, self.instanceUserInfo, self.siteInfo,
          self.groupInfo, instanceDatum, None, SUBSYSTEM)

        self.queries.store(e)
        log.info(e)
        return e
