=========================
``gs.group.member.leave``
=========================
~~~~~~~~~~~~~~~~~~~~~~~~~
Leave a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-10-10
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This part of the code deals with group members leaving groups,
whether voluntarily or as the result of an administrator's
action.

A `Leave page`_ is provided, where a member who wishes to leave
is shown advice on rejoining, given the means to reduce the
amount of email received from the group, and the ability to
leave.

The actual leaving code_ is separate from the page, so that it
can be called by other modules [#manage]_. This code also ensures
that all group-membership roles are removed from the member at
the time of leaving, and takes care of auditing the leave event.

Leave Page
==========

The *Leave* page is ``leave.html`` in the **groups** context. It
is necessary for this page to be outside the **group** context,
otherwise the former member would get a *Permission Denied*
**after** he or she left a *secret* group.

Rather than simply providing a button that removes the member
from the group, the *Leave* page presents the user a choice for
reducing the amount of email. The hypothesis is that members
often leave because they get overwhelmed by email. Giving the
member the choice of going onto Topics Digest or Web Only may
reduce the numbers leaving.

Code
====

The code is not as sophisticated as the Joining User code. The
``gs.group.member.leave.GroupLeaver`` is created:

.. code-block:: python

  leaver = GroupLeaver(self.groupInfo, self.loggedInUser)

Then the ``removeMember`` method is called:

.. code-block:: python

  leaver.removeMember()

More useful is the ``leave_group`` utility function, which is
used by the user-interfaces to remove a person from a group and
people that the member has left.

.. code-block:: python

  leave_group(self.groupInfo, userInfo, self.request)

The ``request`` is necessary so the notifications_ can be
rendered.

Notifications
=============

Two notifications are provided by this product. The *You have
left* notification (``gs-group-member-leave-notification.html``
in the group context) tells the former member that he or she has
left. It is sent from the **Support** email address, which is
quite important: if it comes from the group that has been left
then it is (highly) likely to be marked as spam.

The *Member has left* notification
(``gs-group-member-leave-left.html`` inthe group context) is sent
to the group administrators telling them that the member has
left.

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.member.leave/
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

.. [#manage] See ``gs.group.member.manage``
             <https://github.com/groupserver/gs.group.member.manage/>

..  LocalWords:  html
