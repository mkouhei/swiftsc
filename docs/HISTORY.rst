History
-------

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

