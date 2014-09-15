=========================
``gs.group.member.leave``
=========================
~~~~~~~~~~~~~~~~~~~~~~~~~
Leave a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-03-20
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

This part of the code deals with group members leaving groups,
whether voluntarily or as the result of an administrator's action.

A `Leave page`_ is provided, where a member who wishes to leave is
shown advice on rejoining, given the means to reduce the amount 
of email received from the group, and the ability to leave. 

The actual leaving code_ is separate from the page, so that it can be
called by other modules [#manage]_. This code also ensures that all
group-membership roles are removed from the member at the time of leaving,
and takes care of auditing the leave event.

Leave Page
==========

The *Leave* page is ``leave.html`` in the **groups** context. It is
necessary for this page to be outside the **group** context, otherwise the
former member would get a *Permission Denied* **after** he or she left a
*secret* group.

Rather than simply providing a button that removes the member from the
group, the *Leave* page presents the user a choice for reducing the amount
of email. The hypothesis is that members often leave because they get
overwhelmed by email. Giving the member the choice of going onto Topics
Digest or Web Only may reduce the numbers leaving.

Code
====

The code is not as sophisticated as the Joining User code. The
``gs.group.member.leave.GroupLeaver`` is created::

  leaver = GroupLeaver(self.groupInfo, self.loggedInUser)

Then the ``removeMember`` method is called::

  leaver.removeMember()

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.member.leave/
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#manage] See ``gs.group.member.manage``
             <https://source.iopen.net/groupserver/gs.group.member.manage/>

..  LocalWords:  html
