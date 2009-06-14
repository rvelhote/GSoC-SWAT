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

class TestMenu():
    def test_get_menu_empty_type(self):
	type = ""
	assert len(get_menu(type)) == 0, 'When there is no type it should return an empty list'

    def test_get_menu_valid_type(self):
	type = "top"
	assert len(get_menu(type)) > 0, 'Length of the  returned list should be > 0'

    def test_get_menu_invalid_type(self):
	type = "vandelayindustries"
	assert len(get_menu(type)) == 0, 'When the menu doesn\'t exist an empty list should be returned'

class TestSambaServerStatus():
    def test_get_samba_server_status(self):
	status = get_samba_server_status()
        assert status == "up" or status == "down", 'Status should always be "up" or "down"'

class TestDashboardConfiguration():
    def setUp(self):
	self.d = DashboardConfiguration()

    def tearDown(self):
	pass

    def test_layout_keys(self):
	self.d.load_layout('index')
	layout = self.d.get_layout()

	for row in layout:
	    assert row.has_key('display') and row.has_key('names') == True
	
    def test_load_layout_good(self):
	self.d.load_layout('index')
	layout = self.d.get_layout()
	assert len(layout) > 0
	
    def test_load_layout_bad(self):
	self.d.load_layout('bad-index')
	layout = self.d.get_layout()
	assert len(layout) == 0

    def test_get_item_empty(self):
	self.d.load_layout('index')
	layout = self.d.get_layout()
	
	self.d.load_layout_items(layout)
	assert self.d.get_item('') is None
	
    def test_get_item_invalid(self):
	self.d.load_layout('index')
	layout = self.d.get_layout()
	
	self.d.load_layout_items(layout)	
	assert self.d.get_item('invalid-item') is None
	
    def test_get_item_good(self):
	self.d.load_layout('index')
	layout = self.d.get_layout()
	
	self.d.load_layout_items(layout)	
	assert isinstance(self.d.get_item('share'), ControllerConfiguration)

class TestSwatMessages():
    
    def setUp(self):
	self.m = SwatMessages()

    def tearDown(self):
	pass
	
    def test_add(self):
	self.m.add('test message', 'cool')
	assert self.m.any() == True
	
    def test_clear(self):
	self.m.add('test message', 'cool')
	self.m.clean()
	assert self.m.any() == False
	
    def test_any(self):
	self.m.add('test message', 'cool')
	assert self.m.any() == True
	
	self.m.clean()
	assert self.m.any() == False
	
class TestBreadcrumbTrail():
    def setUp(self):
	self.c = ControllerConfiguration('share')
	self.c.setup()
	
	self.b = self.new_instance()

    def new_instance(self):
	return BreadcrumbTrail(self.c)
	
    def test_add(self):
	self.b = self.new_instance()
	self.b.add('bread', 'share', 'index')
	
	items = self.b.get()
	assert len(items) > 0
	
    def test_build(self):
	self.b = self.new_instance()
	self.b.build()
	
	items = self.b.get()
	
	assert len(items) > 0
		
	for i in items:
	    assert i.has_key('name') and i.has_key('link')

class TestControllerConfiguration():
    def setUp(self):
	self.c = 'share'
	self.a = 'index'
	self.conf = None

    def new_config_instance(self):
	return ControllerConfiguration(self.c, self.a)

    def test_configuration_setup(self):
	self.conf = self.new_config_instance()
	self.conf.setup()

    def test_setup_information(self):
	self.conf = self.new_config_instance()
	
	self.conf.setup_information(self.c, self.a)
	info = self.conf.get_information()
	
	assert len(info) > 0
	