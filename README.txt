Introduction
============

This part of the code deals with group members leaving groups,
whether voluntarily or as the result of an administrator's action.

A Leave page is provided, where a member who wishes to leave is
shown advice on rejoining, given the means to reduce the amount 
of email received from the group, and the ability to leave. 

The actual leaving code is separate from the page, so that it can
be called by other modules (such as gs.group.member.manage). This
code also ensures that all group-membership roles are removed from
the member at the time of leaving, and takes care of auditing the 
leave event.
