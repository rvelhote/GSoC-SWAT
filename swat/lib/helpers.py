#
# Helper Functions/Classes file for SWAT
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
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html.tags import *

from routes import url_for
from pylons import request, app_globals as g

import yaml

class BreadcrumbTrail:
    """ Handles SWAT's Breadcrumb Trail.
    
    The base structure for the Breadcrumb is:
    
    > Dashboard
    > [Advanced]
    > Current Controller if not Dashboard
    > Current Action if not index
    
    """
    
    def __init__(self, controller, dashboard_first=True):
	self._items = []
	self._controller = controller
	self._dashboard_first = dashboard_first
    
    def add(self, name, controller_name, action_name = "index"):
	""" Add an item to the Breadcrumb Trail
	
	name is a String with the items's name
	controller is a String with the controller's name
	action is a String with the Action's Name
	
	This function will store a dictionary with the above information
	
	"""	    
	self._items.append({'name' : name,
			    'link' : url_for(controller = controller_name, \
					       action = action_name)})

    def get(self):
	""" Gets the current Breadcrumb Trail Dictionary. This should be used
	in the Breadcrumb Trail's Mako def
	
	"""
	return self._items
    
    def get_is_dashboard_first(self):
	return self._dashboard_first
    
    def set_is_dashboard_first(self, is_first=True):
	self._dashboard_first = is_first

    def build(self, controller=None):
	controller = controller or self._controller
	
	if self.get_is_dashboard_first() == True:
	    self.add('Dashboard', "dashboard")
	    
	if controller.get_controller_info("is_advanced") == True:
	    self.add("Advanced Dashboard", "dashboard", "advanced")

	if controller.get_controller() != "dashboard":
	    self.add(controller.get_controller_info('friendly_name'), \
		     controller.get_controller())

	    if controller.get_action() != "index":
		self.add(controller.get_action_info('friendly_name'),
			 controller.get_controller(),
			 controller.get_action())

class ControllerConfiguration:
    """ Each controller will have a configuration file. That information will
    be read at the controller's initialization method.
    
    """
    def __init__(self, controller, action='index'):
	""" Set the controller and action for the specified item and fetch the
	necessary information.
	
	The information that retrieved from a controller's configuration is:
	- Dashboard Items: The items that will apear in the dashboard
	- Toolbar Items: The items that will appear in an action's toolbar
	- Information: General Information regarding the Controller.
	
	"""
        import os
        
	self.__controller = controller
	self.__action = action
        self.__yaml = {}

        file_exists = False

        try:
            stream = open('%s/swat/config/yaml/%s.yaml' % (os.getcwd(), controller), 'r')
        except IOError:
            file_exists = False
        else:
            file_exists = True

        if file_exists:        
            self.__yaml = yaml.safe_load(stream)
            stream.close()

    def get_information(self):
	""" Returns general information about this controller """
        information = {}
        
        if self.__yaml.has_key('information'):
            information = self.__yaml['information']
        
	return information

    def get_controller_info(self, key):
	""" Returns a specific value from the controller info dictionary """
	information = self.get_information()
        value = ''

	if information.has_key('controller'):
            if information['controller'].has_key(key):
                value = information['controller'][key]
	    
	return value
	
    def get_action_info(self, key):
	""" Returns a specific value from the action info dictionary """
	information = self.get_information()
        value = ''

	if information.has_key('action'):
            if information['action'][self.__action].has_key(key):
                value = information['action'][self.__action][key]
	    
	return value
    
    def get_dashboard_items(self):
	""" Returns the Dashboard Items specified for this Controller """
	items = {}
        
        if self.__yaml.has_key('dashboard'):
            items = self.__yaml['dashboard']
            
        return items
    
    def get_toolbar_items(self, action='index'):
	""" Returns the Toolbar Items specifoed for this Controller """
	items = {}

        if self.__yaml.has_key('toolbar'):
            if self.__yaml['toolbar'].has_key(action):
                items = self.__yaml['toolbar'][action]
            
        return items
    
    def get_action(self):
        return self.__action
    
    def get_controller(self):
        return self.__controller

class DashboardConfiguration:
    def __init__(self):
        self.__items = {}
        self.__layout = []
        self.__yaml = {}
        
        file_exists = False

        try:
            stream = open('/home/ric/SWAT/pylons/swat/swat/config/yaml/dashboard.yaml', 'r')
        except IOError:
            file_exists = False
        else:
            file_exists = True

        if file_exists:        
            self.__yaml = yaml.safe_load(stream)
            stream.close()
        
    def load_config(self, type='index'):
	self.__load_layout(type)
	self.__load_layout_items(self.get_layout())

    def __load_layout(self, type='index'):
        if self.__yaml.has_key(type):
            self._layout = self.__yaml[type]

    def __load_layout_items(self, layout=None):
	self._items = {}
	
	if layout is None:
	    layout = self.get_layout()

	for row in layout:
	    for controller in row['names']:
		self._items[controller] = ControllerConfiguration(controller)
		
    def get_item(self, name):
	item = None
	
	if self._items.has_key(name) == True:
	    item = self._items[name]
	    
	return item		

    def get_items(self):
	return self._items

    def get_layout(self):
	return self._layout

class SwatMessages:    
    def __init__(self):
	self._items = []
    
    def add(self, text, type='cool'):
	if len(type) == 0:
	    type = 'cool'
	    
	self._items.append({'text' : text, 'type' : type})
	
    def clean(self):
	del self._items[:]

    def get(self):
	return self._items
    
    def __len__(self):
	return len(self._items)
    
    def any(self):
	has_any = False
	
	if len(self._items) > 0:
	    has_any = True
	    
	return has_any
    
swat_messages = SwatMessages()

def get_samba_server_status():
    """ Gets the current Samba4 status to be used in the CSS class name for the
    top template in the Server Name area.
    
    The icon will indicate if Samba's current status is up or down.
    
    At the moment it uses a very quick way to do it. It just checks if the
    process 'samba' has a pid with 'pidof'. Probably not very portable but it
    works for now :)
    
    Returns a string "up" or "down" 
    
    """

    import commands

    status = "down"

    if len(commands.getoutput("pidof samba")) > 0:
	status = "up"

    return status

def get_menu(type):
    """ Gets the menu items attributed to a certain menu type. In the
    future these items will be snatched from an XML or other type of
    configuration file but for now they are statically configures.
    
    The menu name passed as a parameter will be checked agains a list of
    available menus and if it's there, the appropriate information will be
    returned.
    
    Returns a List containing n dictionary items with the link properties
    (name and link) of the selected menu.
    
    """
    
    items = []
    
    if type == "top":
        dashboard_url = url_for(controller = 'dashboard', action = 'index')
        login_url = url_for(controller = 'authentication', action = 'logout')
        
        items.append({"name" : "dashboard", "link" : dashboard_url})
        items.append({"name" : "general help", "link" : url_for('/')})
        items.append({"name" : "context help", "link" : url_for('/')})
        items.append({"name" : "about", "link" : url_for('/')})
        items.append({"name" : "logout", "link" : login_url})    
    
    return items

def load_yaml_file(filename, dir=''):
    pass

def python_libs_exist():
    import sys, os
    
    exist = False

    try:
        import samba, param
    except ImportError, error:
        pass
    else:
        exist = True
        
    if not exist and os.path.exists("/usr/local/samba/lib/python2.6/site-packages"):
        
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages')
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages/samba')
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages/samba/dcerpc')
        
        try:
            import samba, param
        except ImportError, error:
            swat_messages.add(str(error) \
                + " (in Python Libraries directory and in /usr/local/samba/lib/*)",
                "critical")
        else:
            exist = True
    
    return exist