#
# Account Management Controller file for SWAT
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

import param

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render

from pylons.i18n.translation import _

from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, SwatMessages, ParamConfiguration, filter_list

log = logging.getLogger(__name__)

class AccountController(BaseController):
    """ """
    def __init__(self):
        """ """
        me = request.environ['pylons.routes_dict']['controller']
        action = request.environ['pylons.routes_dict']['action']
        
        log.debug("Controller: " + me)
        log.debug("Action: " + action)
        
        c.config = ControllerConfiguration(me, action)
        
        c.breadcrumb = BreadcrumbTrail(c.config)
        c.breadcrumb.build()
            
        c.samba_lp = param.LoadParm()
        c.samba_lp.load_default()
        
    def index(self):
        """ """
        return render('/default/derived/account.mako')
    
    def user(self):
        """ """
        return render('/default/derived/account.mako')
    
    def group(self):
        """ """
        return render('/default/derived/account.mako')
