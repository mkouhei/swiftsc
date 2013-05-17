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
