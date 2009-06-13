import swat.lib.helpers as th
from pylons import session
    
def test_get_menu():
    type = ""
    assert len(th.get_menu(type)) == 0, 'When there is no type it should return an empty list'

    type = "top"
    assert isinstance(th.get_menu(type), list) == True, 'When the menu exists return type should be a list'
    
    type = ""
    assert isinstance(th.get_menu(type), list) == True, 'Return type should always be a list'    

    type = "top"
    assert len(th.get_menu(type)) > 0, 'Length of the  returned list should be > 0'

    type = "vandelayindustries"
    assert len(th.get_menu(type)) == 0, 'When the menu doesn\'t exist an empty list should be returned'

def test_get_samba_server_status():
    assert th.get_samba_server_status() == "up" or \
	    th.get_samba_server_status() == "down", 'Status should always be "up" or "down"'
