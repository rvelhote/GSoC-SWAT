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
from webhelpers.html import literal

from routes import url_for
from pylons import request, app_globals as g, config

import yaml

class BreadcrumbTrail:
    """ Handles SWAT's Breadcrumb Trail.
    
    The base structure for the Breadcrumb is:
    
    1. Dashboard
    2. [Advanced]
    3. Current Controller if not Dashboard
    4. Current Action if not index
    
    """
    
    def __init__(self, controller, dashboard_first=True):
        """ Constructor. It will initialize the breadcrumb with the controller's
        configuration options and we can also define if the first items will
        the a link to the Dashboard

        Keyword arguments:
        controller -- an object of ControllerConfiguration. should contain
        YAML configuration options, mainly the friendly name parameter
        
        dashboard_first -- defines if the first item in the breadcrumb should
        be a link to the Dashboard
    
        """
	self._items = []
	self._controller = controller
	self._dashboard_first = dashboard_first
    
    def add(self, name, controller_name, action_name = "index"):
	""" Add an item to the Breadcrumb Trail. It will be stored in a
        dictionary with the parameters above.
        
        The controller/action pair will be converted into a link
	
        Keyword arguments:
	name -- items's name
	controller -- controller's name
	action -- action's Name

	"""
        link = url_for(controller = controller_name, action = action_name)
	self._items.append({'name':name, 'link':link})

    def get(self):
	""" Gets the current Breadcrumb Trail Dictionary. This should be used
	in the Breadcrumb Trail's Mako def
	
	"""
	return self._items
    
    def get_is_dashboard_first(self):
        """ Is the Dashboard the first item? """
	return self._dashboard_first

    def build(self, controller=None):
        """ Builds the breadcrumb based on the Controller's Configuration
        parameters.
        
        Optionally, we can build the breadcrumb arbitrarily by passing a
        Controller Configuration object as a parameter
        
        Keyword arguments:
        controller -- optional parameter. a ControllerConfiguration object
        
        """
        controller = self._controller or controller
        
	if self.get_is_dashboard_first():
	    self.add('Dashboard', "dashboard")
	    
	if controller.get_is_advanced():
	    self.add("Advanced Dashboard", "dashboard", "advanced")

	if controller.get_controller() != "dashboard":
	    self.add(controller.get_action_info('friendly_name', 'index'), \
		     controller.get_controller())

	    if controller.get_action() != "index":
		self.add(controller.get_action_info('friendly_name'),
			 controller.get_controller(),
			 controller.get_action())
        
class YamlConfig:
    """ Handles some operations associated with loading and getting stuff from
    YAML files
    
    """
    def y_load(self, filename, dir=''):
        """ Load a YAML file
        
        Keyword arguments:
        filename -- the name of the file to load
        dir -- the directory to load the file from. if empty or ommited it will
        default to the YAML configuration directory in the Paster parameters
        
        """
        file_exists = False
        self.yaml_contents = {}
    
        try:
            stream = open('%s/%s.yaml' % (config['yaml.config'], filename), 'r')
        except IOError:
            file_exists = False
        else:
            file_exists = True
    
        if file_exists:        
            self.yaml_contents = yaml.safe_load(stream)
            stream.close()
    
    def y_get(self, tree):
        """ Get the final value of a YAML tree. For example, if you have your
        YAML file defined as:
        
            #   action:
            #       index:
            #           link: x
        
        and, as the parameter, you pass:
        
            #   y.get('action/index/link')
        
        this method will return:
        
            #   x
            
        if there is no value in this tree, an empty string will be returned
        
        Keyword arguments:
        tree -- the structure to get the value from
        
        """
        value = ""
        
        if len(tree) > 0:
            splitted = tree.split('/')
            value = self.__y_get_recursive(0, len(splitted), \
                                           self.yaml_contents, splitted)

        return value

    
    def __y_get_recursive(self, i, depth, value, items):
        """ Recursive function that goes through the tree to get the final
        value.
        
        This was the best way I could think of to do this. I hope there is a
        better one :)
        
        Each value recursively replaces the previous one. For example, if you
        have your YAML file defined as:
        
            #   action:
            #       index:
            #           link: x
            
        on the first iteration 'value' will be:
        
            #   action:
            #       index:
            #           link: x
            
        on the second iteration 'value' will be:
        
            #   index:
            #       link: x
            
        and so on, until we reach the final item in the depth. Fortunately,
        our YAML files are not very deep :)
        
        Keyword arguments:
        i -- current index
        depth -- tree length
        value -- the current value we have
        items -- the list of tree items
        
        """
        if i < depth - 1 and value.has_key(items[i]):
                value = self.__y_get_recursive(i + 1, depth, value[items[i]], items)
        elif value.has_key(items[i]):
                return value[items[i]]
        else:
                return ""

        return value

class ControllerConfiguration(YamlConfig):
    def __init__(self, controller, action='index'):
	self.__controller = controller
	self.__action = action
        
        filename = '%s' % (controller)
        self.y_load(filename)

    def get_action_info(self, tree, action=''):
        if len(action) == 0:
            action = self.get_action()

        tree = ('actions/%s/%s') % (action, tree)
        return self.y_get(tree)

    def get_is_advanced(self):
        tree = ('controller/is_advanced')
        return self.y_get(tree)

    def get_dashboard_items(self):
        tree = ('dashboard/actions')
	return self.y_get(tree)
        
    def get_dashboard_info(self, tree):
        tree = ('dashboard/%s') % (tree)
        return self.y_get(tree)
        
    def get_toolbar_items(self):
        tree = ('toolbar/%s') % self.get_action()
        return self.y_get(tree)
    
    def get_action(self):
        return self.__action
    
    def get_controller(self):
        return self.__controller

class DashboardConfiguration(YamlConfig):
    def __init__(self):
        self.__items = {}
        self.__layout = []
        
        self.y_load('dashboard')
        
    def load_config(self, type='index'):
	self.__load_layout(type)
	self.__load_layout_items(self.get_layout())

    def __load_layout(self, type='index'):
        tree = ('layout/%s') % type
        self.__layout = self.y_get(tree)

    def __load_layout_items(self, layout=None):
	self.__items = {}
	
	if layout is None:
	    layout = self.get_layout()

	for row in layout:
	    for controller in row['names']:
		self.__items[controller] = ControllerConfiguration(controller)
		
    def get_item(self, name):
	item = None
	
	if self.__items.has_key(name) == True:
	    item = self.__items[name]
	    
	return item		

    def get_items(self):
	return self.__items

    def get_layout(self):
	return self.__layout

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


class MenuConfiguration(YamlConfig):
    def __init__(self, type):
        filename = 'menu.%s' % (type)
        self.y_load(filename)
        
    def get_items(self):
        tree = ('actions')
        return self.y_get(tree)
        
    def get_item_configuration(self, name, tree):
        tree = ('%s/%s') % (name, tree)
        return self.y_get(tree)

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