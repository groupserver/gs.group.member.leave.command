Changelog
=========

4.0.1 (2015-01-30)
------------------

* Fixing the group-URL and email address in the ``mailto:`` of
  the *Not a member* notification

4.0.0 (2014-09-03)
------------------

* Adding an HTML form of the *You have left* notification
* Adding an HTML form of the *Member has left* notification
* Adding a list command

  + Refactor ``leave_group`` into a function
  + Further PEP-8 OCD changes.

3.0.3 (2014-07-11)
------------------

* Following ``gs.content.form`` to ``gs.content.form.base``

3.0.2 (2013-10-09)
------------------

* Switching to the new ``del_group`` method of the ucstom user.
* Using the correct Home icon.

3.0.1 (2013-08-09)
------------------

* Updating the license and copyright.

3.0.0 (2013-05-20)
------------------

* Moving the leave-link to ``gs.group.member.info``.
* Adding breadcrumbs, and bringing the page up-to-date with the
  current style.
* Further (PEP-8) code cleanup.

2.0.3 (2012-09-20)
------------------

* Minor (PEP-8) code cleanup, thanks to Ninja-IDE

2.0.2 (2012-07-12)
------------------

* Switching the *Leave* page to be full-page.

2.0.1 (2012-06-22)
------------------

* Update to the SQL Alchemy

2.0.0 (2012-02-24)
-------------------

* Fixing the auditor, and adding the *group leave* event
* Tidying the Leave page, and fixing the ``__init__`` of the ``Leaver``

1.0.4 (2011-05-23)
------------------

* Updating the *Leave* page to use the standard message content-provider
* Changing the permissions on the *Leave* link.

1.0.3 (2010-10-07)
------------------

* Following the radio button to its new home.

1.0.2 (2010-09-23)
------------------

* Bug fixes
* New ``version.py``
* Tweaks to logging and notification
* Moved utility from ``gs.group.member.manage``, and it now
  checks for membership

1.0.1 (2010-08-12)
------------------

* Minor white-space update.

1.0.0 (2010-07-30)
------------------

* Created new product for leaving a group
* Moved the group-leaving-auditor from Products.GSGroupMember

