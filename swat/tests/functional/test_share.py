from swat.tests import *
from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, SwatMessages

class TestShareController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='share', action='index'))
        # Test response...
