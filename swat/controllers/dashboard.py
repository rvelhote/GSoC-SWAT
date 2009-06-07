import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render
from routes import url_for

log = logging.getLogger(__name__)

class DashboardController(BaseController):

    def index(self):
        c.dashboard_type = 'main'
        c.friendly_controller = 'Dashboard'
        
        return render('/default/derived/dashboard.mako')
        
    def advanced(self):
        c.dashboard_type = 'advanced'
        c.friendly_controller = 'Advanced Administration'
        
        return render('/default/derived/dashboard.mako')
            