========
Heroku
========

This page will walk you through some project-specific tasks you might want to perform when using Heroku.

Using Heroku Site
=================

Staging and Production Server is automatically deployed by Travis-CI. 

`Staging Server`_ hold everything on master branch

`Production Server`_ hold everything on release branch

.. note::
    
    Staging Server can only be accessed with credential. See team slack channel pin to get access credential.

UI Team Leader Responsibilties
===============================

In general, only team leader has direct access to heroku server. There are several things should be done by team leader:

#. Update heroku environment variables
#. Revert to a functional version of deployment if sometimes production site failed

.. _`Staging Server`: http://cam2webui-staging.herokuapp.com
.. _`Production Server`: https://www.cam2project.net/
