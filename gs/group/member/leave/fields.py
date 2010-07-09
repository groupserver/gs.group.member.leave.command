# coding=utf-8
from zope.formlib.form import Fields
from zope.schema import Choice
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.XWFCore.XWFUtils import comma_comma_and
from Products.GSGroup.joining import GSGroupJoining, ANYONE, REQUEST, INVITE

class LeaveFields(object):
    def __init__(self, groupInfo):
        self.groupInfo = groupInfo
        self.__rejoinAdvice = self.__leaveTerm = None
        self.__fields = self.__vocab = None
    
    def __call__(self, context):
        return self.fields
    
    @property
    def fields(self):
        if self.__fields == None:
            self.__fields = Fields(Choice(
              title=u'Change Subscription',
              description=u'These options are shown to a group member '\
                u'wishing to leave the group',
              required=True,
              vocabulary=self.vocab))
        return self.__fields
    
    @property
    def vocab(self):
        retval = SimpleVocabulary([
          self.leaveTerm,
          SimpleTerm('web',   'web',    u'Read posts on the web (no email)'),
          SimpleTerm('digest','digest', u'Receive a digest of topics '\
            u'(maximum one email per day)')])
        return retval
    
    @property
    def leaveTerm(self):
        if self.__leaveTerm == None:
            title = u'Leave %s (%s)' % (self.groupInfo.name, self.rejoinAdvice)
            self.__leaveTerm = SimpleTerm('leave', 'leave',  title)
        return self.__leaveTerm
    
    @property
    def rejoinAdvice(self):
        if self.__rejoinAdvice == None:
            joinability = GSGroupJoining(self.groupInfo.groupObj).joinability
            if joinability == ANYONE:
                self.__rejoinAdvice = u'you can rejoin at any time'
            elif joinability == REQUEST:
                admins = self.groupInfo.group_admins
                self.__rejoinAdvice = u'to rejoin, you can apply to '\
                  u'%s at any time' % comma_comma_and(admins)
            elif joinability == INVITE:
                admins = self.groupInfo.group_admins
                self.__rejoinAdvice = u'to rejoin, you must be '\
                  u'invited by %s' % comma_comma_and(admins, conj='or')
            else:
                self.__rejoinAdvice = u''
        return self.__rejoinAdvice
    
    