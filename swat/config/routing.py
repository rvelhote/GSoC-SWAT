"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper
from swat.lib.helpers import python_libs_exist

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'], explicit=True)
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    #
    #   Default root for Application.
    #   For now it's marked as the dashboard because I'm not implementing the
    #   login right away.
    #
    if python_libs_exist():
        map.connect('/', controller='dashboard', action='index')
    else:
        map.connect('/', controller='error', action='no_libs')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{subaction}', subaction='add')
    map.connect('share_action', '/{controller}/{action}/{name}', controller='share')
    map.connect('account_action', '/{controller}/{action}/{subaction}/{id}', controller='account')

    return map
