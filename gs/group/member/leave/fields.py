# coding=utf-8
from zope.component import createObject
from zope.schema import Choice
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.XWFCore.XWFUtils import comma_comma_and
from Products.GSGroup.joining import GSGroupJoining, ANYONE, REQUEST, INVITE
from Products.CustomUserFolder.userinfo import userInfo_to_anchor

class LeaveFields(object):
    def __init__(self, groupInfo):
        self.groupInfo = groupInfo
        self.__rejoinAdvice = self.__leaveTerm = None
        self.__fields = self.__vocab = None
    
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
                #admins = self.groupInfo.group_admins
                admins = group_admins(self.groupInfo)
                self.__rejoinAdvice = u'to rejoin, you can apply to '\
                  u'%s at any time' % comma_comma_and([userInfo_to_anchor(a) for a in admins])
            elif joinability == INVITE:
                #admins = self.groupInfo.group_admins
                admins = group_admins(self.groupInfo)
                #self.__rejoinAdvice = u'to rejoin, you must be '\
                #  u'invited by %s' % comma_comma_and([userInfo_to_anchor(a) for a in admins], conj='or')
                self.__rejoinAdvice = u'to rejoin, you must be '\
                  u'invited by %s' % comma_comma_and([userInfo_to_anchor(a) for a in admins])
            else:
                self.__rejoinAdvice = u''
        return self.__rejoinAdvice
    
def group_admins(g):
    admins = g.groupObj.users_with_local_role('GroupAdmin')
    retval = [ createObject('groupserver.UserFromId', 
                    g.groupObj, a) for a in admins ]
    return retval
