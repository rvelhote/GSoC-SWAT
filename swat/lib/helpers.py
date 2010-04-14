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
from pylons import request, app_globals as g, config, session

import yaml
import logging

log = logging.getLogger(__name__)

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
        
        dir = dir or config['yaml.config']
    
        try:
            stream = open('%s/%s.yaml' % (dir, filename), 'r')
        except IOError:
            file_exists = False
        else:
            file_exists = True
    
        if file_exists:
            try:
                self.yaml_contents = yaml.safe_load(stream)
            except Exception, msg:
                log.fatal("error parsing the yaml file! -- " + str(msg))
                
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
    
class ParamConfiguration(YamlConfig):
    def __init__(self, filename):
        filename = '%s' % (filename)
        self.y_load(filename)
        
    def get_param(self, id):
        tree = ('%s') % id
        return self.y_get(tree)
        
    def get_value(self, id, tree):
        tree = ('%s/%s') % (id, tree)
        return self.y_get(tree)

class ControllerConfiguration(YamlConfig):
    """ Handles the configuration options for the current controller. Each
    controller should instantiate this class at their init method
    
    Configuration Parameters are read from the YamlConfig file matching the
    controller.
    
    All of the methods in this class are just shorthands for common tasks. We
    could just call YamlConfig.y_get(tree) directly but instead we use
    self.get_action_info for example to get information on the current action.
    
    Extends from YamlConfig.
    
    """
    def __init__(self, controller, action='index'):
        """ Constructor. Does the initial loading of the Yaml File.
        
        Keyword arguments:
        controller -- the controller's name to load
        action -- the current action that the controller is handling. defaults
        to 'index'
        
        """
	self.__controller = controller
	self.__action = action
        
        filename = '%s' % (controller)
        self.y_load(filename)

    def get_action_info(self, tree, action=''):
        """ Gets information on an action that belongs to a controller.
        
        Keyword arguments:
        tree -- the tree of which to get the final value from
        action -- the action to get it from. if empty or ommited it will default
        to the current action.
        
        """
        if len(action) == 0:
            action = self.get_action()

        tree = ('actions/%s/%s') % (action, tree)
        return self.y_get(tree)

    def get_is_advanced(self):
        """ Is this controller advanced or not. Advanced means that it's not
        one of the regular tasks (share, printer, machine management). Something
        such as Log Management
        
        """
        tree = ('controller/is_advanced')
        return self.y_get(tree)

    def get_dashboard_items(self):
        """ Gets the Dashboard Actions attributed to this controller """
        tree = ('dashboard/actions')
	return self.y_get(tree)
        
    def get_dashboard_info(self, tree):
        """ Gets information on the Dashboard 'Widget' regarding this controller
        It's mainly just a list of actions that will appear on the dashboard
        when this controller is listed.
        
        """
        tree = ('dashboard/%s') % (tree)
        return self.y_get(tree)
        
    def get_toolbar_items(self):
        """ Gets the Dashboard Actions attributed to the current action
        
        TODO: make the action name a parameter?
        
        """
        tree = ('toolbar/%s') % self.get_action()
        return self.y_get(tree)
    
    def get_action(self):
        """ Gets the current action name """
        return self.__action
    
    def get_controller(self):
        """ Gets the current controller name """
        return self.__controller

class DashboardConfiguration(YamlConfig):
    """ Handles the Dashboard Configuration Layout """
    def __init__(self):
        """ Initialization and loading of the YAML File """
        self.__items = {}
        self.__layout = []
        
        self.y_load('dashboard')
        
    def load_config(self, type='index'):
        """ Loads the configuration data for a specific dashboard type. The
        dashboard type should be the name of an action defined in the
        controller.
        
        Keyword arguments:
        type -- the action name to load which must be in the YAML file. Defaults
        to 'index'
        
        """
	self.__load_layout(type)
	self.__load_layout_items(self.get_layout())

    def __load_layout(self, type='index'):
        """ Loads the base layout for the specified Dashboard. The layout is
        the number of columns on a row and which controllers are present in
        each slot.
        
        Keyword arguments:
        type -- the action name to load which must be in the YAML file. Defaults
        to 'index'
        
        """
        tree = ('layout/%s') % type
        self.__layout = self.y_get(tree)

    def __load_layout_items(self, layout=None):
        """ Loads the Layout Items (i.e. controller configuration) for each of
        the items present in the Dashboard.
        
        The items member variable will be loaded with an instance of each
        controller's configuration options to be listed.
        
        Keyword arguments:
        layout -- a layout definition. defaults to none and if it's none it will
        load the layout present in the current instance of DashboardConfiguration
        
        """
	self.__items = {}
	
	if layout is None:
	    layout = self.get_layout()

	for row in layout:
	    for controller in row['names']:
		self.__items[controller] = ControllerConfiguration(controller)
		
    def get_item(self, name):
        """ Get a ControllerConfiguration item by name
        
        Keyword arguments:
        name -- the name of the controller to get the configuration
        
        """
	item = None
	
	if self.__items.has_key(name) == True:
	    item = self.__items[name]
	    
	return item		

    def get_items(self):
        """ Gets all the items loaded by the current layout """
	return self.__items

    def get_layout(self):
        """ Gets the current layout """
	return self.__layout

class SwatMessages:
    """ Handles informational messages to be shown to the user after each page
    refresh to provide information on the status of an operation for example.
    
    They are not necessarily show only after a refresh. If the a message is
    provided before it is written in the template it will also appear.
    
    TODO/BUG: Must be stored in sessions otherwise if multiple users are logged
    in there will be a problem of them seeing messages that don't belong to them
    
    """
    @staticmethod
    def add(text, type='cool'):
        """ Add a message to the message queue.
        
        Concerning the message type, it can be anything but to have any
        relevance to the end user it should have the name of a class in the CSS
        file.
        
        By default the available message types are:
        - cool (green)
        - warning (yellow)
        - critical (red)
        
        Keyword arguments:
        text -- the text to show in the message
        type -- the type of message. default value is 'cool'
        
        """
        if len(type) == 0:
            type = 'cool'
            
        if not session.has_key('swat_messages'):
            session['swat_messages'] = []

        session['swat_messages'].append({'text' : text, 'type' : type})
        session.save()

    @staticmethod
    def clean():
        """ Cleanup message queue. This should be called after messages are
        shown in the template
        
        """
        if session.has_key('swat_messages'):
            del session['swat_messages']
            session.save()

    @staticmethod
    def get():
        """ Gets all messages currently stored as a dictionary """
        return session['swat_messages']

    @staticmethod
    def __len__():
        """ Returns the number of messsages in store """
        return len(session['swat_messages'])
    
    @staticmethod
    def any():
        """ Checks if there are any messages in the queue.
        Returns a boolean value
        
        """
        has_any = False

	if session.has_key('swat_messages') and len(session['swat_messages']) > 0:
	    has_any = True
	    
	return has_any

def get_samba_server_status():
    """ Gets the current Samba4 status to be used in the CSS class name for the
    top template in the Server Name area.
    
    The icon will indicate if Samba's current status is up or down.
    
    At the moment it uses a very quick way to do it. It just checks if the
    process 'samba' has a pid with 'pidof'. Probably not very portable but it
    works for now :)
    
    """
    import commands

    status = "down"

    if len(commands.getoutput("pidof samba")) > 0:
	status = "up"

    return status

class MenuConfiguration(YamlConfig):
    """ Handles regular menu items in SWAT. Data is loaded from a YAML file """
    def __init__(self, name, dir=''):
        """ Initialization. Loads the YAML file passed as parameter. Only the
        name of the menu (i.e. top, footer) is required.
        
        The standard naming for yaml file concerning menus is:
        
            #   menu.[name].yaml
            
        Therefore, if you pass only the name, the rest of the string will be
        added for you.
        
        Keyword arguments:
        name -- the menu name
        
        """
        filename = 'menu.%s' % (name)
        self.y_load(filename, dir)
        
    def get_items(self):
        """ Gets all possible actions with this menu. This is basically a list
        of the items that will appear in the referenced menu. The individual
        information of each item is obtained with the get_item_configuration()
        method
        
        """
        tree = ('actions')
        return self.y_get(tree)
        
    def get_item_configuration(self, name, tree):
        """ Gets a certain configuration option for a specified item
        
        Keyword arguments:
        name -- the name of the menu item
        tree -- what to get in
        
        """
        tree = ('%s/%s') % (name, tree)
        return self.y_get(tree)

def python_libs_exist():
    """ Checks if the Samba Python Libraries exist in the Python path. If they
    don't exist the default Samba install directory is checked and if they
    exist, they are added to the Python path.
    
    """
    import sys, os
    
    exist = False

    try:
        import samba, param
    except ImportError, error:
        log.warning("did not find python libraries. will try to add them from the default samba install dir at /usr/local/samba/lib")
    else:
        log.info("python libraries are in the default python path")
        exist = True
        
    if not exist and os.path.exists("/usr/local/samba/lib/python2.6/site-packages"):        
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages')
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages/samba')
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages/samba/dcerpc')
        
        try:
            import samba, param
        except ImportError, error:
            log.fatal("python libs are nowhere to be found!")
        else:
            exist = True
            log.info("python libraries are in samba's default install directory")
    
    return exist

def get_group_list():
    """ Gets this System's Groups to appear in the User/Group Selection Popup """
    import grp
    return grp.getgrall()

def get_user_list():
    """ Gets this System's Users to appear in the User/Group Selection Popup """
    users = []
    groups = get_group_list()

    for g in groups:
        if len(g.gr_mem) > 0:
            users.extend(g.gr_mem)

    users = set(users)
    
    return users

def get_path():
    pass

def filter_list(items, regex='.*'):
    import re
    temp = []
    
    for item in items:
        if re.search(regex, item.get_share_name()) is not None:
            temp.append(item)
            
    return temp
    
    
