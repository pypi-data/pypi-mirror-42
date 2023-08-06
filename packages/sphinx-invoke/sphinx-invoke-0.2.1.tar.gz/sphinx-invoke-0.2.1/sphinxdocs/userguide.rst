.. Copyright (C) 2019, Nokia

User Guide
==========

Configuration
-------------

In *conf.py* add the Sphinx extension *sphinxinvoke.ext* to the *extensions*.

For example::

  extensions = ['sphinxinvoke.ext']

Usage in reST source
--------------------

The directive has the following options:

- *module* -- module.path.to.invoke.tasks

- *prog* -- the name of the program for tasks

For example provided :ref:`exampletasks` is the module
*sphinxinvoke.exampletasks*, then the invoke command line
reference for the tasks can be documented in the following fashion:

.. literalinclude:: ../tests/testdocs/cli.rst

.. _exampletasks:

Example tasks
-------------

.. literalinclude:: ../src/sphinxinvoke/exampletasks.py

Sphinx-build results of example
-------------------------------

The directive produces the document tree which is essentially the same
as which is produced by the following reST file:

.. literalinclude:: ../tests/testdocs/cli_expected.rst

This is interpreted finally (without the title) to the following:

.. invoke::
   :module: sphinxinvoke.exampletasks
   :prog: program
