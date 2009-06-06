"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html.tags import stylesheet_link, javascript_link
from routes import url_for

def get_samba_server_status():
    """ Gets the current Samba4 status to be used in the CSS class name for the
    top template in the Server Name area.
    
    The icon will indicate if Samba's current status is up or down.
    
    Returns a string "up" or "down" 
    
    """
    
    return "up"

def get_menu(type):
    """ Gets the menu items attributed to a certain menu type. In the
    future these items will be snatched from an XML or other type of
    configuration file but for now they are statically configures
    
    Returns a List containing n dictionary items with the link properties
    (name and link) of the selected menu
    
    """
    
    if type == "top":
	dashboard_url = url_for(controller = 'dashboard', action = 'index')
	login_url = url_for(controller = 'login', action = 'logout')
	
	items = [{"name" : "dashboard", "link" : dashboard_url}]
	items.append({"name" : "general help", "link" : url_for()})
	items.append({"name" : "context help", "link" : url_for()})
	items.append({"name" : "about", "link" : url_for()})
	items.append({"name" : "logout", "link" : login_url})
    
    return items

def get_widget_area_configuration(type):
    """ Gets the layout type for the area defines as type. Theoratically the
    layout will be specified in a configuration will. It will contain the
    number of columns in one row (display) and the names of the controllers
    that will be in that row. With the controller name, another file will be
    accessed with the configuration options for that specific controller.
    
    If all goes according to plan, there will be two dashboard type areas. One
    will be the Main Dashboard (Point of Entry for SWAT) and the other one will
    be an Administration Dashboard.
    
    Returns the layout for the specified area.
    
    """
    
    config = []
    
    if len(type) > 0:    
	config = [{'display' : 2, 'names' : ['share', 'account']},
		    {'display' : 2, 'names' : ['printer', 'help']},
		    {'display' : 1, 'names' : ['administration']}]

    return config

def get_widget_configuration(controller_name):
    config = None
    
    if controller_name == 'share':
	config = {'title_bar' : {'title' : 'Share Management',
				'title_link' : '',
				'title_icon' : 'folders.png',
				'title_link_title' :
					'Go to the Share Management Area'},
	    
		'actions' : [{'title' : 'add share',
			    'link' : '',
			    'link_title' : 'Add a Share',
			    'icon' : 'folder-plus.png',
			    'icon_alt' : 'Add Share Icon'}]}
    
    elif controller_name == 'account':
	pass
    
    elif controller_name:
	pass
	
    
    return config
