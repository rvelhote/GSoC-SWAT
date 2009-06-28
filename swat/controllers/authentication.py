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
        
    def do(self):
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        
        len_username = len(username)
        len_password = len(password)
        
        if len_username == 0:
            swat_messages.add(_('Username cannot be empty'))
            
        if len_password == 0:
            swat_messages.add(_('Password cannot be empty'))
            
        if username not in self.allow_usernames:
            swat_messages.add(_('That username is not allowed to login to SWAT'))

        if username in self.allow_usernames and len_username > 0 \
            and len_password > 0 and pam.authenticate(username, password):
            
            swat_messages.add(_('Authentication successful!'))
            redirect_to(controller = 'dashboard', action = 'index')
        else:
            swat_messages.add(_('Authentication failed. Try Again'), 'critical')
            redirect_to(controller = 'authentication', action = 'login')
        
