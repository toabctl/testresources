#
#  testresources: extensions to python unittest to allow declaritive use
#  of resources by test cases.
#  Copyright (C) 2005  Robert Collins <robertc@robertcollins.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import testresources
from testresources.tests import SampleTestResource
import unittest


class TestResourcedTestCase(unittest.TestCase):

    def testDefaults(self):
        case = testresources.ResourcedTestCase("run")
        case.setUpResources()
        case.tearDownResources()
        self.assertEqual(case.resources, [])

    def testSingleResource(self):
        case = testresources.ResourcedTestCase("run")
        case.resources = [("_default", SampleTestResource)]
        case.setUpResources()
        self.assertEqual(case._default,
                         "You need to implement your own "
                         "getResource.")
        self.assertEqual(SampleTestResource._uses, 1)
        case.tearDownResources()
        self.failIf(hasattr(case, "_default"))
        self.assertEqual(SampleTestResource._uses, 0)

    def testSingleWithSetup(self):
        case = testresources.ResourcedTestCase("run")
        case.resources = [("_default", SampleTestResource)]
        case.setUp()
        self.assertEqual(case._default,
                         "You need to implement your own "
                         "getResource.")
        self.assertEqual(SampleTestResource._uses, 1)
        case.tearDown()
        self.failIf(hasattr(case, "_default"))
        self.assertEqual(SampleTestResource._uses, 0)

    def testMultipleResources(self):

        class MockResource(testresources.TestResource):

            @classmethod
            def makeResource(self):
                return "Boo!"

        case = testresources.ResourcedTestCase("run")
        case.resources = [("_default", SampleTestResource),
                          ("_mock", MockResource)]
        case.setUpResources()
        self.assertEqual(case._default,
                         "You need to implement your own "
                         "getResource.")
        self.assertEqual(case._mock, "Boo!")
        self.assertEqual(SampleTestResource._uses, 1)
        self.assertEqual(MockResource._uses, 1)
        case.tearDownResources()
        self.failIf(hasattr(case, "_default"))
        self.assertEqual(SampleTestResource._uses, 0)
        self.failIf(hasattr(case, "_mock"))
        self.assertEqual(MockResource._uses, 0)


def test_suite():
    loader = testresources.tests.TestUtil.TestLoader()
    result = loader.loadTestsFromName(__name__)
    return result
