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
import mock
from mock import patch
import requests
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import swiftsc.client as c
import swiftsc_tests.test_vars as v


class ClientTests(unittest.TestCase):

    @patch('requests.get')
    def test_retrieve_token(self, mock_):
        res = requests.Response()
        res.headers = {'X-Auth-Token': v.token,
                       'X-Storage-Url': v.storage_url}
        mock_.return_value = res
        self.assertTupleEqual((v.token, v.storage_url),
                              c.retrieve_token(v.auth_ver_url,
                                               v.username, v.password))

    @patch('requests.get')
    def test_list_containers(self, mock_):
        res = requests.Response()
        res._content = v.containers_json.encode('utf-8')
        res.status_code = 200
        mock_.return_value = res
        self.assertListEqual(v.containers,
                             c.list_containers(v.token, v.storage_url))

    @patch('requests.put')
    def test_create_container(self, mock_):
        res = requests.Response()
        res.status_code = 201
        mock_.return_value = res
        self.assertEqual(201,
                         c.create_container(v.token, v.storage_url,
                                            v.cntr_name))

    @patch('requests.head')
    def test_is_container(self, mock_):
        res = requests.Response()
        res.status_code = 200
        mock_.return_value = res
        self.assertEqual(True,
                         c.is_container(v.token, v.storage_url,
                                        v.cntr_name))

    @patch('requests.delete')
    def test_delete_container(self, mock_):
        res = requests.Response()
        res.status_code = 204
        mock_.return_value = res
        self.assertEqual(204,
                         c.delete_container(v.token, v.storage_url,
                                            v.cntr_name))

    @patch('requests.put')
    def test_create_object(self, mock_):
        res = requests.Response()
        res.status_code = 201
        mock_.return_value = res
        test_file = v.test_file
        self.assertEqual(201,
                         c.create_object(v.token, v.storage_url, v.cntr_name,
                                         test_file, v.object_name))

    @patch('requests.get')
    def test_list_objects(self, mock_):
        res = requests.Response()
        res._content = v.objects_json.encode('utf-8')
        res.status_code = 200
        mock_.return_value = res
        self.assertEqual(v.objects,
                         c.list_objects(v.token, v.storage_url, v.cntr_name))

    @patch('requests.head')
    def test_is_object(self, mock_):
        res = requests.Response()
        res.status_code = 200
        mock_.return_value = res
        self.assertEqual(True,
                         c.is_container(v.token, v.storage_url,
                                        v.cntr_name))

    @patch('requests.get')
    def test_retrieve_object(self, mock_):
        res = requests.Response()
        with open(v.test_file, 'rb') as f:
            res._content = f.read()
            f.seek(0)
            file_content = f.read()
        res.status_code = 200
        mock_.return_value = res
        self.assertEqual((True, file_content),
                         c.retrieve_object(v.token, v.storage_url, v.cntr_name,
                                           v.object_name))

    @patch('requests.get')
    def test_retrieve_object_zero(self, mock_):
        res = requests.Response()
        with open(v.test_zero_file, 'rb') as f:
            res._content = f.read()
            f.seek(0)
            file_content = f.read()
        res.status_code = 200
        mock_.return_value = res
        self.assertEqual((True, file_content),
                         c.retrieve_object(v.token, v.storage_url, v.cntr_name,
                                           v.object_zero_name))

    @patch('requests.put')
    def test_copy_object(self, mock_):
        res = requests.Response()
        res.status_code = 201
        mock_.return_value = res
        self.assertEqual(201,
                         c.copy_object(v.token, v.storage_url, v.cntr_name,
                                       v.object_name, v.dest_obj_name))

    @patch('requests.delete')
    def test_delete_object(self, mock_):
        res = requests.Response()
        res.status_code = 204
        mock_.return_value = res
        self.assertEqual(204,
                         c.delete_object(v.token, v.storage_url, v.cntr_name,
                                         v.object_name))

    def test_retrieve_public_url_swift(self):
        self.assertEqual(v.storage_url_ks,
                         c.retrieve_public_url_swift(v.keystone))

    def test_retrieve_token_keystone(self):
        self.assertEqual(v.token_keystone,
                         c.retrieve_token_keystone(v.keystone))
