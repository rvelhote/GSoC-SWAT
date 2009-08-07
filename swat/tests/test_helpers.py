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
from swat.tests import *
from pylons import config

from mako.template import Template, ModuleTemplate
from mako.lookup import TemplateLookup
from mako import exceptions

class TestMenuConfiguration(TestController):
    def setUp(self):
	""" open the menu configuration yamls """
	self.phony_instance = MenuConfiguration("topaaaaaaa", config['yaml.testfiles'])
	self.instance = MenuConfiguration("top", config['yaml.testfiles'])

    def test_get_phony_menu_items(self):
	""" checks if the phony menu item is empty as it should """
	items = self.phony_instance.get_items()
	assert len(items) == 0, 'Non-existing menu should return empty dictionary'
	
    def test_get_menu_items(self):
	""" check if there's anything at all in the valid menu yaml """
	items = self.instance.get_items()
	assert len(items) > 0, 'Existing menu should return at least one item'
    
    def test_check_for_control_item(self):
	""" checks if the control item is present in the test menu file """
	items = self.instance.get_items()
	assert 'dashboard' in items, 'test menu should have the dashboard item in it'
	
    def test_loop_through(self):
	""" test for the mandatory configuration parameters """
	items = self.instance.get_items()
	for item in items:
	    assert len(self.instance.get_item_configuration(item, 'link/controller')) > 0, 'must have controller defined'
	    assert len(self.instance.get_item_configuration(item, 'link/action')) > 0, 'must have action defined'
	    assert len(self.instance.get_item_configuration(item, 'link/name')) > 0, 'must have name defined'
    
    def test_menu_render(self):
	pass

class TestYamlConfig():
    def setUp(self):
	self.yaml = YamlConfig()
	self.yaml.y_load("yamlconfig", config['yaml.testfiles'])
	
    def test_depth(self):
	value = self.yaml.y_get("dashboard/link/name/title/controller/action/dashboard/link/name/title/controller/finally")
	assert value == 'yay', 'final result shoud be yay'
	
    def test_fake_value(self):
	value = self.yaml.y_get("these/pretzels/are/making/me/thirsty")
	assert len(value) == 0, 'empty result'
	
    def test_malformed_yaml(self):
	yaml_malformed = YamlConfig()
	yaml_malformed.y_load("yamlmalformed", config['yaml.testfiles'])
	
	assert len(yaml_malformed.yaml_contents) == 0, "should be empty"
	
    def test_fake_file(self):
	yaml_gone = YamlConfig()
	yaml_gone.y_load("yamlthatdoesntexist", config['yaml.testfiles'])
	
	assert len(yaml_gone.yaml_contents) == 0, "should be empty"
	

#
#class TestDashboardConfiguration():
#    def setUp(self):
#	self.d = DashboardConfiguration()
#
#    def tearDown(self):
#	pass
#
#    def test_load_config(self):
#	self.d.load_config('index')
#	assert len(self.d.get_layout()) > 0
#
#class TestSwatMessages():
#    def setUp(self):
#	self.m = SwatMessages()
#
#    def tearDown(self):
#	pass
#	
#    def test_add(self):
#	self.m.add('test message', 'cool')
#	assert self.m.any() == True
#	
#    def test_clear(self):
#	self.m.add('test message', 'cool')
#	self.m.clean()
#	assert self.m.any() == False
#	
#    def test_any(self):
#	self.m.add('test message', 'cool')
#	assert self.m.any() == True
#	
#	self.m.clean()
#	assert self.m.any() == False
#	
#class TestBreadcrumbTrail():
#    def setUp(self):
#	self.c = ControllerConfiguration('share')	
#	self.b = self.new_instance()
#
#    def new_instance(self):
#	return BreadcrumbTrail(self.c)
#	
#    def test_add(self):
#	self.b = self.new_instance()
#	self.b.add('bread', 'share', 'index')
#	
#	items = self.b.get()
#	assert len(items) > 0
#	
#    def test_build(self):
#	self.b = self.new_instance()
#	self.b.build()
#	
#	items = self.b.get()
#	
#	assert len(items) > 0
#		
#	for i in items:
#	    assert i.has_key('name') and i.has_key('link')
#
#class TestControllerConfiguration():
#    def setUp(self):
#	self.c = 'share'
#	self.a = 'index'
#	self.conf = None
#	