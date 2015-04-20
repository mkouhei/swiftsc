# -*- coding: utf-8 -*-
""" swiftsc utility module. """
import magic
import sys
from io import BytesIO


def check_mimetype(filepath):
    """ Check mimetype of file.

    :rtype: str
    :return: mimetype

    :param str filepath: target filename path
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
    """ Check mimetype of file.

    :rtype: str
    :return: mimetype

    :param fileobj: target filename path
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
    """ Check mimetype of file object.

    :rtype: tuple
    :return: mimetype, content length, data

    :param file_object: target file object
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
    """ Check file.

    .. warning::
        This method is deprecated, will be removed in version 0.7.0.

    :rtype: bool
    :return: True is file object

    :param str file_path: file path
    """
    is_file = True
    if hasattr(file_path, 'fileno'):
        # stdin pipe
        is_file = False
    return is_file
