.. Copyright (C) 2019, Nokia

.. image:: https://travis-ci.org/nokia/sphinx-invoke.svg?branch=master
    :target: https://travis-ci.org/nokia/sphinx-invoke

Documentation
-------------

Documentation for sphinx-invoke can be found from `Read The Docs`_.

.. _Read The Docs: http://sphinx-invoke.readthedocs.io/

Sphinx directive for invoke tasks
---------------------------------

The package *sphinx-invoke* contains the Sphinx directive which produces the
usage and help for the invoke task.

For example::

  .. invoke::
       :module: module.path.to.tasks
       :prog: programname

Essentially produces sections for each task with the content::

  programname -h taskname

.. note::

  This directive supports only **invoke==0.12.2**.

Installation
------------

The package can be installed with pip::

  # pip install sphinx-invoke

Development practices
---------------------

The development and the testing follows the Common Robot Libraries development
practices defined in crl-devutils_.

.. _crl-devutils: http://crl-devutils.readthedocs.io/.
