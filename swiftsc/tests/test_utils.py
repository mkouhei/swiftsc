# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013 Kouhei Maeda <mkouhei@palmtb.net>

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

    @httprettified
    def test_return_json(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/' % (v.storage_url,
                                           v.cntr_name),
                               body=v.objects_json.encode('utf-8'))
        res = c.list_objects(v.token, v.storage_url, v.cntr_name)
        self.assertTrue(isinstance(res, list))

    def test_generate_uri(self):
        self.assertEqual(u.generate_url(v.partial_uri_list_2), v.auth_url)
        self.assertEqual(u.generate_url(v.partial_uri_list_3),
                         v.auth_ver_url)

    def test_check_mimetype(self):
        self.assertEqual(v.test_file_mimetype,
                         u.check_mimetype(v.test_file))

    def test_check_mimetype_buffer(self):
        fileobj = open(v.test_file, 'rb')
        self.assertEqual(v.test_file_mimetype,
                         u.check_mimetype_buffer(fileobj))
        fileobj.close()

    def test_retrieve_info_from_buffer(self):
        fileobj = open(v.test_file, 'rb')
        file_content = fileobj.read()
        fileobj.seek(0)
        self.assertEqual((v.test_file_mimetype,
                          v.test_file_size,
                          file_content),
                         u.retrieve_info_from_buffer(fileobj))
        fileobj.close()
