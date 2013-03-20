# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.member.viewlet import MemberViewlet


class LeaveLinkViewlet(MemberViewlet):
    def __init__(self, group, request, view, manager):
        MemberViewlet.__init__(self, group, request, view, manager)

    @Lazy
    def show(self):
        retval = self.isMember
        return retval
