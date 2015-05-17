# -*- coding: utf-8 -*-
"""swiftsc.client module."""
import requests
import os.path
import json
import copy

from swiftsc import utils
from swiftsc.exception import ValidationError

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
    obj.headers = {"X-Auth-Token": res.headers.get("X-Auth-Token")}
    obj.uri = res.headers.get("X-Storage-URL")


def _keystone_auth(obj):
    """keystone auth."""
    payload = {
        "auth": {
            "passwordCredentials": {
                "username": obj.username,
                "password": obj.password},
            "tenantName": obj.tenant_name}}
    headers = {"Content-Type": "application/json"}
    res = requests.post(obj.auth_uri,
                        headers=headers,
                        data=json.dumps(payload),
                        verify=obj.verify,
                        timeout=obj.timeout)
    obj.headers = {"X-Auth-Token": res.json()['access']['token']['id']}
    obj.uri = _retrieve_public_url_swift(res.json())


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


def _retrieve_public_url_swift(r_json):
    """Retrieve Swift public url from KeyStone.

    :rtype: string
    :return: swift public url

    :param dict r_json: response payload from KeyStone auth
    """
    endpoints = [ep.get('endpoints')[0]
                 for ep in r_json.get('access').get('serviceCatalog')
                 if ep.get('name') == 'swift'][0]
    return endpoints.get('publicURL')


def retrieve_token(auth_uri, username, password,
                   tenant_name=None, timeout=TIMEOUT, verify=True):
    """Retrieve token.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: tuple
    :return: Auth token, storage url

    :param str auth_uri: Swift API of authentication

        https://<Host>/auth/<api_version>
        ex. https://swift.example.org/auth/v1.0
        using KeyStone as follows
        https://<KeyStone>/<api_version>/tokens
        ex. https://keystone.example.org/v2.0/tokens

    :param str username: Swift User name
    :param str password: Swift User password
    :param str tenant_name: tenant name of OpenStack
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    if tenant_name:
        # using OpenStack KeyStone
        payload = _set_auth_info(username, password, tenant_name)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(auth_uri,
                            headers=headers,
                            data=json.dumps(payload),
                            timeout=timeout,
                            verify=verify)
        res_d = res.json()
        token = _retrieve_token_keystone(res_d)
        storage_url = _retrieve_public_url_swift(res_d)
    else:
        # using tempauth of Swift
        headers = {'X-Storage-User': username, 'X-Storage-Pass': password}
        res = requests.get(auth_uri, headers=headers,
                           timeout=timeout, verify=verify)
        token = res.headers.get('X-Auth-Token')
        storage_url = res.headers.get('X-Storage-Url')
    return token, storage_url


def _set_auth_info(username, password, tenant_name):
    """Generate auth parameters for KeyStone auth.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: dict
    :return: auth parameters for KeyStone auth

    :param str username: keystone username
    :param str password: keystone password
    :param str tenant_name: keystone tenant name
    """
    payload = {
        "auth": {
            "passwordCredentials": {
                "username": username,
                "password": password},
            "tenantName": tenant_name}}
    return payload


def _generate_url(partial_uri_list):
    """Generate url.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: str
    :return: auth url (ex. "https://swift.example.org/auth/v1.0")

    :param list partial_uri_list: patial string of generating URL
    """
    url = ""
    for i, partial_uri in enumerate(partial_uri_list):
        if i + 1 == len(partial_uri_list):
            url += partial_uri
        else:
            url += partial_uri + "/"
    return url


def _retrieve_token_keystone(r_json):
    """Retrieve token of KeyStone Auth.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: str
    :return: Auth token

    :param dict r_json: response payload from KeyStone auth
    """
    return r_json.get('access').get('token').get('id')


def list_containers(token, storage_url, timeout=TIMEOUT, verify=True):
    """List containers.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: list
    :return: containers list

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param float timeout: connection timeout
    :param verify bool: True is check a host's SSL certificate
    """
    headers = {'X-Auth-Token': token}
    payload = {'format': 'json'}
    res = requests.get(storage_url, headers=headers,
                       params=payload, timeout=timeout, verify=verify)
    # not use res.content that is data type is "str".
    # You must encode to unicode and utf-8 by yourself
    # if you use multibyte character.
    res.encoding = 'utf-8'
    return res.json()


def create_container(token, storage_url, container_name,
                     timeout=TIMEOUT, verify=True):
    """Create container.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: int
    :return: status code; 201(Created)

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = _generate_url([storage_url, container_name])
    res = requests.put(url, headers=headers, timeout=timeout, verify=verify)
    return res.status_code


def is_container(token, storage_url, container_name,
                 timeout=TIMEOUT, verify=True):
    """Check container.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: bool
    :return: True is contianer

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = _generate_url([storage_url, container_name])
    res = requests.head(url, headers=headers, timeout=timeout, verify=verify)
    return res.ok


def delete_container(token, storage_url, container_name,
                     timeout=TIMEOUT, verify=True):
    """Delete container.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: int
    :return: status code; 204(No Content)

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = _generate_url([storage_url, container_name])
    res = requests.delete(url, headers=headers, timeout=timeout, verify=verify)
    return res.status_code


def create_object(*args, **kwargs):
    """Create object.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: int
    :return: status code; 201 (Created)

    :param dict **kwargs: token, storage_url, container_name,

        local_file, object_name, timeout, verify
    """
    local_file = args[3]
    object_name = kwargs.get('object_name')
    if object_name is None:
        object_name = os.path.basename(local_file)

    url = _generate_url([args[1], args[2], object_name])

    if kwargs.get('verify'):
        verify = kwargs.get('verify')
    else:
        verify = True

    if kwargs.get('timeout'):
        timeout = kwargs.get('timeout')
    else:
        timeout = TIMEOUT

    is_file = utils.from_file(local_file)
    if is_file:
        # open file
        content_length = os.path.getsize(local_file)
        mimetype = utils.check_mimetype(local_file)
    else:
        # via stdin pipe
        (mimetype,
         content_length,
         data) = utils.retrieve_info_from_buffer(local_file)

    # Failed to upload without "Content-Length" when uploading empty file
    headers = {'X-Auth-Token': args[0],
               'Content-Length': str(content_length),
               'content-type': mimetype}

    if is_file:
        # open file
        with open(local_file, 'rb') as _file:
            res = requests.put(url, headers=headers, data=_file,
                               timeout=timeout, verify=verify)
    else:
        # stdin pipe
        res = requests.put(url, headers=headers, data=data,
                           timeout=timeout, verify=verify)
    return res.status_code


def list_objects(token, storage_url, container_name,
                 timeout=TIMEOUT, verify=True):
    """List objects.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: list
    :return: object list

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    headers = {'X-Auth-Token': token}
    payload = {'format': 'json'}
    url = _generate_url([storage_url, container_name]) + '/'
    res = requests.get(url, headers=headers, params=payload,
                       timeout=timeout, verify=verify)
    res.encoding = 'utf-8'
    return res.json()


def is_object(token, storage_url, container_name, object_name,
              timeout=TIMEOUT, verify=True):
    """Check object.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: bool
    :return: True is object

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = _generate_url([storage_url, container_name, object_name])
    res = requests.head(url, headers=headers, timeout=timeout, verify=verify)
    return res.ok


def retrieve_object(token, storage_url, container_name,
                    object_name, timeout=TIMEOUT, verify=True):
    """Retrieve object.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: tuple
    :return: `Response`.ok, `Response`.content

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param str object_name: object name
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = _generate_url([storage_url, container_name, object_name])
    res = requests.get(url, headers=headers, timeout=timeout, verify=verify)
    return res.ok, res.content


def copy_object(*args, **kwargs):
    """Copy object.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: int
    :return: status code; 201(Created)

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param str src_object_name: object name of source
    :param str dest_object_name: object name of destination
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    token = args[0]
    storage_url = args[1]
    container_name = args[2]
    src_object_name = args[3]
    dest_object_name = args[4]
    if kwargs.get('verify'):
        verify = kwargs.get('verify')
    else:
        verify = True

    if kwargs.get('timeout'):
        timeout = kwargs.get('timeout')
    else:
        timeout = TIMEOUT
    src_url = '/' + _generate_url([container_name, src_object_name])
    headers = {'X-Auth-Token': token,
               'Content-Length': "0",
               'X-Copy-From': src_url}

    dest_url = _generate_url([storage_url, container_name,
                              dest_object_name])
    res = requests.put(dest_url, headers=headers,
                       timeout=timeout, verify=verify)
    return res.status_code


def delete_object(token, storage_url, container_name,
                  object_name, timeout=TIMEOUT, verify=True):
    """Delete object.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: int
    :return: status code; 204(No Content)

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param str object_name: object name
    :param float timeout: connection timeout
    :param bool verify: True is check a host's SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = _generate_url([storage_url, container_name, object_name])
    res = requests.delete(url, headers=headers, timeout=timeout, verify=verify)
    return res.status_code
