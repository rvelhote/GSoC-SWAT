from swat.tests import *

class TestShareController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='share', action='index'))
        # Test response...
