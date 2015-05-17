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
import os.path
import unittest
import requests_mock
from swiftsc import client
from swiftsc.client import Client
from swiftsc.tests import test_vars as v


class ClientTests(unittest.TestCase):

    """Unit test of client.Client"""

    def setUp(self):
        """Initialize"""

        with requests_mock.Mocker() as _mock:
            headers = {'X-Auth-Token': v.TOKEN,
                       'X-Storage-Url': v.STORAGE_URL}
            _mock.get(v.AUTH_URL,
                      headers=headers)
            self.tclient = Client(auth_uri=v.AUTH_URL,
                                  username=v.USERNAME,
                                  password=v.PASSWORD)

    @requests_mock.Mocker()
    def test_list_containers(self, _mock):
        """unit test of list containers"""
        _mock.get(v.STORAGE_URL,
                  json=v.CONTAINERS,
                  status_code=200)
        self.assertEqual(200,
                         self.tclient.containers.list().status_code)
        self.assertListEqual(v.CONTAINERS,
                             self.tclient.containers.list().json())

    @requests_mock.Mocker()
    def test_create_container(self, _mock):
        """unit test of create container"""
        _mock.put('%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                  status_code=201)
        res = self.tclient.containers.create(name=v.CNTR_NAME)
        self.assertEqual(201, res.status_code)

    @requests_mock.Mocker()
    def test_show_metadata_container(self, _mock):
        """unit test of show metadata of container"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                   status_code=200)
        self.assertEqual(200,
                         self.tclient.containers.show_metadata(
                             v.CNTR_NAME).status_code)

    @requests_mock.Mocker()
    def test_delete_container(self, _mock):
        """unit test of delete container"""
        _mock.delete('%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                     status_code=204)
        self.assertEqual(204,
                         self.tclient.containers.delete(
                             v.CNTR_NAME).status_code)

    @requests_mock.Mocker()
    def test_create_object(self, _mock):
        """unit test of create object"""
        object_name = os.path.basename(v.TEST_FILE)
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                  status_code=201)
        self.tclient.containers.container(v.CNTR_NAME)
        res = self.tclient.containers.objects.create(name=object_name,
                                                     file_path=v.TEST_FILE)
        self.assertEqual(201, res.status_code)

    @requests_mock.Mocker()
    def test_create_object_from_stdin(self, _mock):
        """unit test of crete object from stdin"""
        object_name = os.path.basename(v.TEST_FILE)
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                  status_code=201)
        self.tclient.containers.container(v.CNTR_NAME)
        data = open(v.TEST_FILE, 'rb', buffering=0)
        res = self.tclient.containers.objects.create(name=object_name,
                                                     file_path=data)
        self.assertEqual(201, res.status_code)
        data.close()

    @requests_mock.Mocker()
    def test_list_objects(self, _mock):
        """Unit test of list_objects"""
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        self.tclient.containers.container(v.CNTR_NAME)
        self.assertEqual(200,
                         self.tclient.containers.objects.list().status_code)

    @requests_mock.Mocker()
    def test_show_metadata_object(self, _mock):
        """Unit test show metadata of object"""
        object_name = os.path.basename(v.TEST_FILE)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                   status_code=200)
        self.tclient.containers.container(v.CNTR_NAME)
        self.assertEqual(200,
                         self.tclient.containers.objects.show_metadata(
                             object_name).status_code)

    @requests_mock.Mocker()
    def test_detail_object(self, _mock):
        """unit test detail object"""
        object_name = os.path.basename(v.TEST_FILE)
        with open(v.TEST_FILE, 'rb') as fobj:
            body = fobj.read()
        _mock.get('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                  content=body)
        self.tclient.containers.container(v.CNTR_NAME)
        res = self.tclient.containers.objects.detail(object_name)
        self.assertEqual(200, res.status_code)
        self.assertEqual(body, res.content)

    @requests_mock.Mocker()
    def test_copy_object(self, _mock):
        """unit test copy object"""
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, v.DEST_OBJ_NAME),
                  status_code=201)
        self.tclient.containers.container(v.CNTR_NAME)
        res = self.tclient.containers.objects.copy(v.OBJECT_NAME,
                                                   v.DEST_OBJ_NAME)
        self.assertEqual(201, res.status_code)

    @requests_mock.Mocker()
    def test_delete_object(self, _mock):
        """unit test delete object"""
        _mock.delete('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, v.OBJECT_NAME),
                     status_code=204)
        self.tclient.containers.container(v.CNTR_NAME)
        res = self.tclient.containers.objects.delete(v.OBJECT_NAME)
        self.assertEqual(204, res.status_code)


class OldClientTests(unittest.TestCase):

    """Unit test of client module"""

    @requests_mock.Mocker()
    def test_retrieve_token(self, _mock):
        """Unit test of retrieve_token"""
        headers = {'X-Auth-Token': v.TOKEN,
                   'X-Storage-Url': v.STORAGE_URL}

        _mock.get(v.AUTH_VER_URL,
                  headers=headers)
        self.assertTupleEqual((v.TOKEN, v.STORAGE_URL),
                              client.retrieve_token(v.AUTH_VER_URL,
                                                    v.USERNAME,
                                                    v.PASSWORD))

    @requests_mock.Mocker()
    def test_retrieve_token_keystone(self, _mock):
        """Unit test of retrieve_token"""
        _mock.post(v.KEYSTONE_URL,
                   json=v.KEYSTONE)
        self.assertTupleEqual((v.KEYSTONE_TOKEN, v.STORAGE_URL_KS),
                              client.retrieve_token(v.KEYSTONE_URL,
                                                    v.USERNAME,
                                                    v.PASSWORD,
                                                    tenant_name=v.TENANT_NAME))

    @requests_mock.Mocker()
    def test_list_containers(self, _mock):
        """Unit test of list_containers"""
        _mock.get(v.STORAGE_URL,
                  json=v.CONTAINERS,
                  status_code=200)
        self.assertListEqual(v.CONTAINERS,
                             client.list_containers(v.TOKEN,
                                                    v.STORAGE_URL))

    @requests_mock.Mocker()
    def test_create_container(self, _mock):
        """Unit test of create_containers"""
        _mock.put('%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                  status_code=201)
        self.assertEqual(201,
                         client.create_container(v.TOKEN,
                                                 v.STORAGE_URL,
                                                 v.CNTR_NAME))

    @requests_mock.Mocker()
    def test_is_container(self, _mock):
        """Unit test of is_container"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                   status_code=200)
        self.assertEqual(True,
                         client.is_container(v.TOKEN, v.STORAGE_URL,
                                             v.CNTR_NAME))

    @requests_mock.Mocker()
    def test_delete_container(self, _mock):
        """Unit test of delete_container"""
        _mock.delete('%s/%s' % (v.STORAGE_URL, v.CNTR_NAME),
                     status_code=204)
        self.assertEqual(204,
                         client.delete_container(v.TOKEN, v.STORAGE_URL,
                                                 v.CNTR_NAME))

    @requests_mock.Mocker()
    def test_create_object(self, _mock):
        """Unit test of create_object"""
        object_name = os.path.basename(v.TEST_FILE)
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                  status_code=201)
        self.assertEqual(201,
                         client.create_object(v.TOKEN,
                                              v.STORAGE_URL,
                                              v.CNTR_NAME,
                                              v.TEST_FILE,
                                              object_name=v.OBJECT_NAME))

    @requests_mock.Mocker()
    def test_create_object_with_file(self, _mock):
        """Unit test of create_object with file"""
        test_file = open(v.TEST_FILE, 'rb', buffering=0)
        object_name = os.path.basename(v.TEST_FILE)
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                  status_code=201)
        self.assertEqual(201,
                         client.create_object(v.TOKEN,
                                              v.STORAGE_URL,
                                              v.CNTR_NAME,
                                              test_file,
                                              object_name=v.OBJECT_NAME))
        test_file.close()

    @requests_mock.Mocker()
    def test_list_objects(self, _mock):
        """Unit test of list_objects"""
        _mock.get('%s/%s/' % (v.STORAGE_URL, v.CNTR_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        self.assertEqual(v.OBJECTS,
                         client.list_objects(v.TOKEN,
                                             v.STORAGE_URL,
                                             v.CNTR_NAME))

    @requests_mock.Mocker()
    def test_is_object(self, _mock):
        """Unit test of is_object"""
        object_name = os.path.basename(v.TEST_FILE)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                   status_code=200)
        self.assertEqual(True,
                         client.is_object(v.TOKEN, v.STORAGE_URL,
                                          v.CNTR_NAME, object_name))

    @requests_mock.Mocker()
    def test_retrieve_object(self, _mock):
        """Unit test of retrieve_object"""
        object_name = os.path.basename(v.TEST_FILE)
        with open(v.TEST_FILE, 'rb') as _file:
            file_content = _file.read()
        _mock.get('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                  content=file_content,
                  status_code=200)
        self.assertEqual((True, file_content),
                         client.retrieve_object(v.TOKEN,
                                                v.STORAGE_URL,
                                                v.CNTR_NAME,
                                                v.OBJECT_NAME))

    @requests_mock.Mocker()
    def test_retrieve_object_zero(self, _mock):
        """Unit test of retrieve_object with file size zero"""
        object_name = os.path.basename(v.ZERO_FILE)
        with open(v.ZERO_FILE, 'rb') as _file:
            file_content = _file.read()
        _mock.get('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, object_name),
                  content=file_content,
                  status_code=200)
        self.assertEqual((True, file_content),
                         client.retrieve_object(v.TOKEN,
                                                v.STORAGE_URL,
                                                v.CNTR_NAME,
                                                v.OBJECT_ZERO_NAME))

    @requests_mock.Mocker()
    def test_copy_object(self, _mock):
        """Unit test of copy_object"""
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, v.DEST_OBJ_NAME),
                  status_code=201)
        self.assertEqual(201,
                         client.copy_object(v.TOKEN,
                                            v.STORAGE_URL,
                                            v.CNTR_NAME,
                                            v.OBJECT_NAME,
                                            v.DEST_OBJ_NAME))

    @requests_mock.Mocker()
    def test_delete_object(self, _mock):
        """Unit test of delete_object"""
        _mock.delete('%s/%s/%s' % (v.STORAGE_URL, v.CNTR_NAME, v.OBJECT_NAME),
                     status_code=204)
        self.assertEqual(204,
                         client.delete_object(v.TOKEN,
                                              v.STORAGE_URL,
                                              v.CNTR_NAME,
                                              v.OBJECT_NAME))
