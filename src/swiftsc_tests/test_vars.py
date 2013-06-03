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
containers = [{u'bytes': 0, u'count': 0, u'name': u'test'},
              {u'bytes': 0, u'count': 0, u'name': u'test2'}]
containers_json = json.JSONEncoder().encode(containers)
cntr_name = "test_container"
object_name = "test_object"
objects = [{u'bytes': 5246,
            u'content_type': u'text/plain',
            u'hash': u'd226a3f396cbe3c187f2b7b78030eebb',
            u'last_modified': u'2013-05-01T08:40:00.459930',
            u'name': u'sample.txt'},
           {u'bytes': 5246,
            u'content_type': u'text/plain',
            u'hash': u'd226a3f396cbe3c187f2b7b78030eebb',
            u'last_modified': u'2013-05-01T09:23:40.060560',
            u'name': u'sample_2.txt'},
           {u'bytes': 5246,
            u'content_type': u'text/plain',
            u'hash': u'd226a3f396cbe3c187f2b7b78030eebb',
            u'last_modified': u'2013-05-01T09:23:26.092580',
            u'name': u'sample_3.txt'}]
objects_json = json.JSONEncoder().encode(objects)
object_name = 'sample.txt'
dest_obj_name = 'sample_1.txt'
test_file = os.path.abspath('src/swiftsc_tests/sample.txt')
test_file_mimetype = 'text/plain'
object_zero_name = 'empty.txt'
dest_obj_zero_name = 'empty_1.txt'
test_zero_file = os.path.abspath('src/swiftsc_tests/empty.txt')
test_zero_file_mimetype = 'inode/x-empty'
ks = u'c6f41799c8e44974bf6b2f3af9495dc0'
kid = u'162fc4dff590424d86119eed4311680f'
dom = u'http://example.org'
keystone = {
    u'access': {
        u'metadata': {
            u'is_admin': 0,
            u'roles': [
                u'20810c41473b439fb9abb2d3e320dd24']},
        u'serviceCatalog': [
            {u'endpoints': [{u'adminURL': u'%s:8774/v1.1/%s' % (dom, ks),
                             u'id': u'%s/v1.1/%s' % (kid, ks),
                             u'internalURL': u'%s:8774/v1.1/%s' % (dom, ks),
                             u'publicURL': u'%s:8774/v1.1/%s' % (dom, ks),
                             u'region': u'RegionOne'}],
             u'endpoints_links': [],
             u'name': u'nova',
             u'type': u'compute'},
            {u'endpoints': [{u'adminURL': u'http://example.org:9292',
                             u'id': u'26bc2d8a056548339dc2f2bd59486ced',
                             u'internalURL': u'http://example.org:9292',
                             u'publicURL': u'http://example.org:9292',
                             u'region': u'RegionOne'}],
             u'endpoints_links': [],
             u'name': u'glance',
             u'type': u'image'},
            {u'endpoints': [{u'adminURL': u'%s:8776/v1/%s' % (dom, ks),
                             u'id': u'39e6248531344e2d923b3ea53538241a',
                             u'internalURL': u'%s:8776/v1/%s' % (dom, ks),
                             u'publicURL': u'%s:8776/v1/%s' % (dom, ks),
                             u'region': u'RegionOne'}],
             u'endpoints_links': [],
             u'name': u'volume',
             u'type': u'volume'},
            {u'endpoints': [{u'adminURL': u'%s:8773/services/Admin' % dom,
                             u'id': u'3b4359581bc34117bffd7debb0c647bc',
                             u'internalURL': u'%s:8773/services/Cloud' % dom,
                             u'publicURL': u'%s:8773/services/Cloud' % dom,
                             u'region': u'RegionOne'}],
             u'endpoints_links': [],
             u'name': u'ec2',
             u'type': u'ec2'},
            {u'endpoints': [{u'adminURL': u'%s:8080/v1' % dom,
                             u'id': u'43d72312224d4d27a4c261a6f16ecd1c',
                             u'internalURL': u'%s:8080/v1/AUTH_%s' % (dom, ks),
                             u'publicURL': u'%s:8080/v1/AUTH_%s' % (dom, ks),
                             u'region': u'RegionOne'}],
             u'endpoints_links': [],
             u'name': u'swift',
             u'type': u'object-store'},
            {u'endpoints': [{u'adminURL': u'%s:35357/v2.0' % dom,
                             u'id': u'6f8ddae43fd54ec09faad0b3fb1646dc',
                             u'internalURL': u'%s:5000/v2.0' % dom,
                             u'publicURL': u'https://example.org/v2.0',
                             u'region': u'RegionOne'}],
             u'endpoints_links': [],
             u'name': u'keystone',
             u'type': u'identity'}],
        u'token': {u'expires': u'2013-06-04T08:05:44Z',
                   u'id': u'4bbf2976ab9d4703b85207054dbdb701',
                   u'issued_at': u'2013-06-03T08:05:44.201287',
                   u'tenant': {u'description': None,
                               u'enabled': True,
                               u'id': ks,
                               u'name': u'guest'}},
        u'user': {u'id': u'd68c758154dc47399e3c371beb295148',
                  u'name': u'guest',
                  u'roles': [{u'name': u'Member'}],
                  u'roles_links': [],
                  u'username': u'guest'}}}
token_keystone = '4bbf2976ab9d4703b85207054dbdb701'
storage_url_ks = ('http://example.org:8080/v1/'
                  'AUTH_c6f41799c8e44974bf6b2f3af9495dc0')
