#
# Authentication Controller file for SWAT
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#   
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#   
# You should have received a copy of the GNU General Public License
# 
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render
from swat.lib.helpers import SwatMessages

from pylons.i18n.translation import _

log = logging.getLogger(__name__)

class AuthenticationController(BaseController):
    """ Controller that handles the authentication component of SWAT. Uses
    repoze.who with the friendlyform plugin
    
    http://code.gustavonarea.net/repoze.who-friendlyform/
    http://docs.repoze.org/who/
    
    """
    __allow_usernames = ('root', 'ric')
    __reason = ''

    def login(self):
        """ Shows the Login Screen to the user """
        return render('/default/base/login-screen.mako')
    
    def logout(self):
        """ Sends the user to the Login screen. The unsetting of cookies is
        handled by the repoze.who middleware
        
        """
        redirect_to(controller = 'authentication', action = 'login')
        
    def __authenticate(self):
        """ Performs the custom authentication. This method is required by
        repoze and we are sent here by it.
        
        Keyword arguments
        environ -- WSGI environment (request.environ)
        identify -- credentials entered by the user
        
        In case of sucess it returns the username of the user that attempted
        to login otherwise None
        
        TODO: Add i18n here
        BUG: Can't add i18n because for some reason the pylons imports don't
        work here. Maybe I'm using repoze.who wrong?
        
        """
        username = request.params.get("login", "").strip()
        password = request.params.get("password", "").strip()

        len_username = len(username)
        len_password = len(password)

        if len_username == 0:
            SwatMessages.add('Username cannot be empty', 'critical')
            return False
            
        if len_password == 0:
            SwatMessages.add('Password cannot be empty', 'critical')
            return False

        if self.__perform_authentication(username, password):
            SwatMessages.add('Authentication successful!')
            log.info("login attempt successful by " + username)
            request.environ['paste.auth_tkt.set_user'](username)
            
            return True
        
        log.warning("failed login attempt by " + username)
        SwatMessages.add('Authentication failed' + ' -- ' + self.__reason, 'critical')
        
        return False
    
    def __perform_authentication(self, username, password):
        """ Performs User Authentication
        
        Keyword arguments:
        username -- username provided by the login form
        password -- password provided by the login form
        
        """
        from samba import credentials, param
        
        auth_success = False
        
        lp = param.LoadParm()
        lp.load_default()
        
        creds = credentials.Credentials()
        creds.set_username(username)
        creds.set_password(password)
        creds.set_domain("")

        if request.environ.has_key("REMOTE_HOST"):
            creds.set_workstation(request.environ.get("REMOTE_HOST"));
        else:
            creds.set_workstation("")
        
        auth_success =  self.__auth_samr(lp, creds)
        log.info("using samr authentication")
            
        return auth_success

    def __auth_samr(self, lp, credentials):
        """ SAMR Authentication
        
        Keyword arguments:
        lp -- samba configuration file loaded with param.LoadParm
        credentials - Credentials object with the username, password, domain
        and workstation values set

        TODO: Check if user has Administration credentials. Probably something
        to do with the uuid
        
        """
        from samba.dcerpc import samr, security
        
        auth_success = False
        
        try:
            pipe = samr.samr("ncalrpc:", lp, credentials)
            connect_handle = pipe.Connect(None, security.SEC_FLAG_MAXIMUM_ALLOWED)
        except Exception, e:
            self.__reason = str(e)  
        else:
            auth_success = True

        return auth_success

    def do(self):
        """ Stub. Required by repoze.who to be the login_handler_path. I can't
        set this to login otherwise it would just send me to the login method
        
        """
        if self.__authenticate():
            redirect_to(controller='dashboard', action='index')
        else:
            redirect_to(controller='authentication', action='login')
