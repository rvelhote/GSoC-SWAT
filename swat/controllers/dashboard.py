import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render
from routes import url_for

log = logging.getLogger(__name__)

class DashboardController(BaseController):

    def index(self, type = 'main'):
        c.messages = []
        c.dashboard_type = type
        
        c.layout = self.__get_dashboard_configuration(type)
        c.widgets = self.__get_all_widgets(type, c.layout)
        
        return render('/default/derived/dashboard.mako')

    def __get_dashboard_configuration(self, type):
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
    
    def __get_all_widgets(self, type, layout):
        """ Gets all Widgets present in a certain layout
        
        Returns a Dictinary of Widgets will each of their configuration options.
        
        """
        
        widgets = {}
        
        for row in layout:
            for name in row['names']:
                widgets[name] = self.__get_widget_configuration(name)

        return widgets
            
    def __get_widget_configuration(self, controller_name):
        """ Configuration options for a specific controller's widget. Just like
        the layout configuration it's hardcoded for now. If all goes according
        to plan each controller will have a set of specifications in a
        configuration file that will indicate which items and tasks will be
        present at the dashboard.
        
        Returns the Widget's configuration for the controller specified in the
        parameter
        
        """
        
        config = None
        
        if len(controller_name) > 0:
            if controller_name == 'share':
                config = {  'title_bar' : {'title' : 'Share Management',
                                        'title_link' : url_for(controller = controller_name),
                                        'title_icon' : 'folders.png',
                                        'title_link_title' :
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
                                        'icon_alt' : 'List Shares Icon'}]}
        
        return config