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
import requests
import os.path
import json
import sys
if sys.version_info > (3, 0):
    import _io
from swiftsc import utils


TIMEOUT = 5.000


def retrieve_token(auth_url, username, password,
                   tenant_name=None, verify=True):
    """

    Arguments:

        url        : Swift API of authentication
                     https://<Host>/auth/<api_version>
                     ex. https://swift.example.org/auth/v1.0

                     using KeyStone as follows
                     https://<KeyStone>/<api_version>/tokens
                     ex. https://keystone.example.org/v2.0/tokens
        username   : Swift User name
        password   : Swift User password
        tenant_name: tenant name of OpenStack
        verify     : True is check a host’s SSL certificate
    """
    if tenant_name:
        # using OpenStack KeyStone
        payload = set_auth_info(username, password, tenant_name)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(auth_url,
                            headers=headers,
                            data=json.dumps(payload),
                            timeout=TIMEOUT,
                            verify=verify)
        res_d = utils.return_json(res.json)
        token = retrieve_token_keystone(res_d)
        storage_url = retrieve_public_url_swift(res_d)
    else:
        # using tempauth of Swift
        headers = {'X-Storage-User': username, 'X-Storage-Pass': password}
        res = requests.get(auth_url, headers=headers,
                           timeout=TIMEOUT, verify=verify)
        token = res.headers.get('X-Auth-Token')
        storage_url = res.headers.get('X-Storage-Url')
    return token, storage_url


def set_auth_info(username, password, tenant_name):
    """

    Arguments:

        username   : keystone username
        password   : keystone password
        tenant_name: keystone tenant name
    """
    payload = {
        "auth": {
            "passwordCredentials": {
                "username": username,
                "password": password},
            "tenantName": tenant_name}}
    return payload


def retrieve_public_url_swift(r_json):
    """
    Argument: response json
    Return: id
    """
    endpoints = [ep.get('endpoints')[0]
                 for ep in r_json.get('access').get('serviceCatalog')
                 if ep.get('name') == 'swift'][0]
    return endpoints.get('publicURL')


def retrieve_token_keystone(r_json):
    """
    Argument: response json
    Return: id
    """
    return r_json.get('access').get('token').get('id')


def list_containers(token, storage_url, verify=True):
    """

    Arguments:

        token      : authentication token
        storage_url: URL of swift storage
        verify     : True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    payload = {'format': 'json'}
    res = requests.get(storage_url, headers=headers,
                       params=payload, timeout=TIMEOUT, verify=verify)
    # not use res.content that is data type is "str".
    # You must encode to unicode and utf-8 by yourself
    # if you use multibyte character.
    res.encoding = 'utf-8'
    return utils.return_json(res.json)


def create_container(token, storage_url, container_name, verify=True):
    """

    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        verify        : True is check a host’s SSL certificate

    Return: 201 (Created)
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    res = requests.put(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return res.status_code


def is_container(token, storage_url, container_name, verify=True):
    """

    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        verify        : True is check a host’s SSL certificate

    Return: boolean
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    res = requests.head(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return res.ok


def delete_container(token, storage_url, container_name, verify=True):
    """
    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        verify        : True is check a host’s SSL certificate

    Return: 204 (No Content)
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    res = requests.delete(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return res.status_code


def create_object(*args, **kwargs):
    """
    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        local_file    : absolute path of upload file
                        or
                        file object (from stdin pipe)
        object_name   : object name (optional)
                        default is local_file basename or
        verify        : True is check a host’s SSL certificate

    Return: 201 (Created)
    """
    token = args[0]
    storage_url = args[1]
    container_name = args[2]
    local_file = args[3]
    if kwargs.get('object_name'):
        object_name = kwargs.get('object_name')
    else:
        object_name = None
    if kwargs.get('verify'):
        verify = kwargs.get('verify')
    else:
        verify = True

    if ((sys.version_info < (3, 0) and
         isinstance(local_file, file)) or
        (sys.version_info > (3, 0) and
         isinstance(local_file, _io.FileIO))):
        # from stdin pipe
        (mimetype,
         content_length,
         data) = utils.retrieve_info_from_buffer(local_file)
    else:
        with open(local_file, 'rb') as _file:
            data = _file.read()
        content_length = os.path.getsize(local_file)
        mimetype = utils.check_mimetype(local_file)

    if object_name is None:
        object_name = os.path.basename(local_file)

    # Failed to upload without "Content-Length" when uploading empty file
    headers = {'X-Auth-Token': token,
               'Content-Length': str(content_length),
               'content-type': mimetype}

    url = utils.generate_url([storage_url, container_name, object_name])
    res = requests.put(url, headers=headers, data=data,
                       timeout=TIMEOUT, verify=verify)
    return res.status_code


def list_objects(token, storage_url, container_name, verify=True):
    """
    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        verify        : True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    payload = {'format': 'json'}
    url = utils.generate_url([storage_url, container_name]) + '/'
    res = requests.get(url, headers=headers, params=payload,
                       timeout=TIMEOUT, verify=verify)
    res.encoding = 'utf-8'
    return utils.return_json(res.json)


def is_object(token, storage_url, container_name, object_name, verify=True):
    """
    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        object_name   : object name
        verify        : True is check a host’s SSL certificate

    Return: boolean
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name, object_name])
    res = requests.head(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return res.ok


def retrieve_object(token, storage_url, container_name,
                    object_name, verify=True):
    """
    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        object_name   : object name
        verify        : True is check a host’s SSL certificate

    Return: object data
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name, object_name])
    res = requests.get(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return res.ok, res.content


def copy_object(*args, **kwargs):
    """
    Arguments:

        token           : authentication token
        storage_url     : URL of swift storage
        container_name  : container name
        src_object_name : object name of source
        dest_object_name: object name of destination
        verify          : True is check a host’s SSL certificate

    Return: 201 (Created)
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
    src_url = '/' + utils.generate_url([container_name, src_object_name])
    headers = {'X-Auth-Token': token,
               'Content-Length': "0",
               'X-Copy-From': src_url}

    dest_url = utils.generate_url([storage_url, container_name,
                                   dest_object_name])
    res = requests.put(dest_url, headers=headers,
                       timeout=TIMEOUT, verify=verify)
    return res.status_code


def delete_object(token, storage_url, container_name,
                  object_name, verify=True):
    """
    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        object_name   : object name
        verify        : True is check a host’s SSL certificate

    Return: 204 (No Content)
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name, object_name])
    res = requests.delete(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return res.status_code
