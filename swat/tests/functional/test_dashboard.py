from swat.tests import *

class TestDashboardController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='dashboard', action='index'))
        # Test response...
