"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html.tags import stylesheet_link, javascript_link
from routes import url_for
from pylons import request

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
    
    items = None
    
    if type is not None and len(type) > 0:
	if type in get_available_menus():
	    
	    if type == "top":
		dashboard_url = url_for(controller = 'dashboard', action = 'index')
		login_url = url_for(controller = 'login', action = 'logout')
		
		items = [{"name" : "dashboard", "link" : dashboard_url}]
		items.append({"name" : "general help", "link" : url_for()})
		items.append({"name" : "context help", "link" : url_for()})
		items.append({"name" : "about", "link" : url_for()})
		items.append({"name" : "logout", "link" : login_url})
		
	    
    
    return items

def get_dashboard_configuration(type):
    """ Gets the layout type for the area defines as type. Theoratically
    the layout will be specified in a configuration will. It will contain
    the number of columns in one row (display) and the names of the
    controllers that will be in that row. With the controller name, another
    file will be accessed with the configuration options for that specific
    controller.
    
    If all goes according to plan, there will be two dashboard type areas.
    One will be the Main Dashboard (Point of Entry for SWAT) and the other
    one will be an Administration Dashboard.
    
    Returns the layout for the specified area.
    
    """
    
    config = None
    
    if type is not None and len(type) > 0:
	config = [{'display' : 2, 'names' : ['share', 'account']},
		    {'display' : 2, 'names' : ['printer', 'help']},
		    {'display' : 1, 'names' : ['administration']}]

    return config

def get_links_for(type, controller_name='', action=''):
    """ Configuration options for a specific controller's widget. Just like
    the layout configuration it's hardcoded for now. If all goes according
    to plan each controller will have a set of specifications in a
    configuration file that will indicate which items and tasks will be
    present at the dashboard.
    
    Returns the Widget's configuration for the controller specified in the
    parameter
    
    """
    
    config = None
    
    if controller_name is None or len(controller_name) <= 0:
	controller_name = request.environ['pylons.routes_dict']['controller']
	
    print controller_name + " - " + type
    
    if controller_name == 'share':
	if type == 'dashboard':
	    config = {  'title_bar' : {'title' : 'Share Management',
			'title_link' : url_for(controller = controller_name),
			'title_icon' : 'folders.png', 'title_link_title' :
					    'Go to the Share Management Area'},

			'actions' : [{'title' : 'add share',
				    'link' : url_for(controller = controller_name, action = 'add'),
				    'link_title' : 'Add a Share',
				    'icon' : 'folder-plus.png',
				    'icon_alt' : 'Add Share Icon'},

				    {'title' : 'list shares',
				    'link' : url_for(controller = controller_name),
				    'link_title' : 'List All Shares',
				    'icon' : 'folders-stack.png',
				    'icon_alt' : 'List Shares Icon'},
				    
				    {'title' : 'add share assistant',
				    'link' : url_for(controller = controller_name, action = 'add_assistant'),
				    'link_title' : 'Add a Share using the Assistant',
				    'icon' : 'wand.png',
				    'icon_alt' : 'Add Share Assistant Icon'}]}

	elif type == 'toolbar':
		# Default
		if action is None or len(action) <= 0 or action == 'default':
		    config = {'actions' : [{'title' : 'add share',
				    'link' : url_for(controller = controller_name, action = 'add'),
				    'link_title' : 'Add a Share',
				    'icon' : 'folder-plus.png',
				    'icon_alt' : 'Add Share Icon'},
			    
			    
				    {'title' : 'add share assistant',
				    'link' : url_for(controller = controller_name, action = 'add_assistant'),
				    'link_title' : 'Add a Share using the Assistant',
				    'icon' : 'wand.png',
				    'icon_alt' : 'Add Share Assistant Icon'}]}
		elif action == 'add':
		    config = {'actions' : [{'title' : 'switch to assistant',
				    'link' : url_for(controller = controller_name, action = 'add_assistant'),
				    'link_title' : 'Switch to Assistant View',
				    'icon' : 'wand.png',
				    'icon_alt' : 'Assistant Icon'},

				    {'title' : 'save',
				    'link' : url_for(controller = controller_name, action = 'save'),
				    'link_title' : 'Save Share Information',
				    'icon' : 'disk.png',
				    'icon_alt' : 'Save Share Icon'},
				    
				    {'title' : 'apply',
				    'link' : url_for(controller = controller_name, action = 'apply'),
				    'link_title' : 'Apply Changes and Return to this Page',
				    'icon' : 'disk-arrow.png',
				    'icon_alt' : 'Apply Changes Icon'},
				     
				    {'title' : 'cancel',
				    'link' : url_for(controller = controller_name, action = 'cancel'),
				    'link_title' : 'Cancel Share Creation',
				    'icon' : 'minus-circle.png',
				    'icon_alt' : 'Cancel Icon'}]}

    return config
    