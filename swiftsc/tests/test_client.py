# -*- coding: utf-8 -*-
"""swiftsc.client unit tests."""
import os.path
import unittest
import requests_mock
from swiftsc.client import Client
from swiftsc.exception import AuthenticationError
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
    def test_get_token_keystone(self, _mock):
        """Unit test of retrieve_token"""
        _mock.post(v.KEYSTONE_URL,
                   json=v.KEYSTONE)
        cli = Client(auth_uri=v.KEYSTONE_URL,
                     username=v.USERNAME,
                     password=v.PASSWORD,
                     tenant_name=v.TENANT_NAME)
        self.assertEqual(cli.uri, v.STORAGE_URL_KS)
        self.assertEqual(cli.headers['X-Auth-Token'], v.KEYSTONE_TOKEN)

    @requests_mock.Mocker()
    def test_get_token_keystone_v3(self, _mock):
        """Unit test of retrieve_token"""
        _mock.post(v.KEYSTONE_V3_URL,
                   headers={'x-subject-token': v.KEYSTONE_TOKEN},
                   json=v.KEYSTONE_V3)
        cli = Client(auth_uri=v.KEYSTONE_V3_URL,
                     username=v.USERNAME,
                     password=v.PASSWORD,
                     tenant_name=v.TENANT_NAME)
        self.assertEqual(cli.uri, v.STORAGE_URL_KS)
        self.assertEqual(cli.headers['X-Auth-Token'], v.KEYSTONE_TOKEN)

    @requests_mock.Mocker()
    def test_get_token_keystone_fail(self, _mock):
        """Unit test of retrieve_token"""
        _mock.post(v.KEYSTONE_V3_URL,
                   headers={'x-subject-token': v.KEYSTONE_TOKEN},
                   status_code=401,
                   json={'error': {
                       'message': ('The request you have made requires '
                                   'authentication.'),
                       'code': 401,
                       'title': 'Unauthorized'}})
        with self.assertRaises(AuthenticationError):
            Client(auth_uri=v.KEYSTONE_V3_URL,
                   username=v.USERNAME,
                   password=v.PASSWORD,
                   tenant_name=v.TENANT_NAME)

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
