===================================================
swiftsc is simple client library of OpenStack Swift
===================================================

This tool is simple client library of OpenStack Swift.
This tool is intended to be used in the module and Python script other.
The main purpose of this tool is used as a core module for backup tool.


Requirements
------------

* Python 2.7 or Python 3.2
* requests 0.12.1 later
* python-magic 5.x in debian package or python-magic 0.4.x of PyPI


Setup
-----
::

   $ git clone https://github.com/mkouhei/swiftsc
   $ cd swiftsc
   $ sudo python setup.py install


Development
-----------

Firstly copy pre-commit hook script.::

   $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Debian systems
^^^^^^^^^^^^^^

Next install python2.7 later, and python-requests, python-magic, py.test, mock, pep8. Below in Debian GNU/Linux Sid system,::

   $ sudo apt-get install python python-requests python-pytest pep8 python-magic python-mock

Then checkout 'devel' branch for development, commit your changes. Before pull request, execute git rebase.

Apply debian patch with dquilt as follwoing when making debian package.::

  $ dquilt diff
  Index: swiftsc-0.x.x/setup.py
  ===================================================================
  --- swiftsc-0.x.x.orig/setup.py 2013-05-08 23:53:17.000000000 +0900
  +++ swiftsc-0.x.x/setup.py      2013-05-09 11:01:52.231198152 +0900
  @@ -39,7 +39,7 @@
           open(os.path.join("docs","TODO.rst")).read() + \
           open(os.path.join("docs","HISTORY.rst")).read()
 
  -requires = ['setuptools', 'requests', 'python-magic']
  +requires = ['setuptools', 'requests']
 
  (snip)


See also
--------

* `OpenStack Object Storage Developer Guide <http://docs.openstack.org/api/openstack-object-storage/1.0/content/index.html>`_
* `Requests <http://ja.python-requests.org/en/latest/>`_

