#
# Share Management Controller file for SWAT
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
from pylons import app_globals as g

from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, SwatMessages

log = logging.getLogger(__name__)

class ShareController(BaseController):
    """ Share Management controller Will handle all operations concerning
    Shares in SWAT.
    
    """

    def __init__(self):
        me = request.environ['pylons.routes_dict']['controller']
        c.controller_config = ControllerConfiguration(me)
        
        c.breadcrumb = BreadcrumbTrail(c.controller_config)
        c.breadcrumb.build()
    
    def index(self):        
        """ Point of entry. """
        return render('/default/derived/share.mako')
        
    def add(self):
        return render('/default/derived/add-share.mako')
    
    def add_assistant(self):
        pass
