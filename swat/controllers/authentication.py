import logging, pam

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render
from swat.lib.helpers import swat_messages

log = logging.getLogger(__name__)

class AuthenticationController(BaseController):

    def login(self):
        return render('/default/base/login-screen.mako')
    
    def logout(self):
        redirect_to(controller = 'authentication', action = 'login')
        
    def do(self):
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        
        len_username = len(username)
        len_password = len(password)
        
        if len_username == 0:
            swat_messages.add('Username cannot be empty')
            
        if len_password == 0:
            swat_messages.add('Password cannot be empty')
        
        if len_username > 0 and len_password > 0 and pam.authenticate(username,
                                                                      password):
            
            swat_messages.add('Login successful (as you may have noticed :D)')
            redirect_to(controller = 'dashboard', action = 'index')
        else:
            swat_messages.add('Login Failed. Try Again', 'critical')
            redirect_to(controller = 'authentication', action = 'login')
        
