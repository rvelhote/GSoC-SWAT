from swat.tests import *
from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, SwatMessages

class TestDashboardController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='dashboard', action='index'))
        assert "Samba Web Administration Tool" in response