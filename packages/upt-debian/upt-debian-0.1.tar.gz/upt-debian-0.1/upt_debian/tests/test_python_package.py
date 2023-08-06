# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import unittest

import upt

from upt_debian.upt_debian import DebianPythonPackage


class TestPythonPackage(unittest.TestCase):
    def setUp(self):
        upt_pkg = upt.Package('foo', '42')
        self.debian_pkg = DebianPythonPackage(upt_pkg)

    def test_debianize_name(self):
        self.assertEqual(self.debian_pkg.debianize_name('requests'),
                         'python3-requests')
        self.assertEqual(self.debian_pkg.debianize_name('python-glanceclient'),
                         'python3-glanceclient')


if __name__ == '__main__':
    unittest.main()
