import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AuthenticationController(BaseController):

    def login(self):
        return render('/default/base/login-screen.mako')
    
    def logout(self):
        redirect_to(controller = 'authentication', action = 'login')
        
    def do(self):
        redirect_to(controller = 'dashboard', action = 'index')
