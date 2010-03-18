import unittest
import doctest

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import ptc

from archetypes.z3crelationfield.testing import demo_layer

optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE
               )


def test_suite():
    suite = ztc.FunctionalDocFileSuite(
            'field.txt',
            test_class=ptc.FunctionalTestCase,
            optionflags=optionflags
            )
    suite.layer = demo_layer

    return unittest.TestSuite([suite])
