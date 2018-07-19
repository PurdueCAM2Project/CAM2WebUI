============================
Travis CI Setup
============================

Travis CI is a continuous integration testing service used to build and test software projects hosted at GitHub

Connect Travis CI with Github
=============================

To connect Travis with Github Repository, There are several steps (repository admin permission is necessary):

#. Go to repository main page, click on *Settings* tab.
#. Click on *Integration & Service* on menu.
#. Click on *Add Service* drop-down menu and select *Travis CI*.
#. Sign in `Travis CI Website`_ with Github account.
#. Once sign in, click on *account* at top right corner of web page.
#. At this page, repositories under this github account will be shown, select checkbox of corresponding repository. 
#. Create a Travis configuration file :code:`.travis.yml` at root directory of repository.
#. Start writing configuration file and testing script will be triggered on every push to Github or based on configuration.

.. note::

    While Travis CI for public github repository is free, it doesn't work with private repository. To use Travis CI for private repository, go to `Travis CI Pro Website`_, purchase plans, and follow the instructions above.

Travis CI Configuration File
=============================

Travis scripts can be generally devided into following groups:

- Environment selection
- pre-test scripts and installation
- testing scripts
- deployment
- Notifications

Details of each part will be explained in following sections

Environment Selection
---------------------

Travis CI is basically a remote ubuntu or osx machine that runs testing code in repository with testing scripts provided in travis configuration file. Therefore, selecting environment is analogous to choose the operating system and language you would like to use for testing environment. With respect to cam2 project, ubuntu environment and python are used, so the configuration file is as follow:

.. code-block :: bash

    dist: trusty
    language: python
    python:
    - '3.6.1'

The :code:`dist` infers version of OS, a detailed table is provided on `Travis Build Environment Overview`_

pre-test scripts and installation
---------------------------------

Before running of testcases, all the dependent software needs to be installed and correctly configured. In general, there are four sections to used for this steps, they are:

#. addons
#. before_install
#. before_script
#. install

the :code:`addons` section is used for Travis CI built-in packages and configuration such as Firefox, MariaDB, Ubuntu package manager APT, etc. The rest of three are run in the order as listed above. In general there is no specific difference among these three section except naming. All the normal Ubuntu apt command and bash command can be run in all of three sections. Usually, based on the naming convention of each section, :code:`before_install` can be used for install basic packages, :code:`before_script` can be used for configure the packages installed or downloaded at :code:`before_install` section and :code:`install` section is used for install rest of packages before using any testing scripts.

In our specific case, we need Firefox as dependency. So we add the Firefox in the addons sections, and specify the version of Firefox we want:

.. code-block :: bash

    addons: 
      firefox: "56.0"

The reason of fixing the version of Firefox browser will be explained later. In addition to Firefox, we also need :code:`xvfb` package and :code:`geckodriver` for Selenium testing. Since it's in apt repository and git repository, we use :code:`apt install` and :code:`wget` to install or download them.

.. code-block :: bash

    before_install:
    - sudo apt-get install xvfb
    - wget https://github.com/mozilla/geckodriver/releases/download/v0.19.0/geckodriver-v0.19.0-linux64.tar.gz

Here we comes the reason of specify version of Firefox. Since geckodriver only support some specific versions of Firefox. If we want to update the version of Firefox, we need to update the version of geckodriver as well.

Then, we need to configure these packages, unzip the geckodriver and move it to global library directory of Linux to be ready to use. We also need to configure xvfb, the detail of configuration of xvfb is given by `Travis CI xvfb Configuration`_. The sample code is as follow:

.. code-block :: bash

    - sudo tar -xzf geckodriver-v0.19.0-linux64.tar.gz -C /usr/bin
    - sudo chmod a+x /usr/bin/geckodriver
    - export DISPLAY=:99.0
    - sh -e /etc/init.d/xvfb start
    - sleep 5 # give xvfb some time to start

testing scripts
---------------

After setup all the packages, the testing is actually very easy, put all the testing command executed locally here and wait for the testing result. 

.. note::

    Any failure in this section will be considered the failure of whole testing, resulting the termination of deployment section

To reduce the amount of random failure of testing scripts, Travis provided a prefix :code:`travis_retry`. In fact, all the command script in the sections above can use this prefix. In general the command with this prefix will be retry for several times if it fails. The default retry times is three. You can also modify it as you want. The detail documents of :code:`travis_retry`  and advanced method to eliminate timeout failure are on `Timeouts installing dependencies`_ section.

deployment
----------

After testing success, having Travis automatically deploy code for us is a good choice. To do that, we need to first find out if Travis support the cloud platform we want to use. See `Supported Providers`_ for details.

Each platform has its own configuration. However, there is one useful configuration that is pervasive throughout all platform. It's the :code:`app` section. In this section, you can specify which specific branch you want to deploy and which one you don't want, since if the testing code is on a feature branch, you don't want it to deploy to the production site app.  

Notifications
-------------

Once you have finished all the Travis CI configuration. After you finish one push, it's the time you can have some rest. However, if your test script is very complicated, you may want Travis to norify you whenever testing is finished with success or failure. Travis CI does have its own notification system. The default nofitication is sent to your github email. However, you can configure it to different social app or team management app like *Slack*. To know how to configure it, see `Travis CI Notifications`_.



.. _`Travis CI Website`: https://travis-ci.org/
.. _`Travis CI Pro Website`: https://travis-ci.com/
.. _`Travis Build Environment Overview`: https://docs.travis-ci.com/user/reference/overview/
.. _`Travis Configuration`: https://docs.travis-ci.com/user/deployment/pages/
.. _`Travis CI xvfb Configuration`: https://docs.travis-ci.com/user/gui-and-headless-browsers/#Using-xvfb-to-Run-Tests-That-Require-a-GUI
.. _`Timeouts installing dependencies`: https://docs.travis-ci.com/user/common-build-problems/#Timeouts-installing-dependencies
.. _`Supported Providers`: https://docs.travis-ci.com/user/deployment/
.. _`Travis CI Notifications`: https://docs.travis-ci.com/user/notifications/
