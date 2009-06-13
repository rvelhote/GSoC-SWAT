"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html.tags import *

from routes import url_for
from pylons import request

class BreadcrumbTrail:
    """ Handles SWAT's Breadcrumb Trail.
    
    The base structure for the Breadcrumb is:
    
    > Dashboard
    > [Advanced]
    > Current Controller if not Dashboard
    > Current Action
    
    """
    
    def __init__(self, controller=None, dashboard_first=True):
	self._items = []
	self._controller = controller
	self._dashboard_first = dashboard_first
    
    def add(self, name, controller_name, action_name = ""):
	""" Add an item to the Breadcrumb Trail
	
	name is a String with the items's name
	controller is a String with the controller's name
	action is a String with the Action's Name
	
	This function will store a dictionary with the above information
	
	"""
	
	if len(action_name) <= 0:
	    action_name = "index"
	    
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
	    
	if controller.get_controller_info('name') != "dashboard":
	    self.add(controller.get_controller_info('friendly_name'), \
		     controller.get_controller_info('name'))

	    if controller.get_action_info("name") != "index":
		self.add(controller.get_action_info('friendly_name'),
			 controller.get_controller_info('name'), \
			 controller.get_action_info('name'))

class ControllerConfiguration:
    """ Each controller will have a configuration file. That information will
    be read at the controller's initialization method.
    
    """
    def __init__(self, controller=None, action='index'):
	""" Set the controller and action for the specified item and fetch the
	necessary information.
	
	The information that retrieved from a controller's configuration is:
	- Dashboard Items: The items that will apear in the dashboard
	- Toolbar Items: The items that will appear in an action's toolbar
	- Information: General Information regarding the Controller.
	
	"""
	self._controller = controller or ""
	self._action = action or ""
	
	self._dashboard_items = self.__dashboard(self._controller)
	self._toolbar_items = self.__toolbar(self._controller, self._action)
	self._information = self.__information(self._controller, self._action)
	
    def get_dashboard_items(self):
	""" Returns the Dashboard Items specified for this Controller """
	return self._dashboard_items
    
    def get_toolbar_items(self):
	""" Returns the Toolbar Items specifoed for this Controller """
	return self._toolbar_items
    
    def get_information(self):
	""" Returns general information about this controller """
	return self._information
    
    def __information(self, controller, action):
	""" The controller's information is divided into two areas. The
	controller's base data and information about each of the actions it
	implements.
	
	This information is used to set the Page Tile and the Breadcrumb trail
	for example
	
	Returns a Dictionary with two keys whose values contain another
	dictionary with the required info.
	
	"""
	
	controller_info = {}
	action_info = {}
	
	if controller == 'dashboard':
	    controller_info = {'is_advanced' : False,
			       'friendly_name' : 'Dashboard',
			       'name' : controller}
	
	    if action == 'index':
		action_info = {'friendly_name' : 'Dashboard',
			       'name' : action}
	
	elif controller == 'share':
	    controller_info = {'is_advanced' : False,
			       'friendly_name' : 'Share Management',
			       'name' : controller}
	    
	    if action == 'index':
		action_info = {'friendly_name' : 'Share List',
			       'page_title' : 'Share Management',
			       'name' : action}
	    elif action == 'add':
		action_info = {'friendly_name' : 'Add New Share',
			       'page_title' : 'Add New Share',
			       'name' : action}

	info = {'controller' : controller_info, 'action' : action_info}

	return info
    
    def get_controller_info(self, key):
	""" Returns a specific value from the controller info dictionary """
	value = ""
	
	if self._information['controller'].has_key(key):
	    value = self._information['controller'][key]
	    
	return value
	
    def get_action_info(self, key):
	""" Returns a specific value from the action info dictionary """
	value = ""
	
	if self._information['action'].has_key(key):
	    value = self._information['action'][key]
	    
	return value

    def __toolbar(self, controller, action):
	""" Gets the Toolbar items for the current controller's action """
	
	config = {}
	
	if controller == 'share':
	    if action == 'index':
		config = {'actions' : [{'title' : 'add share',
				'link' : url_for(controller = controller,
						 action = 'add'),
				'link_title' : 'Add a Share',
				'icon' : 'folder-plus.png',
				'icon_alt' : 'Add Share Icon'},
			
			
				{'title' : 'add share assistant',
				'link' : url_for(controller = controller,
						 action = 'add_assistant'),
				'link_title' : 'Add a Share using the Assistant',
				'icon' : 'wand.png',
				'icon_alt' : 'Add Share Assistant Icon'}]}

	    elif action == 'add':
		config = {'actions' : [{'title' : 'switch to assistant',
				'link' : url_for(controller = controller,
						 action = 'add_assistant'),
				'link_title' : 'Switch to Assistant View',
				'icon' : 'wand.png',
				'icon_alt' : 'Assistant Icon'},
    
				{'title' : 'save',
				'link' : url_for(controller = controller,
						 action = 'save'),
				'link_title' : 'Save Share Information',
				'icon' : 'disk.png',
				'icon_alt' : 'Save Share Icon'},
				
				{'title' : 'apply',
				'link' : url_for(controller = controller,
						 action = 'apply'),
				'link_title' : 'Apply Changes and \
							Return to this Page',
				'icon' : 'disk-arrow.png',
				'icon_alt' : 'Apply Changes Icon'},
				 
				{'title' : 'cancel',
				'link' : url_for(controller = controller,
						 action = 'cancel'),
				'link_title' : 'Cancel Share Creation',
				'icon' : 'minus-circle.png',
				'icon_alt' : 'Cancel Icon'}]}

	return config

    def __dashboard(self, controller):
	""" Configuration options for a specific controller's widget. Just like
	the layout configuration it's hardcoded for now. If all goes according
	to plan each controller will have a set of specifications in a
	configuration file that will indicate which items and tasks will be
	present at the dashboard.
	
	Returns the Widget's configuration for the controller specified in the
	parameter
	
	"""
	
	config = {}
	
	if controller == 'share':
	    config = {  'title_bar' : {'title' : 'Share Management',
			'title_link' : url_for(controller = controller),
			'title_icon' : 'folders.png', 'title_link_title' :
					    'Go to the Share Management Area'},

			'actions' : [{'title' : 'add share',
				    'link' : url_for(controller = controller,
						     action = 'add'),
				    'link_title' : 'Add a Share',
				    'icon' : 'folder-plus.png',
				    'icon_alt' : 'Add Share Icon'},

				    {'title' : 'list shares',
				    'link' : url_for(controller = controller),
				    'link_title' : 'List All Shares',
				    'icon' : 'folders-stack.png',
				    'icon_alt' : 'List Shares Icon'},
				    
				    {'title' : 'add share assistant',
				    'link' : url_for(controller = controller,
						     action = 'add_assistant'),
				    'link_title' : 'Add a Share using the \
								    Assistant',
				    'icon' : 'wand.png',
				    'icon_alt' : 'Add Share Assistant Icon'}]}
    
	return config

class DashboardConfiguration:
    """ Description about the Dashboard's configuration and its items. The
    main members are:
    
    Items: Each controller will have a bunch of items. They will be stored here
    Layout: Information about the Dashboard's layout and the controllers that
    are present
    
    """
    def __init__(self, type='index'):
	""" Sets the layout options for the area defined as type. Theoratically
	the layout will be specified in a configuration will. It will contain
	the number of columns in one row (display) and the names of the
	controllers that will be in that row. With the controller name, another
	file will be accessed with the configuration options for that specific
	controller.
	
	If all goes according to plan, there will be two dashboard type areas.
	One will be the Main Dashboard (Point of Entry for SWAT) and the other
	one will be an Administration Dashboard.
	
	"""
	self._items = {}
	self._layout = []
	
	self.load_layout(type)
	self.load_layout_items()
		
    def load_layout(self, type='index'):
	""" Loads the layout defined in type
	
	All content is loaded into self._layout so you will need to access it
	with the getters
	
	"""
	self._layout = []
	
	if type is None or len(type) == 0:
	    type = 'index'

	if type == 'index':
	    self._layout = [{'display' : 2, 'names' : ['share', 'account']},
			    {'display' : 2, 'names' : ['printer', 'help']},
			    {'display' : 1, 'names' : ['administration']}]

    def load_layout_items(self, layout=None):
	""" Loads the Items present in the layout.
	
	All content is loaded into self._items so you will need to access it
	with the getters
	
	"""
	self._items = {}
	
	if layout is None:
	    layout = self.get_layout()
	
	for row in layout:
	    for controller in row['names']:
		self._items[controller] = ControllerConfiguration(controller)

    def get_items(self):
	""" Gets all the items present in the Dashboard Configuration. Each
	items is a widget.
	
	returns a Dictionary of all items with the key being the controller's
	name
	
	"""
	return self._items;
    
    def get_item(self, name):
	""" Gets a specific item from the items present in the Dashboard
	Configuration.
	
	name is a String with the name of the item we want to fetch
	
	returns and object of type ControllerConfiguration
	
	"""
	return self._items[name]

    def get_layout(self):
	""" Gets the layout specified in the Dashboard configuration. The
	layout is defined by a 'display' which indicated the number os columns
	in a row and 'names' which indicate which controllers and actions will
	be present in the dashboard for that controller
	
	returns a List containing n Dictionaries describing the layout
	
	"""
	return self._layout;
    
class SwatMessages:
    def __init__(self):
	self._items = []
    
    def add(self, text, type='cool'):
	self._items.append({'text' : text, 'type' : type})
	
    def clean(self):
	del self._items[:]

    def get(self):
	return self._items
    
    def any(self):
	has_any = False
	
	if len(self.get()) > 0:
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

def get_available_menus():
    """ Gets all available menus in SWAT. There will be a configuration file to
    specify all of this information but for now it's all static.
    
    Returns a list containing all the available menus for the application.
    
    """
    return ['top']

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
    
    if type is not None and len(type) > 0:
	if type in get_available_menus():
	    if type == "top":
		dashboard_url = url_for(controller = 'dashboard',
							    action = 'index')
		login_url = url_for(controller = 'login', action = 'logout')
		
		items = [{"name" : "dashboard", "link" : dashboard_url}]
		items.append({"name" : "general help", "link" : url_for()})
		items.append({"name" : "context help", "link" : url_for()})
		items.append({"name" : "about", "link" : url_for()})
		items.append({"name" : "logout", "link" : login_url})

    return items
