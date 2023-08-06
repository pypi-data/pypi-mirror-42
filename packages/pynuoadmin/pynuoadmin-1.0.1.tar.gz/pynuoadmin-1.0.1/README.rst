==================
NuoDB - Pynuoadmin
==================

.. contents::

This package enables the nuoadmin client management of a NuoDB database
without the need to install the full NuoDB product distribution on a
client machine.

Requirements
------------

* Python -- one of the following:

  - CPython_ >= 2.7

* NuoDB -- one of the following:

  - NuoDB_ >= 3.3.1


If you haven't done so already, and plan to use pynuoadmin with the NuoDB
Community Edition, visit `Download and Install NuoDB`_.

Installation
------------

The last stable release is available on PyPI and can be installed with
``pip``::

    $ pip install 'pynuoadmin[completion]'
    $ eval "$(register-python-argcomplete nuocmd)"

We recommend installing using the "completion" module, to enable command
line argument completion.

Alternatively (e.g. if ``pip`` is not available), a tarball can be downloaded
from GitHub and installed with Setuptools::

    $ curl -L https://github.com/nuodb/nuodb-pynuoadmin/archive/master.tar.gz | tar xz
    $ cd nuodb-pynuoadmin*
    $ python setup.py install

The folder nuodb-pynuoadmin* can be safely removed after installation.

Example
-------

Run the following command to confirm the pynuoamdin package is installed
properly::

    $ nuocmd show domain


Resources
---------

NuoDB Documentation: http://doc.nuodb.com/Latest/Default.htm

License
-------

Pynuoadmin is licensed under a `BSD 3-Clause License`_.

.. _BSD 3-Clause License: https://github.com/nuodb/nuodb-python/blob/master/LICENSE
.. _Download and Install NuoDB: https://www.nuodb.com/dev-center/community-edition-download
.. _NuoDB: https://www.nuodb.com/
.. _CPython: https://www.python.org/
