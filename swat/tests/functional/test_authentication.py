from swat.tests import *

class TestAuthenticationController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='authentication', action='index'))
        # Test response...
