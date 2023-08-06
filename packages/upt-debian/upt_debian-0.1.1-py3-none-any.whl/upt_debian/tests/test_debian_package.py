# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import unittest
from unittest import mock

import upt

from upt_debian.upt_debian import DebianPackage


class TestDebianPackage(unittest.TestCase):
    def setUp(self):
        upt_pkg = upt.Package('foo', '42')
        self.debian_pkg = DebianPackage(upt_pkg)

    def test_name(self):
        self.assertEqual(self.debian_pkg.name, 'foo')

    def test_homepage(self):
        self.debian_pkg.upt_pkg.homepage = 'homepage'
        self.assertEqual(self.debian_pkg.homepage, 'homepage')

    def test_description(self):
        self.debian_pkg.upt_pkg.description = 'Description'
        self.assertEqual(self.debian_pkg.description, 'Description')

    def test_summary(self):
        self.debian_pkg.upt_pkg.summary = 'Summary'
        self.assertEqual(self.debian_pkg.summary, 'Summary')

    def test_version(self):
        self.assertEqual(self.debian_pkg.version, '42')

    def test_debianize_version_specifier(self):
        test_data = [
            ('==42', '=42'),
            ('>=42', '>=42'),
            ('>42', '>>42'),
            ('<=42', '<=42'),
            ('<42', '<<42')
        ]
        for (upt_version, debian_version) in test_data:
            out = self.debian_pkg._debianize_version_specifier(upt_version)
            self.assertEqual(out, debian_version)

    def test_debianize_requirement(self):
        self.debian_pkg.debianize_name = lambda x: x
        test_data = [
            (upt.PackageRequirement('foo', '>1.2'), 'foo (>>1.2)'),
            (upt.PackageRequirement('foo', '>1,<3'), 'foo (>>1), foo (<<3)'),
            (upt.PackageRequirement('foo'), 'foo'),
        ]
        for (upt_req, debian_req) in test_data:
            out = self.debian_pkg.debianize_requirement(upt_req)
            self.assertEqual(out, debian_req)


class TestDirectoryCreation(unittest.TestCase):
    def setUp(self):
        upt_pkg = upt.Package('foo', '42')
        self.debian_pkg = DebianPackage(upt_pkg)

    @mock.patch('os.makedirs', side_effect=PermissionError)
    def test_create_directories_permission_error(self, m_makedirs):
        with self.assertRaises(SystemExit):
            self.debian_pkg._create_output_directories()

    @mock.patch('os.makedirs', side_effect=FileExistsError)
    def test_create_directories_file_exists(self, m_makedirs):
        with self.assertRaises(SystemExit):
            self.debian_pkg._create_output_directories()


if __name__ == '__main__':
    unittest.main()
