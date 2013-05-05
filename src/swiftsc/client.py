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
import utils


def retrieve_token(auth_url, username, password):
    """

    Arguments:

        url: Swift API of authentication
             https://<Host>/auth/<api_version>
             ex. https://swift.example.org/auth/v1.0
        username: Swift User name
        password: Swift User password
    """
    headers = {'X-Storage-User': username, 'X-Storage-Pass': password}
    r = requests.get(auth_url, headers=headers)
    return r.headers.get('X-Auth-Token'), r.headers.get('X-Storage-Url')


def list_containers(token, storage_url):
    """

    Arguments:

        token: authentication token
        storage_url: URL of swift storage
    """
    headers = {'X-Auth-Token': token}
    payload = {'format': 'json'}
    r = requests.get(storage_url, headers=headers, params=payload)
    # not use r.content that is data type is "str".
    # You must encode to unicode and utf-8 by yourself
    # if you use multibyte character.
    r.encoding = 'utf-8'
    return r.json


def create_container(token, storage_url, container_name):
    """

    Arguments:

        token: authentication token
        storage_url: URL of swift storage
        container_name: container name

    Return: 201 (Created)
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    r = requests.put(url, headers=headers)
    return r.status_code


def is_container(token, storage_url, container_name):
    """

    Arguments:

        token: authentication token
        storage_url: URL of swift storage
        container_name: container name

    Return: 200
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    r = requests.get(url, headers=headers)
    return r.status_code


def delete_container(token, storage_url, container_name):
    """
    Arguments:

        token: authentication token
        storage_url: URL of swift storage
        container_name: container name

    Return: 204 (No Content)
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name])
    r = requests.delete(url, headers=headers)
    return r.status_code


def create_object(token, storage_url, container_name,
                  local_filepath, object_name=None):
    """
    Arguments:

        token: authentication token
        storage_url: URL of swift storage
        container_name: container name
        local_filepath: absolute path of upload file
        object_name: object name (optional)

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
    r = requests.put(url, headers=headers, data=data)
    return r.status_code


def list_objects(token, storage_url, container_name):
    """
    Arguments:

        token: authentication token
        storage_url: URL of swift storage
        container_name: container name
    """
    headers = {'X-Auth-Token': token}
    payload = {'format': 'json'}
    url = utils.generate_url([storage_url, container_name]) + '/'
    r = requests.get(url, headers=headers, params=payload)
    r.encoding = 'utf-8'
    return r.json


def retrieve_object(token, storage_url, container_name, object_name):
    """
    Arguments:

        token: authentication token
        storage_url: URL of swift storage
        container_name: container name
        object_name: object name

    Return: object data
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name, object_name])
    r = requests.get(url,  headers=headers)
    return r.content


def copy_object(token, storage_url, container_name,
                src_object_name, dest_object_name):
    """
    Arguments:

        token: authentication token
        storage_url: URL of swift storage
        container_name: container name
        src_object_name: object name of source
        dest_object_name: object name of destination

    Return: 201 (Created)
    """
    src_url = '/' + utils.generate_url([container_name, src_object_name])
    headers = {'X-Auth-Token': token,
               'Content-Length': "0",
               'X-Copy-From': src_url}

    dest_url = utils.generate_url([storage_url, container_name,
                                   dest_object_name])
    r = requests.put(dest_url, headers=headers)
    return r.status_code


def delete_object(token, storage_url, container_name, object_name):
    """
    Arguments:

        token: authentication token
        storage_url: URL of swift storage
        container_name: container name
        object_name: object name

    Return: 204 (No Content)
    """
    headers = {'X-Auth-Token': token}
    url = utils.generate_url([storage_url, container_name, object_name])
    r = requests.delete(url, headers=headers)
    return r.status_code
