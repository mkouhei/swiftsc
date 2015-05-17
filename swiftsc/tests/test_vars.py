# -*- coding: utf-8 -*-
""" Sample data for unit test """
import os.path

USERNAME = "username"
PASSWORD = "password"
PARTIAL_URI_LIST_2 = ["https://example.org", "auth"]
PARTIAL_URI_LIST_3 = ["https://example.org", "auth", "v1.0"]
AUTH_URL = "https://example.org/auth"
AUTH_VER_URL = "https://example.org/auth/v1.0"
KEYSTONE_URL = 'https://keystone.example.org/v2.0/tokens'
TOKEN = 'AUTH_tk55ed712a114a467ca10e3841bb98accf'
STORAGE_URL = ('https://example.org/v1/'
               'AUTH_c1d6a4bc-892d-4106-9c62-36a48ea0f129')
CONTAINERS = [{'bytes': 0, 'count': 0, 'name': 'test'},
              {'bytes': 0, 'count': 0, 'name': 'test2'}]
CNTR_NAME = "test_container"
OBJECTS = [{'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T08:40:00.459930',
            'name': 'sample.txt'},
           {'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T09:23:40.060560',
            'name': 'sample_2.txt'},
           {'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T09:23:26.092580',
            'name': 'sample_3.txt'}]
OBJECT_NAME = 'sample.txt'
DEST_OBJ_NAME = 'sample_1.txt'
TEST_FILE = os.path.abspath('swiftsc/tests/sample.txt')
TEST_FILE_MIMETYPE = 'text/plain'
TEST_FILE_SIZE = os.path.getsize(TEST_FILE)
OBJECT_ZERO_NAME = 'empty.txt'
ZERO_FILE = os.path.abspath('swiftsc/tests/empty.txt')
KS = 'c6f41799c8e44974bf6b2f3af9495dc0'
KID = '162fc4dff590424d86119eed4311680f'
DOM = 'http://example.org'
KEYSTONE = {
    'access': {
        'metadata': {
            'is_admin': 0,
            'roles': [
                '20810c41473b439fb9abb2d3e320dd24']},
        'serviceCatalog': [
            {'endpoints': [{'adminURL': '%s:8774/v1.1/%s' % (DOM, KS),
                            'id': '%s/v1.1/%s' % (KID, KS),
                            'internalURL': '%s:8774/v1.1/%s' % (DOM, KS),
                            'publicURL': '%s:8774/v1.1/%s' % (DOM, KS),
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'nova',
             'type': 'compute'},
            {'endpoints': [{'adminURL': 'http://example.org:9292',
                            'id': '26bc2d8a056548339dc2f2bd59486ced',
                            'internalURL': 'http://example.org:9292',
                            'publicURL': 'http://example.org:9292',
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'glance',
             'type': 'image'},
            {'endpoints': [{'adminURL': '%s:8776/v1/%s' % (DOM, KS),
                            'id': '39e6248531344e2d923b3ea53538241a',
                            'internalURL': '%s:8776/v1/%s' % (DOM, KS),
                            'publicURL': '%s:8776/v1/%s' % (DOM, KS),
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'volume',
             'type': 'volume'},
            {'endpoints': [{'adminURL': '%s:8773/services/Admin' % DOM,
                            'id': '3b4359581bc34117bffd7debb0c647bc',
                            'internalURL': '%s:8773/services/Cloud' % DOM,
                            'publicURL': '%s:8773/services/Cloud' % DOM,
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'ec2',
             'type': 'ec2'},
            {'endpoints': [{'adminURL': '%s:8080/v1' % DOM,
                            'id': '43d72312224d4d27a4c261a6f16ecd1c',
                            'internalURL': '%s:8080/v1/AUTH_%s' % (DOM, KS),
                            'publicURL': '%s:8080/v1/AUTH_%s' % (DOM, KS),
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'swift',
             'type': 'object-store'},
            {'endpoints': [{'adminURL': '%s:35357/v2.0' % DOM,
                            'id': '6f8ddae43fd54ec09faad0b3fb1646dc',
                            'internalURL': '%s:5000/v2.0' % DOM,
                            'publicURL': 'https://example.org/v2.0',
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'keystone',
             'type': 'identity'}],
        'token': {'expires': '2013-06-04T08:05:44Z',
                  'id': '4bbf2976ab9d4703b85207054dbdb701',
                  'issued_at': '2013-06-03T08:05:44.201287',
                  'tenant': {'description': None,
                             'enabled': True,
                             'id': KS,
                             'name': 'guest'}},
        'user': {'id': 'd68c758154dc47399e3c371beb295148',
                 'name': 'guest',
                 'roles': [{'name': 'Member'}],
                 'roles_links': [],
                 'username': 'guest'}}}
TOKEN_KEYSTONE = '4bbf2976ab9d4703b85207054dbdb701'
STORAGE_URL_KS = ('http://example.org:8080/v1/'
                  'AUTH_c6f41799c8e44974bf6b2f3af9495dc0')
TENANT_NAME = 'guest'
KEYSTONE_TOKEN = '4bbf2976ab9d4703b85207054dbdb701'
