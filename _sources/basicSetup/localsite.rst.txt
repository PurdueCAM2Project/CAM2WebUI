=======================
Viewing Website Locally
=======================

There are four steps to viewing the website locally.

.. _`Setup virtualenv`:

Virtualenv Setup
================

To simplify Python dependencies, use :code:`virtualenv`. This tool can be install with:

.. code-block:: bash

    $ pip install virtualenv

Then, create a new python virtual environment for python 3.6; make sure have python 3.6 installed before run this command:

.. code-block:: bash

    $ virtualenv -p `which python3.6` ~/<anyname>/

A virtual environment named :code:`<anyname>` will be created in home directory. To activate it:

.. code-block:: bash

    $ source ~/<anyname>/bin/activate

The :code:`bash` prompt will now begin with :code:`(<anyname>)`. To deactivate virtualenv:

.. code-block:: bash

    $ deactivate

Configuring Python Virtual Environment
======================================

`Setup virtualenv`_ and activate it. Then install requirements with

.. code-block:: bash

    $ pip install -r requirements.txt

If you are using Ubuntu, you may get compilation errors related to psycopg2. In this case, install the needed libraries with:

.. code-block:: bash

    $ sudo apt-get install libpq-dev python3-dev

Exporting Config vars
=====================

Django expects several environment variables on startup. For each required environment variable, execute

.. code-block:: bash

    $ export <VAR_NAME>=<value>


The required environment variables are:

===================================== ========
 Name                                 Value 
===================================== ========
 :code:`DJANGO_SECRET_KEY`            Give this variable a dummy value. 
 :code:`GITHUB_KEY`                   Retrieve this value from GitHub_.
 :code:`GITHUB_SECRET`                Retrieve this value from GitHub_.
 :code:`BASICAUTH_USERNAME`           Give this variable a dummy value. (you will need to enter it when accessing the local site) 
 :code:`BASICAUTH_PASSWORD`           Give this variable a dummy value. (you will need to enter it when accessing the local site) 
 :code:`GOOGLE_API_KEY`               Get it from team slack channel
 :code:`GOOGLE_LOGIN_KEY`             Get it from team slack channel
 :code:`GOOGLE_LOGIN_SECRET`          Get it from team slack channel 
 :code:`DATABASE_URL`                 Get it from team slack channel 
 :code:`EMAIL_HOST`                   Get it from team slack channel 
 :code:`EMAIL_PORT`                   Get it from team slack channel 
 :code:`EMAIL_HOST_USER`              Get it from team slack channel 
 :code:`EMAIL_HOST_PASSWORD`          Get it from team slack channel 
 :code:`RECAPTCHA_PRIVATE_KEY`        Get it from team slack channel 
 :code:`RECAPTCHA_SITE_KEY`           Get it from team slack channel 
 :code:`RECAPTCHA_TEST_PRIVATE_KEY`   Get it from team slack channel 
 :code:`RECAPTCHA_TEST_SITE_KEY`      Get it from team slack channel 
 :code:`IS_PRODUCTION_SITE`           False 
===================================== ========

.. note::

    It might be helpful to add these to a file that you can run whenever you need to export them to your environment. Just remember **DON'T COMMIT IT!**

.. note::

    If you want to disable basic authentication for the local site, remove :code:`BasicAuthMiddleware` from :code:`cam2webui/settings.py`.

Run Local Server
================

.. code-block:: bash

    $ python manage.py runserver


.. _`GitHub`: https://github.com/settings/applications/new
