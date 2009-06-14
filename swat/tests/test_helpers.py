#
# Test Cases for Helper Methods/Functions
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#   
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#   
# You should have received a copy of the GNU General Public License
# 
from swat.lib.helpers import *
from pylons import session
from nose import with_setup
    
def test_get_menu_empty_type():
    type = ""
    assert len(get_menu(type)) == 0, 'When there is no type it should return an\
								    empty list'

def test_get_menu_valid_type():
    type = "top"
    assert len(get_menu(type)) > 0, 'Length of the  returned list should be > 0'
    

def test_get_menu_invalid_type():
    type = "vandelayindustries"
    assert len(get_menu(type)) == 0, 'When the menu doesn\'t exist an empty\
							list should be returned'

def test_get_samba_server_status():
    assert get_samba_server_status() == "up" or \
	    get_samba_server_status() == "down", 'Status should always be\
								"up" or "down"'

class TestDashboardConfiguration():
    def __init__(self):
	self.dash_obj = DashboardConfiguration('index')

    def test_layout_keys(self):
	layout = self.dash_obj.get_layout()
	for row in layout:
	    assert row.has_key('display') and row.has_key('names') == True
	
    def test_load_layout_good(self):
	self.dash_obj.load_layout('index')
	assert len(self.dash_obj.get_layout()) > 0
	
    def test_load_layout_bad(self):
	self.dash_obj.load_layout('bad-index')
	assert len(self.dash_obj.get_layout()) == 0

    def test_get_item_empty(self):
	assert self.dash_obj.get_item('') is None
	
    def test_get_item_invalid(self):
	assert self.dash_obj.get_item('invalid-item') is None
	
    def test_get_item_good(self):
	assert isinstance(self.dash_obj.get_item('share'), ControllerConfiguration)

class TestSwatMessages():
    def __init__(self):
	self.m = SwatMessages()
	
    def test_add(self):
	type = 'cool'
	text = 'test message'
	
	self.m.add(text, type)
	assert self.m.any() == True
	
    def test_clear(self):
	type = 'cool'
	text = 'test message'
	
	self.m.add(text, type)
	self.m.clean()
	assert self.m.any() == False
	
    def test_any(self):
	type = 'cool'
	text = 'test message'
	
	self.m.add(text, type)
	assert self.m.any() == True
	
	self.m.clean()
	assert self.m.any() == False	
	