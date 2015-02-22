# -*- coding: utf-8 -*-
""" swiftsc.client """
import requests
import os.path
import json
from swiftsc import utils


#: connection timeout
#: see also http://goo.gl/6KIJnc
TIMEOUT = 5.000


def retrieve_token(auth_url, username, password,
                   tenant_name=None, timeout=TIMEOUT, verify=True):
    """Retrieve token

    :rtype: tuple
    :return: Auth token, storage url

    :param str auth_url: Swift API of authentication

        https://<Host>/auth/<api_version>
        ex. https://swift.example.org/auth/v1.0
        using KeyStone as follows
        https://<KeyStone>/<api_version>/tokens
        ex. https://keystone.example.org/v2.0/tokens

    :param str username: Swift User name
    :param str password: Swift User password
    :param str tenant_name: tenant name of OpenStack
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
    """
    if tenant_name:
        # using OpenStack KeyStone
        payload = set_auth_info(username, password, tenant_name)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(auth_url,
                            headers=headers,
                            data=json.dumps(payload),
                            timeout=timeout,
                            verify=verify)
        res_d = res.json()
        token = retrieve_token_keystone(res_d)
        storage_url = retrieve_public_url_swift(res_d)
    else:
        # using tempauth of Swift
        headers = {'X-Storage-User': username, 'X-Storage-Pass': password}
        res = requests.get(auth_url, headers=headers,
                           timeout=timeout, verify=verify)
        token = res.headers.get('X-Auth-Token')
        storage_url = res.headers.get('X-Storage-Url')
    return token, storage_url


def set_auth_info(username, password, tenant_name):
    """Generate auth parameters for KeyStone auth

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


def retrieve_public_url_swift(r_json):
    """Retrieve Swift public url from KeyStone

    :rtype: string
    :return: swift public url

    :param dict r_json: response payload from KeyStone auth
    """
    endpoints = [ep.get('endpoints')[0]
                 for ep in r_json.get('access').get('serviceCatalog')
                 if ep.get('name') == 'swift'][0]
    return endpoints.get('publicURL')


def retrieve_token_keystone(r_json):
    """Retrieve token of KeyStone Auth

    :rtype: str
    :return: Auth token

    :param dict r_json: response payload from KeyStone auth
    """
    return r_json.get('access').get('token').get('id')


def list_containers(token, storage_url, timeout=TIMEOUT, verify=True):
    """List containers

    :rtype: list
    :return: containers list

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param float timeout: connection timeout
    :param verify bool: True is check a host’s SSL certificate
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
    """Create container

    :rtype: int
    :return: status code; 201(Created)

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    res = requests.put(url, headers=headers, timeout=timeout, verify=verify)
    return res.status_code


def is_container(token, storage_url, container_name,
                 timeout=TIMEOUT, verify=True):
    """Check container

    :rtype: bool
    :return: True is contianer

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    res = requests.head(url, headers=headers, timeout=timeout, verify=verify)
    return res.ok


def delete_container(token, storage_url, container_name,
                     timeout=TIMEOUT, verify=True):
    """Delete container

    :rtype: int
    :return: status code; 204(No Content)

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    res = requests.delete(url, headers=headers, timeout=timeout, verify=verify)
    return res.status_code


def create_object(*args, **kwargs):
    """Create object

    :rtype: int
    :return: status code; 201 (Created)

    :param dict \*\*kwargs: token, storage_url, container_name,

        local_file, object_name, timeout, verify
    """
    local_file = args[3]
    if kwargs.get('object_name'):
        object_name = kwargs.get('object_name')
    else:
        object_name = None

    if object_name is None:
        object_name = os.path.basename(local_file)

    url = utils.generate_url([args[1], args[2], object_name])

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
    """List objects

    :rtype: list
    :return: object list

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    payload = {'format': 'json'}
    url = utils.generate_url([storage_url, container_name]) + '/'
    res = requests.get(url, headers=headers, params=payload,
                       timeout=timeout, verify=verify)
    res.encoding = 'utf-8'
    return res.json()


def is_object(token, storage_url, container_name, object_name,
              timeout=TIMEOUT, verify=True):
    """Check object

    :rtype: bool
    :return: True is object

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name, object_name])
    res = requests.head(url, headers=headers, timeout=timeout, verify=verify)
    return res.ok


def retrieve_object(token, storage_url, container_name,
                    object_name, timeout=TIMEOUT, verify=True):
    """Retrieve object

    :rtype: tuple
    :return: `Response`.ok, `Response`.content

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param str object_name: object name
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name, object_name])
    res = requests.get(url, headers=headers, timeout=timeout, verify=verify)
    return res.ok, res.content


def copy_object(*args, **kwargs):
    """Copy object

    :rtype: int
    :return: status code; 201(Created)

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param str src_object_name: object name of source
    :param str dest_object_name: object name of destination
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
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
    src_url = '/' + utils.generate_url([container_name, src_object_name])
    headers = {'X-Auth-Token': token,
               'Content-Length': "0",
               'X-Copy-From': src_url}

    dest_url = utils.generate_url([storage_url, container_name,
                                   dest_object_name])
    res = requests.put(dest_url, headers=headers,
                       timeout=timeout, verify=verify)
    return res.status_code


def delete_object(token, storage_url, container_name,
                  object_name, timeout=TIMEOUT, verify=True):
    """Delete object

    :rtype: int
    :return: status code; 204(No Content)

    :param str token: authentication token
    :param str storage_url: URL of swift storage
    :param str container_name: container name
    :param str object_name: object name
    :param float timeout: connection timeout
    :param bool verify: True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name, object_name])
    res = requests.delete(url, headers=headers, timeout=timeout, verify=verify)
    return res.status_code
