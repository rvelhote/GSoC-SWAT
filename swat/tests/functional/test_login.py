from swat.tests import *

class TestLoginController(TestController):

    def test_login(self):
        response = self.app.get(url(controller='login', action='login'))
        # Test response...

    def test_logout(self):
        response = self.app.get(url(controller='login', action='logout'))
        # Test response...