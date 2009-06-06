import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render

from swat.lib.helpers import get_swat_messages

log = logging.getLogger(__name__)

class DashboardController(BaseController):

    def index(self):
        c.messages = get_swat_messages()
        return render('/default/derived/dashboard.mako')
