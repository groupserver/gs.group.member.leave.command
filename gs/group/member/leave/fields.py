# coding=utf-8
from zope.component import createObject
from zope.schema import Choice
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.GSGroup.joining import GSGroupJoining

class LeaveFields(object):
    def __init__(self, groupInfo):
        self.groupInfo = groupInfo
        self.__leaveTerm = self.__fields = self.__vocab = None
    
    @property
    def fields(self):
        if self.__fields == None:
            self.__fields = Choice(
              __name__=u'changeSubscription',
              title=u'Want less email?',
              description=u'These options are shown to a group member '\
                u'wishing to leave the group',
              vocabulary=self.vocab,
              default='leave',
              required=False)
        return self.__fields
    
    @property
    def vocab(self):
        retval = SimpleVocabulary([
          self.leaveTerm,
          SimpleTerm('web', 'web', u'Read posts on the web (no email)'),
          SimpleTerm('digest', 'digest', u'Receive a digest of topics '\
            u'(maximum one email per day)')])
        return retval
    
    @property
    def leaveTerm(self):
        if self.__leaveTerm == None:
            rejoinAdvice = GSGroupJoining(self.groupInfo.groupObj).rejoin_advice
            title = u'Leave %s (%s)' % (self.groupInfo.name, rejoinAdvice)
            self.__leaveTerm = SimpleTerm('leave', 'leave', title)
        return self.__leaveTerm
