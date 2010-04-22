from swat.tests import *

class TestAuthenticationController(TestController):
    def test_authentication_success(self):
        #self.username = "Administrator"
        #self.password = "x"
        #
        #response = self.app.get(url(controller='authentication', action='do'),
        #                        params={'login': self.username,
        #                                'password': self.password
        #                        },
        #                        status=302)
        #
        #assert response.status == "302 Found", "Authentication should redirect"
        #assert 'Set-Cookie' in response.headers, "If sucessful a cookie must be in response"
        #
        #self.app.reset()
        pass

    def test_authentication_fail(self):
        #self.username = "Administrator"
        #self.password = "xorg"
        #
        #response = self.app.get(url(controller='authentication', action='do'),
        #                        params={'login': self.username,
        #                                'password': self.password
        #                        },
        #                        status=302)
        #
        #assert response.status == "302 Found", "Authentication should redirect"
        #assert 'Set-Cookie' not in response.headers, "No cookie should be in response"
        #
        #self.app.reset()
        pass
        
    def test_authentication_sucess_redirect(self):
        #self.username = "Administrator"
        #self.password = "x"
        #
        #response = self.app.get(url(controller='authentication', action='do'),
        #                        params={'login': self.username,
        #                                'password': self.password
        #                        },
        #                        status=302)
        #
        #assert 'Authentication successful!' in response.follow(), "There should be a success message"
        #
        #self.app.reset()
        pass

    def test_authentication_fail_redirect(self):
        """ Not working at the moment """
        #self.username = "Administrator"
        #self.password = "xorg"
        #
        #response = self.app.get(url(controller='authentication', action='do'),
        #                        params={'login': self.username,
        #                                'password': self.password
        #                        },
        #                        status=302)
        #
        #assert 'Authentication failed. Try Again' in response.follow(), "There should be a fail message"
        #
        #self.app.reset()
        pass
        