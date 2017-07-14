============================
Sphinx-generated Github Page
============================

This page will give a tutorial of creating Github page with sphinx supporting both *reStructuredText* and *MarkDown* markup language. See `Sphinx Official Website`_ for more detail about Sphinx

Environment Setup
=================
Sphinx is a python based tool, all relevant installation will go through :code:`pip`. In general, we need to install sphinx core, a sphinx theme, and a *MarkDown* parser:

.. code-block :: bash

    $ pip install sphinx==1.5.6
    $ pip install sphinx_rtd_theme
    $ pip install recommonmark

.. note ::
    
    since :code:`recommonmark` MarkDown parser has a poor support with sphinx 1.6+. Use sphinx 1.5+ before :code:`recommonmark` support sphinx 1.6+

A recommended way to install these packages is putting them into a :code:`requirements.txt` under docs folder of project root directory, and execute:

.. code-block :: bash

    $ pip install -r requirements.txt


Sphinx Configuration
====================

Initial Sphinx Set up
---------------------

for initial set up of sphinx folders, execute:

.. code-block :: bash

    $ sphinx-quickstart

this command will guide you initial set up of sphinx document source folder. Most of options can be left default, except a *GithubPage* option should be set to True. After finishing initial setup, open and modify :code:`conf.py`. 

.. _gitignore:

Add build folder to gitignore
-----------------------------

After finishing setup, some build folders should be ignored during git commit. By default, these folders are

.. code-block :: bash

    # sphinx document build folders
    path_to_sphinx_root/_build/
    path_to_sphinx_root/_static/
    path_to_sphinx_root/_templates/


Add Sphinx RTD theme
--------------------

1. import sphinx RTD theme library

.. code-block :: python

    import sphinx_rtd_theme

2. set sphinx theme to RTD

.. code-block :: python

    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

3. set sphinx theme option

.. code-block :: python

    html_theme_options = {
        'display_version': False,
        'navigation_depth': 2,
    }
    
for more Sphinx rtd theme settings, see `Sphinx rtd github repo`_


Add Sphinx MarkDown Support
---------------------------

1. import markdown parser library

.. code-block :: python

    from recommonmark.parser import CommonMarkParser
    from recommonmark.transform import AutoStructify

2. Change :code:`source_suffix` to following to make parser recognize markdown files

.. code-block :: python

    source_suffix = ['.rst', '.md']
    
3. add following configuration to make use of markdown parser
    
.. code-block :: python 

    source_parsers = {
        '.md': CommonMarkParser,
    }
    
    def setup(app):
        app.add_config_value('recommonmark_config', {
            'enable_eval_rst': True,
        }, True)
        app.add_transform(AutoStructify)

if you want to modify setup of recommonmark markdown parser, refer to `Recommonmark Documentation`_


Index.rst setup
---------------

Although :code:`recommonmark` support sphinx markdown parsing, it still lack of some functionality. One of them is :code:`toctree` which allow you to see documentation structure on the left-hand side of webpage. To enable :code:`toctree`, we need to write index file in :code:`rst` format. The :code:`index.rst` will contain only documentation title (automatically generated during initial setup) and files need to contain in the :code:`toctree` sections. a sample format is as below


.. code-block :: rst

    .. toctree::
       :glob:
       :caption: section title
       
       docsFolderName/*
       docFileName1.md
       docFileName2.rst

As code sample above, document files can be found with regular express pattern matching. This is accomplished by :code:`:glob:` attribute. It avoids adding document file name to index every time a new file is created, but files that failed in pattern matching still need to be added manually. For more information of how to write :code:`toctree`, see `Sphinx TOC tree Docs`_


Write Documentation
===================

Generally, writing :code:`rst` format documents is recommended for sphinx. If you want still using markdown. Following some rules to make sphinx parser generate :code:`toctree` correctly.

#. Every Document Starts with :code:`#`, a title for this documentation
#. Use :code:`##` for subsection, use :code:`###` as further section division
#. If document contains table, you may want to swtich to :code:`rst` (current sphinx markdown parser doesn't support table parsing), see `rst reference`_ to know how to write reStructuredTest Document.

.. note::
    
    you may not use github wiki page editor preview to determine which markdown :code:`#` title level you should use, since github will render major :code:`#` header really large.

After creating a document, make sure your new document file name is in :code:`index.rst` or satisfying any pattern matching in any :code:`toctree` section. Otherwise, readers are not able to navigate to your page (**In order word, your documents are useless**)

Locally View Documentation
==========================

Before pushing your documents to repository, viewing them locally to make sure it displays as expected and check no any typo. To do so, simply execute following command in sphinx root directory (not project root directory)

.. code-block :: bash

    $ make html

if you didn't change settings during initial setup, a folder named :code:`_build` will show up, inside this folder, there is a :code:`html` folder. Open :code:`index.html` and you should be able to view documentation webpage locally.

.. note ::

    When you modify some files and rebuild documentation page, but didn't see any changes, clean temperary build files by running 
    
    .. code-block :: bash
    
        $ make clean


Deploy to Github Page
=====================

Since obtaining Sphinx Documentation requires a build step, there are two ways to deploy built sphinx page to Github page. One is using some automatic built services (like Travis-CI) which will automatically build and deploy for you. The other is built locally yourself.


Deploy with Travis-CI
---------------------

Deploy with Travis-CI basically needs 4 steps:

1. modify :code:`.travis.yml` configuration by adding the following (only works in python environment). For more information about travis github page deployment, see `Travis Configuration`_

.. code-block :: bash

    install:            # Install requirement as "Environment Setup Section"
    - pip install -r sphinx_root/requirements.txt
    script:             # build sphinx document
    - cd sphinx_root/
    - make html
    - cd -
    deploy              # deploy to github page
    - provider: pages
      skip_cleanup: true
      local_dir: sphinx_root/_build/html
      github_token: $GITHUB_TOKEN # Set in travis-ci.org dashboard


2. Obtain Github personal token. 
   This Token can be anyone who has access right to Repository. To obtain this token, Go to personal Github settings, At very end of left column, click *personal access tokens* and create a new one. With regards to Scope option during token creation, only :code:`public_repo` should be selected for safety.  Put this token in Travis-CI environment variable settings with name corresponding to travis script

.. note::
    
    Whoever use their own *personal access token*, every auto deployment commit will be treated as their commit. For a team, it's recommended to use tokens from organization

3. Change repository settings
   repository manager should change github page source to branch :code:`gh-pages` branch. This branch will be created during auto deployment by default. 

.. note::

    :code:`gh-pages` branch can't be a protected branch, otherwise, Travis-CI won't be able to push to repository.


Locally built and deploy by push
--------------------------------

Deploy by github push needs 6 steps:

1. create a :code:`source` directory inside docs folder of repo root directory and move everything in sphinx root to new folder

2. allow git to track sphinx temp file by removing these lines shown gitignore_ section

3. Change Sphinx build path to parent directory of sphinx root directory by changing two lines in :code:`Makefile` and :code:`make.bat`:

.. code-block:: bash

    # in Makefile
    BUILDDIR=_build        ->       BUILDDIR=..
    # in make.bat
    set BUILDDIR=_build    ->       set BUILDDIR=..

4. execute following command to move files to docs folder in *root docs directory*

.. code-block :: bash

    $ mv html/* ./

.. note ::

    if this command reports error, there are several possibilities:

    1. didn't build document with :code:`make html`
    2. execute in wrong directory.
    3. may need to clean the *root docs directory*, only leave *source* folder there and *html* folder there

5. commit every change in docs folder and push it to github

6. (only needs to be done once) change github repo github page settings, make source to be *master branch /docs folder*




.. _`Sphinx Official Website`: http://www.sphinx-doc.org
.. _`Sphinx rtd github repo`: https://github.com/rtfd/sphinx_rtd_theme
.. _`Recommonmark Documentation`: https://recommonmark.readthedocs.io/en/latest/
.. _`Sphinx TOC tree Docs`: http://www.sphinx-doc.org/en/stable/markup/toctree.html
.. _`rst reference`: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _`Travis Configuration`: https://docs.travis-ci.com/user/deployment/pages/
