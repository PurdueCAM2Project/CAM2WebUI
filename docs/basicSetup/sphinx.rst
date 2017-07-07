============================
Sphinx-generated Github Page
============================

This page will give a tutorial of creating Github page with sphinx supporting both *reStructuredText* and *MarkDown* markup language. See `Sphinx Official Website`_ for more detail about Sphinx

Environment Setup
=================
Sphinx is a python based tool, all relevant installation will go through :code:`pip`. In general, we need to install sphinx core, a sphinx theme, and a *MarkDown* parser:

.. code-block:: bash

    pip install sphinx==1.5.6
    pip install sphinx_rtd_theme
    pip install recommonmark

.. note::
    
    since :code:`recommonmark` MarkDown parser has a poor support with sphinx 1.6+. Use sphinx 1.5+ before :code:`recommonmark` support sphinx 1.6+

A recommended way to install these packages is putting them into a :code:`requirements.txt` under docs folder of project root directory, and execute:

.. code-block:: bash

    pip install -r requirements.txt


Sphinx Configuration
====================

Write Documentation
===================

Locally View Documentation
==========================

Deploy to Github Page
=====================


.. _`Sphinx Official Website`: http://www.sphinx-doc.org
