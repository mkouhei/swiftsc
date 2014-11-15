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
import magic
import inspect
import sys
from io import BytesIO


def return_json(response_json):
    """
    Argument:

        response_json

    Retrun: JSON
    """
    if isinstance(response_json, dict) or isinstance(response_json, list):
        return response_json
    elif inspect.ismethod(response_json):
        # support requests 1.0 over
        return response_json()


def generate_url(partial_uri_list):
    """
    Argument:

        partial_uri_list: patial string of generating URL
                          ex. ["https://swift.example.org", "auth", "v1.0"]

    Return: URL
            ex. "https://swift.example.org/auth/v1.0"
    """
    url = ""
    for i, partial_uri in enumerate(partial_uri_list):
        if i + 1 == len(partial_uri_list):
            url += partial_uri
        else:
            url += partial_uri + "/"
    return url


def check_mimetype(filepath):
    """check mimetype of file

    Argument:

        filename: target filename path
    """
    if hasattr(magic, 'open'):
        # for python-magic package of Debian Wheezy/Sid, Ubuntu 12.04
        mgc = magic.open(magic.MAGIC_MIME)
        mgc.load()
        mimetype = mgc.file(filepath).split('; ')[0]
    elif 'from_file' in dir(magic):
        # for pip install python-magic
        mimetype = magic.from_file(filepath, mime=True)
    else:
        raise RuntimeError("Not support python-magic in this environment")
    if sys.version_info > (3, 0) and isinstance(mimetype, bytes):
        mimetype = mimetype.decode('utf-8')
    return mimetype


def check_mimetype_buffer(fileobj):
    """check mimetype of file

    Argument:

        filename: target filename path
    """
    if 'open' in dir(magic):
        # for python-magic package of Debian Wheezy/Sid, Ubuntu 12.04
        mgc = magic.open(magic.MAGIC_MIME)
        mgc.load()
        mimetype = mgc.buffer(fileobj.read()).split('; ')[0]
    elif 'from_file' in dir(magic):
        # for pip install python-magic
        mimetype = magic.from_buffer(fileobj.read(), mime=True)
    else:
        raise RuntimeError("Not support python-magic in this environment")
    if sys.version_info > (3, 0) and isinstance(mimetype, bytes):
        mimetype = mimetype.decode('utf-8')
    return mimetype


def retrieve_info_from_buffer(file_object):
    """check mimetype of file object

    Argument:

        file_object: target file object
    """
    bio = BytesIO()
    bio.write(file_object.read())
    bio.seek(0)
    mimetype = check_mimetype_buffer(bio)
    bio.seek(0)
    content_length = len(bio.read())
    bio.seek(0)
    data = bio.read()
    bio.close()
    return (mimetype, content_length, data)


def from_file(file_path):
    '''
    Returns: `bool`

    :param file_path: :string:`file path`
    '''
    is_file = True
    if hasattr(file_path, 'fileno'):
        # stdin pipe
        is_file = False
    return is_file
