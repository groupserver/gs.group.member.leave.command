=================================
``gs.group.member.leave.command``
=================================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The email command to leave a group (unsubscribe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-06-15
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This part of the code deals with a group member leaving a group
using the email command_. It also provides the notification_ sent
to people when they use an unrecognised email address.

Command
=======

The *Unsubscribe* command removes someone from a group. It works
without confirmation removing someone immediately on receipt of a
message with ``Unsubscribe`` in the ``Subject`` header. This is
because many email providers send a *Unsubscribe* command when
someone clicks **Spam** on a message from a group [#sender]_, and
any email that asked for confirmation would look like spam. (The
behaviour of the *Unsubscribe* command is different to the
*Subscribe* command [#subscribe]_, which requires confirmation.)

The only complication is the notification_ which is sent out when
the email address in the ``From`` header does not match that of a
group member.

Notification
============

The *Not a member* notification is provided by this product. This
notification is sent to the person who tried to leave the group,
the email address failed to match a member.

Normally an address fails to match when

* The person has multiple email addresses, **and**
* Rewrite rules when receiving.

This is quite common in large organisations. For example someone
registers with ``a.person@example.com`` and this is rewritten to
``another-person@example.com``.
  
The message to support that is embedded in this notification is
the one that is most commonly seen by `OnlineGroups.net`_
support. (Provided by ``gs-group-member-leave-not-a-member.html``
in the **groups** context, not the group.)

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.group.member.leave.command/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

.. [#manage] See ``gs.group.member.manage``
   <https://github.com/groupserver/gs.group.member.manage/>
.. [#sender] The *Unsubscribe* command is sent when people click
   **Spam** because the command is listed in the
   ``List-Unsubscribe`` email header
   <https://github.com/groupserver/gs.group.list.sender/>
.. [#subscribe] See ``gs.group.member.subscribe``
             <https://github.com/groupserver/gs.group.member.subscribe/>

..  LocalWords:  html
