import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render
from routes import url_for

log = logging.getLogger(__name__)

class DashboardController(BaseController):

    def index(self, type = 'main'):
        c.messages = []
        c.dashboard_type = type
        
        return render('/default/derived/dashboard.mako')
            