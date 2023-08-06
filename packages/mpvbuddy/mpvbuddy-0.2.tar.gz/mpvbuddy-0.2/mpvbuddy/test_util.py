import unittest

from mpvbuddy.util import filename_from_url, abs_path_from_url


class UtilTest(unittest.TestCase):

    def test_file_from_url(self):
        self.assertEqual(filename_from_url('file:///a/b/c/d.mpeg'), 'd.mpeg')
        self.assertEqual(filename_from_url('file:///foo/bar/This%20Is%20A%20Name.mpeg'), 'This Is A Name.mpeg')

    def test_abs_path_from_url(self):
        self.assertEqual(abs_path_from_url('file:///a/b/c/d.mpeg'), '/a/b/c/d.mpeg')
        self.assertEqual(abs_path_from_url('file:///foo/bar/This%20Is%20A%20Name.mpeg'), '/foo/bar/This Is A Name.mpeg')
