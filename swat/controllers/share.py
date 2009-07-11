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
from pylons.i18n.translation import _
from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, swat_messages

log = logging.getLogger(__name__)

class ShareController(BaseController):
    """ Share Management controller Will handle all operations concerning
    Shares in SWAT.
    
    """

    def __init__(self):
        """ Initialization. Load the controller's configuration, builds the
        breadcrumb trail based on that information and load the backend
        information
        
        There are a few operations that don't require this initialization e.g.
        save, apply, cancel; they always redirect somewhere. therefore, there
        is a list of allowed operations that is checked to see if it's ok to
        load the configuration
        
        """
        me = request.environ['pylons.routes_dict']['controller']
        action = request.environ['pylons.routes_dict']['action']
        
        allowed = ('index', 'add', 'edit', 'add_assistant')
        
        if action in allowed:
            c.config = ControllerConfiguration(me, action)
            
            c.breadcrumb = BreadcrumbTrail(c.config)
            c.breadcrumb.build()
            
            c.samba_lp = param.LoadParm()
            c.samba_lp.load_default()
    
    def index(self):        
        """ Point of entry. Loads the Share List Template """
        return render('/default/derived/share.mako')
        
    def add(self):
        """ Add a New Share. Loads the Share Edition Template. It's the same as
        calling the edit template but with an empty share name
        
        """
        return self.edit('')
    
    def add_assistant(self):
        pass
    
    def edit(self, name):
        """ Edit a share. Loads the Share Edition Template.
        
        Keyword arguments:
        name -- the share name to load the information from
        
        """
        c.share_name = name
        return render('/default/derived/edit-share.mako')
        
    def save(self):
        message = _("Share Information was Saved")
        swat_messages.add(message)
        
        print request.params
            
        redirect_to(controller='share', action='index')
        
    def apply(self):
        message = _("Share Information was Saved")
        swat_messages.add(message)
            
        redirect_to(controller='share', action='edit', name='test')
    
    def cancel(self, name=''):
        message = _("Cancelled Share editing. No changes were saved!")
        swat_messages.add(message, "warning")
            
        redirect_to(controller='share', action='index')
        
    def path(self):
        path = request.params.get('path', '/')
        return render_mako_def('/default/component/popups.mako', 'select_path', \
                               current=path)
        
    def users_groups(self):
        return render_mako_def('/default/component/popups.mako', \
                               'select_user_group')
        
    def remove(self):
        pass
    
    def copy(self):
        pass
    
    def toggle(self):
        pass
