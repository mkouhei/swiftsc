# -*- coding: utf-8 -*-
"""swiftsc.client module."""
import os.path
import json
import copy
import requests

from swiftsc import utils
from swiftsc.exception import ValidationError, AuthenticationError

#: connection timeout
#: see also http://goo.gl/6KIJnc
TIMEOUT = 5.000

# See: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings()


def _temp_auth(obj):
    """tmpauth."""
    auth_headers = {"X-Storage-User": obj.username,
                    "X-Storage-Pass": obj.password}
    res = requests.get(obj.auth_uri,
                       headers=auth_headers,
                       verify=obj.verify,
                       timeout=obj.timeout)
    if res.status_code != 200:
        raise AuthenticationError('Authentication failed')
    obj.headers = {"X-Auth-Token": res.headers.get("X-Auth-Token")}
    obj.uri = res.headers.get("X-Storage-URL")


def _keystone_auth_payload(obj):
    """Keystone auth request payload."""
    if "/v2.0/tokens" in obj.auth_uri:
        payload = {
            "auth": {
                "passwordCredentials": {
                    "username": obj.username,
                    "password": obj.password},
                "tenantName": obj.tenant_name}}
    elif "/v3/auth/tokens" in obj.auth_uri:
        payload = {
            "auth": {
                "scope": {
                    "project": {
                        "id": obj.tenant_name}},
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "id": obj.username,
                            "password": obj.password}}}}}
    return payload


def _set_auth_token(res):
    """Retrieve Auth token."""
    if res.json().get('access'):
        # Identity API v2.0
        token = res.json()['access']['token']['id']
    elif res.headers.get('x-subject-token'):
        # Identity API v3
        token = res.headers.get('x-subject-token')
    return {"X-Auth-Token": token}


def _keystone_auth(obj):
    """keystone auth."""
    payload = _keystone_auth_payload(obj)
    headers = {"Content-Type": "application/json"}
    res = requests.post(obj.auth_uri,
                        headers=headers,
                        data=json.dumps(payload),
                        verify=obj.verify,
                        timeout=obj.timeout)
    if res.status_code != 200:
        raise AuthenticationError('Authentication failed')
    obj.headers = _set_auth_token(res)
    obj.uri = _retrieve_public_url_swift(res.json())


def _retrieve_public_url_swift(r_json):
    """Retrieve Swift public url from KeyStone.

    :rtype: string
    :return: swift public url

    :param dict r_json: response payload from KeyStone auth
    """
    if r_json.get('access'):
        # Identity API v2.0
        url = [ep.get('endpoints')[0]
               for ep in r_json.get('access').get('serviceCatalog')
               if ep.get('type') == 'object-store'][0].get('publicURL')
    else:
        # Identity API v3
        url = [ep.get('endpoints')[0]
               for ep in r_json.get('token').get('catalog')
               if ep.get('type') == 'object-store'][0].get('url')
    return url


class Client(object):
    """The :class:`Client <Client>` object.

    This provides REST connection including tempauth or KeyStone Auth.::

        >>> from swiftsc import Client
        >>> client = Client(auth_uri='https://swift.example.org/auth/v1.0',
        ... username='swiftuser', password='passw0rd')

    :param str auth_uri: tempauth URL or KeyStone URL
    :param str uri: Storage URL (required token)
    :param str username: tempauth or KeyStone username
    :param str password: tempauth or KeyStone password
    :param str token: Auth token
    :param str tenant_name: KeyStone tenant name
    """

    #: The path of the API endpoint.
    path = None

    def __init__(self,
                 auth_uri=None,
                 uri=None,
                 username=None,
                 password=None,
                 token=None,
                 tenant_name=None,
                 verify=True,
                 timeout=TIMEOUT):
        """constructor of Client."""
        #: SSL Cert Verification. (default: ``True``)
        self.verify = verify
        #: Request timeout. (default: ``5.0``)
        self.timeout = timeout

        if uri:
            #: Swift Storage URL
            self.uri = uri
        if token:
            self.headers = {'X-Auth-Token': token}
        elif auth_uri and username and password:
            #: TempAuth or KeyStone API URL
            self.auth_uri = auth_uri
            #: username
            self.username = username
            #: password
            self.password = password
            #: KeyStone tenant name
            if tenant_name:
                # for KeyStone

                self.tenant_name = tenant_name
                _keystone_auth(self)
            else:
                # for tempauth
                _temp_auth(self)

        self.containers = Container(self)


class _CRUD(object):
    """The :class:`_CRUD <_CRUD>` object."""

    def __init__(self):
        self.uri = None
        self.headers = None
        self.verify = True
        self.timeout = TIMEOUT
        """ Constructor of _CRUD """

    def _set_path(self, path):
        """Change endpoint.

        :param str path: the path of the endpoint URL.
        """
        self.uri = "%(uri)s/%(path)s" % {"uri": self.uri, "path": path}

    def no_verify(self):
        """Ignore SSL Cert Verification.

        Change ``verify`` to ``False``.
        """
        self.verify = False

    def change_timeout(self, timeout):
        """Change timeout.

        Change timeout to other than "5.0"
        """
        if timeout:
            self.timeout = timeout

    def list(self):
        """List collection of resources.

        :rtype: `requests.Response`
        :return: Response of list collection.
        """
        return requests.get(self.uri,
                            headers=self.headers,
                            params={"format": "json"},
                            verify=self.verify,
                            timeout=self.timeout)

    def detail(self, obj_id=None):
        """Show/Get a single resource.

        :rtype: `requests.Response`
        :return: Response of detail single resource.

        :param str obj_id: resource id (or resource name)
        """
        if obj_id is None:
            raise KeyError
        return requests.get("%(uri)s/%(id)s" % {"uri": self.uri,
                                                "id": obj_id},
                            headers=self.headers,
                            verify=self.verify,
                            timeout=self.timeout)

    def show_metadata(self, obj_id=None):
        """Show metadata.

        :rtype: `requests.Response`
        :return: Response of metadata single resource.

        :param str obj_id: resource id (or resource name)
        """
        if obj_id is None:
            raise KeyError
        return requests.head("%(uri)s/%(id)s" % {"uri": self.uri,
                                                 "id": obj_id},
                             headers=self.headers,
                             verify=self.verify,
                             timeout=self.timeout)

    def create(self, **kwargs):
        """Create or replace resource.

        :rtype: `requests.Response`
        :return: Response of metadata single resource.

        :param **kwargs: parameters
        """
        self._validate(**kwargs)
        return requests.put('%(uri)s/%(id)s' % {'uri': self.uri,
                                                'id': kwargs.get('name')},
                            data=kwargs.get('data'),
                            headers=self.headers,
                            verify=self.verify,
                            timeout=self.timeout)

    @staticmethod
    def _validate(**kwargs):
        """Validate parameters.

        :rtype: dict
        :return: dict of keyword arguments

        :param **kwargs: parameters
        """
        return kwargs

    def update_metadata(self, obj_id, **kwargs):
        """Create, Update (or delete) metadata.

        :rtype: `requests.Response`
        :return: Response of updating a single resource.

        :param str obj_id: resource id (or resource name)
        :param **kwargs: keyword arguments of method
        """
        return requests.post("%(uri)s/%(id)s" % {"uri": self.uri,
                                                 "id": obj_id},
                             headers=self.headers,
                             data=json.dumps(kwargs),
                             verify=self.verify,
                             timeout=self.timeout)

    def delete(self, obj_id):
        """Delete resource.

        :rtype: `requests.Response`
        :return: Response of deleting a single resource.

        :param str obj_id: resource id (or resource name)
        """
        if obj_id is None:
            raise KeyError
        return requests.delete("%(uri)s/%(id)s" % {"uri": self.uri,
                                                   "id": obj_id},
                               headers=self.headers,
                               verify=self.verify,
                               timeout=self.timeout)


class Container(_CRUD):
    """
    Swift container resources.

    ::

        >>> client.containers.list().json()
        [{'bytes': 1403088360, 'count': 5, 'name': 'container-a'},
         {'bytes': 393429510, 'count': 11, 'name': 'container-b'},
         {'bytes': 410389320, 'count': 11, 'name': 'container-c'},
         ...
         {'bytes': 9690876040, 'count': 57, 'name': 'container-x'}]

    """

    def __init__(self, obj):
        """constructor of Container."""
        self.uri = obj.uri
        self.headers = obj.headers
        self.verify = obj.verify
        self.timeout = obj.timeout

        self.container_name = None
        self.objects = None

    def container(self, container_name):
        r"""Set container name and create instances.

        The instance has the attributes
        of :class:`Container <Container>`, as follows.

        * objects: :class:`Object <Object>`

        :param str container_name: container name
        """
        self.container_name = container_name
        self.objects = Object(self)

    def _validate(self, **kwargs):
        if kwargs.get('name') is None:
            raise ValidationError('name is None')


class Object(_CRUD):
    """Objects resources.

    ::

        >>> client.containers.container('container-a')
        >>> client.containers.objects.list().json()
        [{'bytes': 0,
          'content_type': 'application/octet-stream',
          'hash': 'd41d8cd98f00b204e9800998ecf8427e',
          'last_modified': '2015-03-05T07:57:17.450440',
          'name': 'test'},
         {'bytes': 225280,
          'content_type': 'application/x-tar',
          'hash': '9aa58f7a3fca9853c26a048eda407c71',
          'last_modified': '2013-07-18T09:56:30.989920',
          'name': 'test.tgz'},
         {'bytes': 22,
          'content_type': 'text/plain',
          'hash': '4cc6982f37c06ec4eb378e916cfbd289',
          'last_modified': '2015-03-05T09:34:42.935400',
          'name': 'test2'}]

    """

    def __init__(self, obj):
        """Constructor of Object."""
        if obj.container_name is None:
            raise KeyError('Container name is None')
        self.uri = obj.uri
        self.headers = obj.headers
        self.verify = obj.verify
        self.timeout = obj.timeout

        self.container_name = obj.container_name
        self._set_path(self.container_name)
        self.object_name = None

    def object(self, object_name):
        """Set object name.

        :param str object_name: object name
        """
        self.object_name = object_name

    def create(self, **kwargs):
        """Create object.

        :param **kwargs: parameters for creating object

        :rtype: `requests.Response`
        :return: Response of create object
        """
        self._validate(**kwargs)

        name = kwargs.get('name')
        if hasattr(kwargs.get('file_path'), 'fileno'):
            # stdin pipe
            mtype, length, data = utils.retrieve_info_from_buffer(
                kwargs.get('file_path'))
            self._set_content_length(length=length)
            self._set_content_type(mtype)

        elif kwargs.get('file_path'):
            # local file
            self._set_content_length(file_path=kwargs.get('file_path'))
            self._set_content_type(file_path=kwargs.get('file_path'))
            if name is None:
                name = os.path.basename(kwargs.get('file_path'))
            with open(kwargs.get('file_path'), 'rb') as fobj:
                data = fobj.read()

        return requests.put('%(uri)s/%(name)s' % dict(uri=self.uri, name=name),
                            headers=self.headers,
                            data=data,
                            verify=self.verify,
                            timeout=self.timeout)

    def _set_content_length(self, length=None, file_path=None):
        """Set 'Content-Length' to HTTP headers.

        :param int lengthh: content length
        :param str file_path: local file path
        """
        if length:
            self.headers['Content-Length'] = length
        elif file_path:
            self.headers['Content-Length'] = os.path.getsize(file_path)

    def _set_content_type(self, mimetype=None, file_path=None):
        """Set 'Content-Type' to HTTP headers.

        :param str file_path: local file path
        """
        if mimetype:
            self.headers['Content-Type'] = mimetype
        elif file_path:
            self.headers['Content-Type'] = utils.check_mimetype(file_path)

    def copy(self, src_object_name, dest_object_name):
        """Copy object.

        :rtype: `requests.Response`
        :return: Response of copy object
        """
        headers = copy.deepcopy(self.headers)
        headers['Content-Length'] = '0'
        headers['X-Copy-From'] = (
            '/%(cont)s/%(obj)s' % {'cont': self.container_name,
                                   'obj': src_object_name})

        uri = (
            '%(uri)s/%(obj)s' % {'uri': self.uri,
                                 'obj': dest_object_name})

        return requests.put(uri,
                            headers=headers,
                            verify=self.verify,
                            timeout=self.timeout)
