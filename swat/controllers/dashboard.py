#
# Dashboard Controller file for SWAT
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
from routes import url_for

from pylons.i18n.translation import _

from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, SwatMessages, swat_messages

log = logging.getLogger(__name__)

class DashboardController(BaseController):
    
    def __init__(self):
        me = request.environ['pylons.routes_dict']['controller']
        type = request.environ['pylons.routes_dict']['action']

        c.config = ControllerConfiguration(me, type)

        c.dash = DashboardConfiguration()
        c.dash.load_config(type)

        c.breadcrumb = BreadcrumbTrail(c.config)
        c.breadcrumb.build()
        
        c.samba_lp = param.LoadParm()
        c.samba_lp.load_default()

    def index(self):
        identity = request.environ.get('repoze.who.identity')
        
        if identity is None:
            swat_messages.add(_("You must be authenticated to perform that action"), "critical")
            abort(401)
        
        """ The default Dashboard. The entry point for SWAT """
        return render('/default/derived/dashboard.mako')
        
    def advanced(self):
        """ The advanced layout for the Dashboard is exactly the same as the
        'normal' dashboard. The only difference is the items that are loaded
        and the Breadcrumb Trail
        
        """
        return render('/default/derived/dashboard.mako')
