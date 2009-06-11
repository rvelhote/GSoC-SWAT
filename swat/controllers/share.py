import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render

from swat.lib.helpers import BreadcrumbTrail, ControllerConfiguration, DashboardConfiguration

log = logging.getLogger(__name__)

class ShareController(BaseController):
    """ Share Management controller Will handle all operations concerning
    Shares in SWAT.
    
    """
    
    def __init__(self):
        c.controller_config = ControllerConfiguration()
        
        c.breadcrumb = BreadcrumbTrail(c.controller_config)
        c.breadcrumb.build()        
    
    def index(self):        
        """ Point of entry. """
        c.friendly_controller = 'Share Management'
        c.friendly_action = 'List'
        
        return render('/default/derived/share.mako')
        
    def add(self):
        c.friendly_controller = 'Share Management'
        c.friendly_action = 'Add New Share'
        
        return render('/default/derived/add-share.mako')
    
    def add_assistant(self):
        pass
    
    def save(self):
        pass
    
    def cancel(self):
        pass
    
    def apply(self):
        pass
