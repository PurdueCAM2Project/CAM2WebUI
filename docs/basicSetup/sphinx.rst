============================
Sphinx-generated Github Page
============================

This page will give a tutorial of creating Github page with sphinx supporting both *reStructuredText* and *MarkDown* markup language. See `Sphinx Official Website`_ for more detail about Sphinx

Environment Setup
=================
Sphinx is a python based tool, all relevant installation will go through :code:`pip`. In general, we need to install sphinx core, a sphinx theme, and a *MarkDown* parser:

.. code-block:: bash

    $ pip install sphinx==1.5.6
    $ pip install sphinx_rtd_theme
    $ pip install recommonmark

.. note::
    
    since :code:`recommonmark` MarkDown parser has a poor support with sphinx 1.6+. Use sphinx 1.5+ before :code:`recommonmark` support sphinx 1.6+

A recommended way to install these packages is putting them into a :code:`requirements.txt` under docs folder of project root directory, and execute:

.. code-block:: bash

    $ pip install -r requirements.txt


Sphinx Configuration
====================
for initial set up of sphinx folders, execute:

.. code-block:: bash

    $ sphinx-quickstart

this command will guide you initial set up of sphinx document source folder. Most of options can be left default, except a *GithubPage* option should be set to True. After finishing initial setup, open and modify :code:`conf.py`. 


Add Sphinx RTD theme
--------------------

#. import sphinx RTD theme library

    .. code-block:: python
    
        import sphinx_rtd_theme

#. set sphinx theme to RTD

    .. code-block:: python
    
        html_theme = "sphinx_rtd_theme"
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

#. set sphinx theme option

    .. code-block:: python
    
        html_theme_options = {
            'display_version': False,
            'navigation_depth': 2,
        }
    
for more Sphinx rtd theme settings, see `Sphinx rtd github repo`_


Add Sphinx MarkDown Support
---------------------------

#. import markdown parser library

    .. code-block:: python
    
        from recommonmark.parser import CommonMarkParser
        from recommonmark.transform import AutoStructify

#. Change :code:`source_suffix` to following to make parser recognize markdown files

    .. code-block:: python
    
        source_suffix = ['.rst', '.md']
    
#. add following configuration to make use of markdown parser
    
    .. code-block:: python 
    
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


.. code-block:: rst

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

.. code-block:: bash

    $ make html

if you didn't change settings during initial setup, a folder named :code:`_build` will show up, inside this folder, there is a :code:`html` folder. Open :code:`index.html` and you should be able to view documentation webpage locally.

.. note::

    if you modify some files and rebuild documentation page, but didn't see any changes, clean temperary build files by running 
    
    .. code-block:: bash
    
        $ make clean


Deploy to Github Page
=====================


.. _`Sphinx Official Website`: http://www.sphinx-doc.org
.. _`Sphinx rtd github repo`: https://github.com/rtfd/sphinx_rtd_theme
.. _`Recommonmark Documentation`: https://recommonmark.readthedocs.io/en/latest/
.. _`Sphinx TOC tree Docs`: http://www.sphinx-doc.org/en/stable/markup/toctree.html
.. _`rst reference`: http://docutils.sourceforge.net/docs/user/rst/quickref.html
