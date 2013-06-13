# -*- coding: utf-8 -*-
import json
import os.path

username = "username"
password = "password"
partial_uri_list_2 = ["https://example.org", "auth"]
partial_uri_list_3 = ["https://example.org", "auth", "v1.0"]
auth_url = "https://example.org/auth"
auth_ver_url = "https://example.org/auth/v1.0"
token = 'AUTH_tk55ed712a114a467ca10e3841bb98accf'
storage_url = ('https://example.org/v1/'
               'AUTH_c1d6a4bc-892d-4106-9c62-36a48ea0f129')
containers = [{'bytes': 0, 'count': 0, 'name': 'test'},
              {'bytes': 0, 'count': 0, 'name': 'test2'}]
containers_json = json.JSONEncoder().encode(containers)
cntr_name = "test_container"
object_name = "test_object"
objects = [{'bytes': 5246,
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
objects_json = json.JSONEncoder().encode(objects)
object_name = 'sample.txt'
dest_obj_name = 'sample_1.txt'
test_file = os.path.abspath('src/swiftsc_tests/sample.txt')
test_file_mimetype = 'text/plain'
object_zero_name = 'empty.txt'
dest_obj_zero_name = 'empty_1.txt'
test_zero_file = os.path.abspath('src/swiftsc_tests/empty.txt')
test_zero_file_mimetype = 'inode/x-empty'
ks = 'c6f41799c8e44974bf6b2f3af9495dc0'
kid = '162fc4dff590424d86119eed4311680f'
dom = 'http://example.org'
keystone = {
    'access': {
        'metadata': {
            'is_admin': 0,
            'roles': [
                '20810c41473b439fb9abb2d3e320dd24']},
        'serviceCatalog': [
            {'endpoints': [{'adminURL': '%s:8774/v1.1/%s' % (dom, ks),
                            'id': '%s/v1.1/%s' % (kid, ks),
                            'internalURL': '%s:8774/v1.1/%s' % (dom, ks),
                            'publicURL': '%s:8774/v1.1/%s' % (dom, ks),
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
            {'endpoints': [{'adminURL': '%s:8776/v1/%s' % (dom, ks),
                            'id': '39e6248531344e2d923b3ea53538241a',
                            'internalURL': '%s:8776/v1/%s' % (dom, ks),
                            'publicURL': '%s:8776/v1/%s' % (dom, ks),
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'volume',
             'type': 'volume'},
            {'endpoints': [{'adminURL': '%s:8773/services/Admin' % dom,
                            'id': '3b4359581bc34117bffd7debb0c647bc',
                            'internalURL': '%s:8773/services/Cloud' % dom,
                            'publicURL': '%s:8773/services/Cloud' % dom,
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'ec2',
             'type': 'ec2'},
            {'endpoints': [{'adminURL': '%s:8080/v1' % dom,
                            'id': '43d72312224d4d27a4c261a6f16ecd1c',
                            'internalURL': '%s:8080/v1/AUTH_%s' % (dom, ks),
                            'publicURL': '%s:8080/v1/AUTH_%s' % (dom, ks),
                            'region': 'RegionOne'}],
             'endpoints_links': [],
             'name': 'swift',
             'type': 'object-store'},
            {'endpoints': [{'adminURL': '%s:35357/v2.0' % dom,
                            'id': '6f8ddae43fd54ec09faad0b3fb1646dc',
                            'internalURL': '%s:5000/v2.0' % dom,
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
                             'id': ks,
                             'name': 'guest'}},
        'user': {'id': 'd68c758154dc47399e3c371beb295148',
                 'name': 'guest',
                 'roles': [{'name': 'Member'}],
                 'roles_links': [],
                 'username': 'guest'}}}
token_keystone = '4bbf2976ab9d4703b85207054dbdb701'
storage_url_ks = ('http://example.org:8080/v1/'
                  'AUTH_c6f41799c8e44974bf6b2f3af9495dc0')
