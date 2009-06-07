import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ShareController(BaseController):

    def index(self):
        return render('/default/derived/share.mako')
