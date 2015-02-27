# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013, 2014 Kouhei Maeda <mkouhei@palmtb.net>

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
import os.path
import json
import unittest
from httpretty import HTTPretty, httprettified
from swiftsc import client
from swiftsc.tests import test_vars as v


class ClientTests(unittest.TestCase):
    """Unit test of client module"""

    @httprettified
    def test_retrieve_token(self):
        """Unit test of retrieve_token"""
        headers = {'X-Auth-Token': v.TOKEN,
                   'X-Storage-Url': v.STORAGE_URL}

        HTTPretty.register_uri(HTTPretty.GET,
                               v.AUTH_VER_URL,
                               adding_headers=headers)
        self.assertTupleEqual((v.TOKEN, v.STORAGE_URL),
                              client.retrieve_token(v.AUTH_VER_URL,
                                                    v.USERNAME,
                                                    v.PASSWORD))

    @httprettified
    def test_retrieve_token_keystone(self):
        """Unit test of retrieve_token"""
        HTTPretty.register_uri(HTTPretty.POST,
                               v.KEYSTONE_URL,
                               body=json.dumps(v.KEYSTONE))
        self.assertTupleEqual((v.KEYSTONE_TOKEN, v.STORAGE_URL_KS),
                              client.retrieve_token(v.KEYSTONE_URL,
                                                    v.USERNAME,
                                                    v.PASSWORD,
                                                    tenant_name=v.TENANT_NAME))

    @httprettified
    def test_list_containers(self):
        """Unit test of list_containers"""
        HTTPretty.register_uri(HTTPretty.GET,
                               v.STORAGE_URL,
                               body=v.CONTAINERS_JSON.encode('utf-8'),
                               status=200)
        self.assertListEqual(v.CONTAINERS,
                             client.list_containers(v.TOKEN,
                                                    v.STORAGE_URL))

    @httprettified
    def test_create_container(self):
        """Unit test of create_containers"""
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                               status=201)
        self.assertEqual(201,
                         client.create_container(v.TOKEN,
                                                 v.STORAGE_URL,
                                                 v.CNTR_NAME))

    @httprettified
    def test_is_container(self):
        """Unit test of is_container"""
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                               status=200)
        self.assertEqual(True,
                         client.is_container(v.TOKEN, v.STORAGE_URL,
                                             v.CNTR_NAME))

    @httprettified
    def test_delete_container(self):
        """Unit test of delete_container"""
        HTTPretty.register_uri(HTTPretty.DELETE,
                               '%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                               status=204)
        self.assertEqual(204,
                         client.delete_container(v.TOKEN, v.STORAGE_URL,
                                                 v.CNTR_NAME))

    @httprettified
    def test_create_object(self):
        """Unit test of create_object"""
        object_name = os.path.basename(v.TEST_FILE)
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CNTR_NAME,
                                             object_name),
                               status=201)
        self.assertEqual(201,
                         client.create_object(v.TOKEN,
                                              v.STORAGE_URL,
                                              v.CNTR_NAME,
                                              v.TEST_FILE,
                                              object_name=v.OBJECT_NAME))

    @httprettified
    def test_create_object_with_file(self):
        """Unit test of create_object with file"""
        test_file = open(v.TEST_FILE, 'rb', buffering=0)
        object_name = os.path.basename(v.TEST_FILE)
        files = {'file': (object_name,
                          test_file,
                          v.TEST_FILE_MIMETYPE)}
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CNTR_NAME,
                                             object_name),
                               files=files,
                               status=201)
        self.assertEqual(201,
                         client.create_object(v.TOKEN,
                                              v.STORAGE_URL,
                                              v.CNTR_NAME,
                                              test_file,
                                              object_name=v.OBJECT_NAME))
        test_file.close()

    @httprettified
    def test_list_objects(self):
        """ Unit test of list_objects """
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/' % (v.STORAGE_URL,
                                           v.CNTR_NAME),
                               body=v.OBJECTS_JSON.encode('utf-8'))
        self.assertEqual(v.OBJECTS,
                         client.list_objects(v.TOKEN,
                                             v.STORAGE_URL,
                                             v.CNTR_NAME))

    @httprettified
    def test_is_object(self):
        """ Unit test of is_object """
        object_name = os.path.basename(v.TEST_FILE)
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CNTR_NAME,
                                             object_name))
        self.assertEqual(True,
                         client.is_object(v.TOKEN, v.STORAGE_URL,
                                          v.CNTR_NAME, object_name))

    @httprettified
    def test_retrieve_object(self):
        """ Unit test of retrieve_object """
        object_name = os.path.basename(v.TEST_FILE)
        with open(v.TEST_FILE, 'rb') as _file:
            file_content = _file.read()
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CNTR_NAME,
                                             object_name),
                               body=file_content)
        self.assertEqual((True, file_content),
                         client.retrieve_object(v.TOKEN,
                                                v.STORAGE_URL,
                                                v.CNTR_NAME,
                                                v.OBJECT_NAME))

    @httprettified
    def test_retrieve_object_zero(self):
        """ Unit test of retrieve_object with file size zero """
        object_name = os.path.basename(v.ZERO_FILE)
        with open(v.ZERO_FILE, 'rb') as _file:
            file_content = _file.read()
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CNTR_NAME,
                                             object_name),
                               body=file_content)
        self.assertEqual((True, file_content),
                         client.retrieve_object(v.TOKEN,
                                                v.STORAGE_URL,
                                                v.CNTR_NAME,
                                                v.OBJECT_ZERO_NAME))

    @httprettified
    def test_copy_object(self):
        """ Unit test of copy_object """
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CNTR_NAME,
                                             v.DEST_OBJ_NAME),
                               status=201)
        self.assertEqual(201,
                         client.copy_object(v.TOKEN,
                                            v.STORAGE_URL,
                                            v.CNTR_NAME,
                                            v.OBJECT_NAME,
                                            v.DEST_OBJ_NAME))

    @httprettified
    def test_delete_object(self):
        """ Unit test of delete_object """
        HTTPretty.register_uri(HTTPretty.DELETE,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CNTR_NAME,
                                             v.OBJECT_NAME),
                               status=204)
        self.assertEqual(204,
                         client.delete_object(v.TOKEN,
                                              v.STORAGE_URL,
                                              v.CNTR_NAME,
                                              v.OBJECT_NAME))
