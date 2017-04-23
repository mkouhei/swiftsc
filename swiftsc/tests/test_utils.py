# -*- coding: utf-8 -*-
"""swiftsc.utils unit tests."""
import unittest
from swiftsc import utils as u
from swiftsc.tests import test_vars as v


class UtilsTests(unittest.TestCase):

    """Unit test of utils.py"""

    def test_check_mimetype(self):
        """test checking mimetype"""
        self.assertEqual(v.TEST_FILE_MIMETYPE,
                         u.check_mimetype(v.TEST_FILE))

    def test_check_mimetype_buffer(self):
        """test checking mimetype of buffer"""
        fileobj = open(v.TEST_FILE, 'rb')
        self.assertEqual(v.TEST_FILE_MIMETYPE,
                         u.check_mimetype_buffer(fileobj))
        fileobj.close()

    def test_retrieve_info_from_buffer(self):
        """test retriving info from buffer"""
        fileobj = open(v.TEST_FILE, 'rb')
        file_content = fileobj.read()
        fileobj.seek(0)
        self.assertEqual((v.TEST_FILE_MIMETYPE,
                          v.TEST_FILE_SIZE,
                          file_content),
                         u.retrieve_info_from_buffer(fileobj))
        fileobj.close()
