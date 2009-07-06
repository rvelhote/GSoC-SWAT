import logging, pam

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render
from swat.lib.helpers import swat_messages

from pylons.i18n.translation import _

log = logging.getLogger(__name__)

class AuthenticationController(BaseController):
    
    allow_usernames = ('root', 'ric')

    def login(self):
        return render('/default/base/login-screen.mako')
    
    def logout(self):
        redirect_to(controller = 'authentication', action = 'login')
        
    def authenticate(self, environ, identity):
        username = identity['login']
        password = identity['password']
        
        len_username = len(username)
        len_password = len(password)        
        
        if len_username == 0:
            swat_messages.add('Username cannot be empty', 'critical')
            
        if len_password == 0:
            swat_messages.add('Password cannot be empty', 'critical')
            
        if username not in self.allow_usernames:
            swat_messages.add('That username is not allowed to login to SWAT')        
        
        if pam.authenticate(username, password):
            swat_messages.add('Authentication successful!')
            return username
        
        swat_messages.add('Authentication failed. Try Again', 'critical')
        
        return None        
        
    def do(self):
        pass
