History
-------

0.7.0 (2015-08-30)
^^^^^^^^^^^^^^^^^^

* Support Python 3.50-rc2.
* Discard the functions not related Client class.
* Supports Identity API v3 of OpenStack KeyStone.
* Fixes serviceCatlog key for the public cloud using OpenStack.
* Changes development status.
* Change Sphinx theme to sphinx_rtd_theme.

0.6.5 (2015-05-17)
^^^^^^^^^^^^^^^^^^

* Changes HTTpretty to requests_mock

0.6.4 (2015-05-16)
^^^^^^^^^^^^^^^^^^

* Supports wheel
* Adds extras_require to setup.py
* Applies pep257
* Pins httpretty version to 0.8.6
* Workaround Read the docs theme
* Changed to generate requirements.txt automatically
* Adds basic usage new API

0.6.3 (2015-03-17)
^^^^^^^^^^^^^^^^^^

* Fail creating object from stdin

0.6.2 (2015-03-11)
^^^^^^^^^^^^^^^^^^

* Suppressed InsecureRequestWarning

0.6.1 (2015-03-09)
^^^^^^^^^^^^^^^^^^

* Fixed storage uri
* Supported PyPy
* Updated pre-commit hook script
* Applied inherited-members to Sphinx documentation
* Changed attribute of automodule

0.6.0 (2015-03-06)
^^^^^^^^^^^^^^^^^^

* Added new client API
* Added Sphinx documentation

0.5.5 (2014-11-19)
^^^^^^^^^^^^^^^^^^

* Appended argument timeout to change value


0.5.4 (2014-11-16)
^^^^^^^^^^^^^^^^^^

* Bump version

0.5.3 (2014-11-15)
^^^^^^^^^^^^^^^^^^

* Unsuppored Python3.2
* Fixed #12 Read timed out
* Integrated pylint, pychecker to tox
* Fixed dependencies
* Fixed almost violations of pylint

0.5.2 (2014-05-10)
^^^^^^^^^^^^^^^^^^

* refactoring
* support python 3.4, PyPI
* apply tox for unit test

0.5.1 (2013-11-06)
^^^^^^^^^^^^^^^^^^

* fixes fail to load _io module in Python 2.6
* support Python 2.6

0.5 (2013-07-27)
^^^^^^^^^^^^^^^^

* support input file from stdin pipe, redirect
* detect "python-magic" debian package in setup.py

0.4 (2013-06-13)
^^^^^^^^^^^^^^^^

* support Python 3.2, 3.3

0.3 (2013-06-03)
^^^^^^^^^^^^^^^^

* support auth of keystone

0.2.2 (2013-05-20)
^^^^^^^^^^^^^^^^^^

* support to ignore verifying the SSL certficate

0.2.1 (2013-05-17)
^^^^^^^^^^^^^^^^^^

* change api of retrieve_object(), response inserted boolean before content

0.2 (2013-05-10)
^^^^^^^^^^^^^^^^

* add is_object method
* change api of is_container, response is changed status code to boolean

0.1.3 (2013-05-08)
^^^^^^^^^^^^^^^^^^

* fixes the response is not invalid with Response.json in requests 1.0 later

0.1.2 (2013-05-07)
^^^^^^^^^^^^^^^^^^

* set default timeout as 5.0

0.1.1 (2013-05-05)
^^^^^^^^^^^^^^^^^^

* fixes failed to upload without "Content-Length" when uploading empty file

0.1 (2013-05-02)
^^^^^^^^^^^^^^^^

* first release

