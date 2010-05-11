import logging
from samba import param

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render

from swat.lib.helpers import ControllerConfiguration, BreadcrumbTrail, \
SwatMessages

log = logging.getLogger(__name__)

class HelpController(BaseController):
    """ """
    def __init__(self):
        """ """
        me = request.environ['pylons.routes_dict']['controller']
        action = request.environ['pylons.routes_dict']['action']
        
        c.config = ControllerConfiguration(me, action)
        
        c.breadcrumb = BreadcrumbTrail(c.config)
        c.breadcrumb.build()
        
        c.samba_lp = param.LoadParm()
        c.samba_lp.load_default()
        
    def index(self):
        """ """
        return render('/default/derived/help.mako')
        
    def module(self):
        """ """
        c.help_module_name = request.params.get("name")
        c.help_module_action = request.params.get("action")
        
        return render('/default/derived/help.mako')
        
    def about(self):
        """ """
        return render('/default/derived/help/about.mako')
