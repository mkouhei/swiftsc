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
import inspect
import json
import utils

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
        r = requests.post(auth_url, headers=headers, data=json.dumps(payload),
                          timeout=TIMEOUT, verify=verify)
    else:
        # using tempauth of Swift
        headers = {'X-Storage-User': username, 'X-Storage-Pass': password}
        r = requests.get(auth_url, headers=headers,
                         timeout=TIMEOUT, verify=verify)
    return r.headers.get('X-Auth-Token'), r.headers.get('X-Storage-Url')


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


def list_containers(token, storage_url, verify=True):
    """

    Arguments:

        token      : authentication token
        storage_url: URL of swift storage
        verify     : True is check a host’s SSL certificate
    """
    headers = {'X-Auth-Token': token}
    payload = {'format': 'json'}
    r = requests.get(storage_url, headers=headers,
                     params=payload, timeout=TIMEOUT, verify=verify)
    # not use r.content that is data type is "str".
    # You must encode to unicode and utf-8 by yourself
    # if you use multibyte character.
    r.encoding = 'utf-8'
    if isinstance(r.json, list):
        return r.json
    elif inspect.ismethod(r.json):
        # support requests 1.0 over
        return r.json()


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
    r = requests.put(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return r.status_code


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
    r = requests.head(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return r.ok


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
    r = requests.delete(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return r.status_code


def create_object(token, storage_url, container_name,
                  local_filepath, object_name=None, verify=True):
    """
    Arguments:

        token         : authentication token
        storage_url   : URL of swift storage
        container_name: container name
        local_filepath: absolute path of upload file
        object_name   : object name (optional)
        verify        : True is check a host’s SSL certificate

    Return: 201 (Created)
    """
    if object_name is None:
        object_name = os.path.basename(local_filepath)
    mimetype = utils.check_mimetype(local_filepath)
    content_length = os.path.getsize(local_filepath)
    # Failed to upload without "Content-Length" when uploading empty file
    headers = {'X-Auth-Token': token,
               'Content-Length': str(content_length),
               'content-type': mimetype}

    with open(local_filepath, 'rb') as f:
        data = f.read()
    url = utils.generate_url([storage_url, container_name, object_name])
    r = requests.put(url, headers=headers, data=data,
                     timeout=TIMEOUT, verify=verify)
    return r.status_code


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
    r = requests.get(url, headers=headers, params=payload,
                     timeout=TIMEOUT, verify=verify)
    r.encoding = 'utf-8'
    if isinstance(r.json, list):
        return r.json
    elif inspect.ismethod(r.json):
        # support requests 1.0 over
        return r.json()


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
    r = requests.head(url,  headers=headers, timeout=TIMEOUT, verify=verify)
    return r.ok


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
    r = requests.get(url,  headers=headers, timeout=TIMEOUT, verify=verify)
    return r.ok, r.content


def copy_object(token, storage_url, container_name,
                src_object_name, dest_object_name, verify=True):
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
    src_url = '/' + utils.generate_url([container_name, src_object_name])
    headers = {'X-Auth-Token': token,
               'Content-Length': "0",
               'X-Copy-From': src_url}

    dest_url = utils.generate_url([storage_url, container_name,
                                   dest_object_name])
    r = requests.put(dest_url, headers=headers, timeout=TIMEOUT, verify=verify)
    return r.status_code


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
    r = requests.delete(url, headers=headers, timeout=TIMEOUT, verify=verify)
    return r.status_code
