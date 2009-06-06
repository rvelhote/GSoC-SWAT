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

def get_top_menu_items():
    """ Gets the menu items attributed to the top section of SWAT. In the
    future these items will be snatched from an XML or other type of
    configuration file.
    
    Returns a List containing n dictionary items with the link properties
    (name and link)
    
    """
    
    dashboard_url = url_for(controller = 'dashboard', action = 'index')
    login_url = url_for(controller = 'login', action = 'index')
    
    items = [{"name" : "dashboard", "link" : dashboard_url}]
    items.append({"name" : "general help", "link" : url_for()});
    items.append({"name" : "context help", "link" : url_for()});
    items.append({"name" : "about", "link" : url_for()});
    items.append({"name" : "logout", "link" : login_url});
    
    return items
