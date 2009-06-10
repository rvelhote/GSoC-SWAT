import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render
from routes import url_for

from swat.lib.helpers import BreadcrumbTrail, ControllerConfiguration, DashboardConfiguration

log = logging.getLogger(__name__)

class DashboardController(BaseController):
    
    def __init__(self):
        c.dashboard_type = request.environ['pylons.routes_dict']['action']
        c.dashboard_config = DashboardConfiguration(c.dashboard_type)

    def index(self):
        return render('/default/derived/dashboard.mako')
        
    def advanced(self):
        c.friendly_controller = 'Advanced Administration'
        
        return render('/default/derived/dashboard.mako')
            