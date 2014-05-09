===================================================
swiftsc is simple client library of OpenStack Swift
===================================================

This tool is simple client library of OpenStack Swift.
This tool is intended to be used in the module and Python script other.
The main purpose of this tool is used as a core module for backup tool.

.. image:: https://secure.travis-ci.org/mkouhei/swiftsc.png?branch=devel
   :target: http://travis-ci.org/mkouhei/swiftsc
.. image:: https://coveralls.io/repos/mkouhei/swiftsc/badge.png?branch=devel
   :target: https://coveralls.io/r/mkouhei/swiftsc?branch=devel
.. image:: https://pypip.in/v/swiftsc/badge.png
   :target: https://crate.io/packages/swiftsc


Requirements
------------

* Python 2.7 over or Python 3.2 over
* requests 0.12.1 later
* python-magic 5.x in debian package or python-magic 0.4.3 later of PyPI


Setup
-----
::

   $ git clone https://github.com/mkouhei/swiftsc
   $ cd swiftsc
   $ sudo python setup.py install

workaround of Python 3.3
^^^^^^^^^^^^^^^^^^^^^^^^

When not using debian package of python-magic, current version(0.4.3) is not support python 3.3. Python 3.3 is supported by committed after one of the tag of 0.3.

https://github.com/ahupp/python-magic/commit/d033eb46a8ace66cf795c54168a197228e47ce9e

So you must install from github until next version will release.::

  $ git clone https://github.com/ahupp/python-magic
  $ cd python-magic
  $ sudo python setup.py install
  $ cd
  $ git clone https://github.com/mkouhei/swiftsc
  $ cd swiftsc
  $ sudo python setup.py install

Development
-----------

Firstly copy pre-commit hook script.::

   $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Debian systems
^^^^^^^^^^^^^^

Next install python2.7, python3.2 later, and python-requests, python-magic, python-tox, pychecker. Below in Debian GNU/Linux Sid system,::

   $ sudo apt-get install python python-requests python-pytest pep8 python-magic python-tox pychecker

Then checkout 'devel' branch for development, commit your changes. Before pull request, execute git rebase.


See also
--------

* `OpenStack Object Storage Developer Guide <http://docs.openstack.org/api/openstack-object-storage/1.0/content/index.html>`_
* `Requests <http://ja.python-requests.org/en/latest/>`_

