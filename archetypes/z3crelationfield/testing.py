from Testing import ZopeTestCase
from collective.testcaselayer import ptc, common

from example.dexterity.tests import test_integration
test_integration  # importing initiates setup


class DemoLayer(ptc.BasePTCLayer):
    """
    """

    def afterSetUp(self):
        """
        Arguments:
        - `self`:
        """
        from example.dexterity.tests import test_integration
        test_integration  # import installs example Dexterity types
        ZopeTestCase.installPackage('archetypes.z3crelationfield')
        self.addProfile('archetypes.z3crelationfield:demo')
        self.portal.portal_catalog.refreshCatalog()
        self.login()
        self.folder.invokeFactory(
            type_name='example.ttwpage',
            id='dexterity_1', title='Dexterity 1')
        self.folder.invokeFactory(
            type_name='ZCRelationFieldDemoContent',
            id='atct_1', title='ATCT 1')

demo_layer = DemoLayer([common.common_layer])
