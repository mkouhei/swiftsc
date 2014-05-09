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
import unittest
from httpretty import HTTPretty, httprettified
from swiftsc import client as c
from swiftsc.tests import test_vars as v


class ClientTests(unittest.TestCase):

    @httprettified
    def test_retrieve_token(self):
        headers = {'X-Auth-Token': v.token,
                   'X-Storage-Url': v.storage_url}

        HTTPretty.register_uri(HTTPretty.GET,
                               v.auth_ver_url,
                               adding_headers=headers)
        self.assertTupleEqual((v.token, v.storage_url),
                              c.retrieve_token(v.auth_ver_url,
                                               v.username, v.password))

    @httprettified
    def test_list_containers(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               v.storage_url,
                               body=v.containers_json.encode('utf-8'),
                               status=200)
        self.assertListEqual(v.containers,
                             c.list_containers(v.token, v.storage_url))

    @httprettified
    def test_create_container(self):
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s' % (v.storage_url, v.cntr_name),
                               status=201)
        self.assertEqual(201,
                         c.create_container(v.token, v.storage_url,
                                            v.cntr_name))

    @httprettified
    def test_is_container(self):
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.storage_url, v.cntr_name),
                               status=200)
        self.assertEqual(True,
                         c.is_container(v.token, v.storage_url,
                                        v.cntr_name))

    @httprettified
    def test_delete_container(self):
        HTTPretty.register_uri(HTTPretty.DELETE,
                               '%s/%s' % (v.storage_url, v.cntr_name),
                               status=204)
        self.assertEqual(204,
                         c.delete_container(v.token, v.storage_url,
                                            v.cntr_name))

    @httprettified
    def test_create_object(self):
        test_file = v.test_file
        object_name = os.path.basename(test_file)
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.storage_url,
                                             v.cntr_name,
                                             object_name),
                               status=201)
        self.assertEqual(201,
                         c.create_object(v.token, v.storage_url, v.cntr_name,
                                         v.test_file, v.object_name))

    @httprettified
    def test_create_object_with_file_object(self):
        test_file = open(v.test_file, 'rb', buffering=0)
        object_name = os.path.basename(v.test_file)
        files = {'file': (object_name,
                          test_file,
                          v.test_file_mimetype)}
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.storage_url,
                                             v.cntr_name,
                                             object_name),
                               files=files,
                               status=201)
        self.assertEqual(201,
                         c.create_object(v.token, v.storage_url, v.cntr_name,
                                         test_file, v.object_name))
        test_file.close()

    @httprettified
    def test_list_objects(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/' % (v.storage_url,
                                           v.cntr_name),
                               body=v.objects_json.encode('utf-8'))
        self.assertEqual(v.objects,
                         c.list_objects(v.token, v.storage_url, v.cntr_name))

    @httprettified
    def test_is_object(self):
        test_file = v.test_file
        object_name = os.path.basename(test_file)
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.storage_url,
                                             v.cntr_name,
                                             object_name))
        self.assertEqual(True,
                         c.is_object(v.token, v.storage_url,
                                     v.cntr_name, object_name))

    @httprettified
    def test_retrieve_object(self):
        object_name = os.path.basename(v.test_file)
        with open(v.test_file, 'rb') as f:
            file_content = f.read()
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/%s' % (v.storage_url,
                                             v.cntr_name,
                                             object_name),
                               body=file_content)
        self.assertEqual((True, file_content),
                         c.retrieve_object(v.token, v.storage_url, v.cntr_name,
                                           v.object_name))

    @httprettified
    def test_retrieve_object_zero(self):
        object_name = os.path.basename(v.test_zero_file)
        with open(v.test_zero_file, 'rb') as f:
            file_content = f.read()
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/%s' % (v.storage_url,
                                             v.cntr_name,
                                             object_name),
                               body=file_content)
        self.assertEqual((True, file_content),
                         c.retrieve_object(v.token, v.storage_url, v.cntr_name,
                                           v.object_zero_name))

    @httprettified
    def test_copy_object(self):
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.storage_url,
                                             v.cntr_name,
                                             v.dest_obj_name),
                               status=201)
        self.assertEqual(201,
                         c.copy_object(v.token, v.storage_url, v.cntr_name,
                                       v.object_name, v.dest_obj_name))

    @httprettified
    def test_delete_object(self):
        HTTPretty.register_uri(HTTPretty.DELETE,
                               '%s/%s/%s' % (v.storage_url,
                                             v.cntr_name,
                                             v.object_name),
                               status=204)
        self.assertEqual(204,
                         c.delete_object(v.token, v.storage_url, v.cntr_name,
                                         v.object_name))

    def test_retrieve_public_url_swift(self):
        self.assertEqual(v.storage_url_ks,
                         c.retrieve_public_url_swift(v.keystone))

    def test_retrieve_token_keystone(self):
        self.assertEqual(v.token_keystone,
                         c.retrieve_token_keystone(v.keystone))
