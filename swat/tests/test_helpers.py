from swat.lib.helpers import *
from pylons import session
    
def test_get_menu():
    type = ""
    assert len(get_menu(type)) == 0, 'When there is no type it should return an empty list'

    type = "top"
    assert isinstance(get_menu(type), list) == True, 'When the menu exists return type should be a list'
    
    type = ""
    assert isinstance(get_menu(type), list) == True, 'Return type should always be a list'    

    type = "top"
    assert len(get_menu(type)) > 0, 'Length of the  returned list should be > 0'

    type = "vandelayindustries"
    assert len(get_menu(type)) == 0, 'When the menu doesn\'t exist an empty list should be returned'

def test_get_samba_server_status():
    assert get_samba_server_status() == "up" or \
	    get_samba_server_status() == "down", 'Status should always be\
								"up" or "down"'

class TestDashboardConfiguration():
    def test_initialization(self):
	config = DashboardConfiguration("index")
	assert len(config.get_layout()) > 0
	
	layout = config.get_layout()
	assert layout[0].has_key('display') and layout[0].has_key('names') == True
	