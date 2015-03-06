# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013-2015 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import unittest
from httpretty import HTTPretty, httprettified
from swiftsc import utils as u
from swiftsc import client as c
from swiftsc.tests import test_vars as v


class UtilsTests(unittest.TestCase):
    """
    Unit test of utils.py
    """

    @httprettified
    def test_return_json(self):
        """
        test return json
        """
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/' % (v.STORAGE_URL,
                                           v.CNTR_NAME),
                               body=v.OBJECTS_JSON.encode('utf-8'))
        res = c.list_objects(v.TOKEN, v.STORAGE_URL, v.CNTR_NAME)
        self.assertTrue(isinstance(res, list))

    def test_check_mimetype(self):
        """
        test checking mimetype
        """
        self.assertEqual(v.TEST_FILE_MIMETYPE,
                         u.check_mimetype(v.TEST_FILE))

    def test_check_mimetype_buffer(self):
        """
        test checking mimetype of buffer
        """
        fileobj = open(v.TEST_FILE, 'rb')
        self.assertEqual(v.TEST_FILE_MIMETYPE,
                         u.check_mimetype_buffer(fileobj))
        fileobj.close()

    def test_retrieve_info_from_buffer(self):
        """
        test retriving info from buffer
        """
        fileobj = open(v.TEST_FILE, 'rb')
        file_content = fileobj.read()
        fileobj.seek(0)
        self.assertEqual((v.TEST_FILE_MIMETYPE,
                          v.TEST_FILE_SIZE,
                          file_content),
                         u.retrieve_info_from_buffer(fileobj))
        fileobj.close()
