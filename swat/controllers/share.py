import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ShareController(BaseController):
    """ Share Management controller
    
    Will handle all operations concerning Shares in SWAT
    
    """
    def index(self):
        """ Point of entry. """
        return render('/default/derived/share.mako')
        
    def add(self):
        return render('/default/derived/add-share.mako')
    
    def add_assistant(self):
        pass
    
    def save(self):
        pass
    
    def cancel(self):
        pass
    
    def apply(self):
        pass
