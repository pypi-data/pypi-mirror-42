# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import unittest

import upt

from upt_freebsd.upt_freebsd import FreeBSDRubyPackage


class TestRubyPackage(unittest.TestCase):
    def setUp(self):
        upt_pkg = upt.Package('foo', '42')
        self.freebsd_pkg = FreeBSDRubyPackage(upt_pkg, None)

    def test_freebsd_pkg_name(self):
        out = self.freebsd_pkg._freebsd_pkg_name('cogbot')
        self.assertEqual(out, 'rubygem-cogbot')

    def test_jinja2_reqformat(self):
        req = upt.PackageRequirement('cinch', '>=2.3.3')
        out = self.freebsd_pkg.jinja2_reqformat(req)
        expected = 'rubygem-cinch>=2.3.3:XXX/rubygem-cinch'
        self.assertEqual(out, expected)

    def test_jinja2_reqformat_no_specifier(self):
        req = upt.PackageRequirement('cinch', '')
        out = self.freebsd_pkg.jinja2_reqformat(req)
        expected = 'rubygem-cinch>0:XXX/rubygem-cinch'
        self.assertEqual(out, expected)


if __name__ == '__main__':
    unittest.main()
