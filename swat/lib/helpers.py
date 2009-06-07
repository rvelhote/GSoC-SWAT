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
    
    return "down"

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
	    dashboard_url = url_for(controller = 'dashboard', action = 'index')
	    login_url = url_for(controller = 'login', action = 'logout')
	    
	    items = [{"name" : "dashboard", "link" : dashboard_url}]
	    items.append({"name" : "general help", "link" : url_for()})
	    items.append({"name" : "context help", "link" : url_for()})
	    items.append({"name" : "about", "link" : url_for()})
	    items.append({"name" : "logout", "link" : login_url})
    
    return items


def get_swat_messages():
    return None