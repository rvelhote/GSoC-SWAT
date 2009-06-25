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
import param

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from swat.lib.base import BaseController, render

from pylons.templating import render_mako_def

from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, swat_messages

log = logging.getLogger(__name__)

class ShareController(BaseController):
    """ Share Management controller Will handle all operations concerning
    Shares in SWAT.
    
    """

    def __init__(self):
        me = request.environ['pylons.routes_dict']['controller']
        action = request.environ['pylons.routes_dict']['action']
        
        allowed = ('index', 'add', 'edit', 'add_assistant')
        
        if action in allowed:
            c.controller_config = ControllerConfiguration(me, action)
            
            c.breadcrumb = BreadcrumbTrail(c.controller_config)
            c.breadcrumb.build()
            
            c.samba_lp = param.LoadParm()
            c.samba_lp.load_default()
    
    def index(self):        
        """ Point of entry. """
        return render('/default/derived/share.mako')
        
    def add(self):
        return self.edit('')
    
    def add_assistant(self):
        pass
    
    def edit(self, name):
        c.share_name = name
        return render('/default/derived/edit-share.mako')
        
    def save(self):
        message = "Share Information was Saved"
        swat_messages.add(message)
            
        redirect_to(controller='share', action='index')
        
    def apply(self):
        message = "Share Information was Saved"
        swat_messages.add(message)
            
        redirect_to(controller='share', action='edit', name='test')
    
    def cancel(self, name=''):
        message = "Cancelled Share editing. No changes were saved!"
        swat_messages.add(message, "warning")
            
        redirect_to(controller='share', action='index')
        
    def path(self):
        path = request.params.get('path', '/')
        return render_mako_def('/default/component/popups.mako', 'select_path', \
                               current=path)
