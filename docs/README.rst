===================================================
swiftsc is simple client library of OpenStack Swift
===================================================

This tool is simple client library of OpenStack Swift.
This tool is intended to be used in the module and Python script other.
The main purpose of this tool is used as a core module for backup tool.


Requirements
------------

* Python 2.7 or Python 3.2
* requires 0.12.1
* python-magic 5.x of debian package or python-magic 0.4.x of PyPI


Setup
-----
::

   $ git clone https://github.com/mkouhei/swiftsc
   $ cd swiftsc
   $ sudo python setup.py install


Contribute
----------

Firstly copy pre-commit hook script.::

   $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Next install python2.7 later, and python-requests, py.test. Below in Debian GNU/Linux Sid system,::

   $ sudo apt-get install python python-requests python-pytest pep8 python-magic python3 python3-requests python3-pytest

Then checkout 'devel' branch for development, commit your changes. Before pull request, execute git rebase.


See also
--------

* `OpenStack Object Storage Developer Guide <http://docs.openstack.org/api/openstack-object-storage/1.0/content/index.html>`_
* `Requests <http://ja.python-requests.org/en/latest/>`_

