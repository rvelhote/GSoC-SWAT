import swat.lib.helpers as th

def test_get_samba_server_status():
    """ Test for the Server Status helper. Ensures that the status is only
    'up' or 'down'
    
    """
    
    assert th.get_samba_server_status() == "up" \
	or th.get_samba_server_status() == "down", \
	'Server status should be "up" or "down"'
    
def test_get_menu_type_empty():
    """ When the type is empty, the method should return None """
    
    type = ""
    assert th.get_menu(type) is None

def test_get_menu_type_none():
    """ When the type is None, the method should return None """
    
    type = ""
    assert th.get_menu(type) is None