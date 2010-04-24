#
# Test Cases for ShareBackendLdb Class
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

from swat.tests import *
from pylons import config
from swat.controllers import share

import param, ldb
import random

class MockShareParams(object):
    def create_backend_object(self, params=None, file=None):
        samba_lp = param.LoadParm()
        samba_lp.load_default()
        
        if file is None:
            file = config["backend.testfiles"] + config["backend.ldb.testfile"]
        
        if params is None:
            params = {}
            params["share_path"] = "/usr/local/" + str(random.random())
            params["share_hosts_allow"] = "a,b,c,d"
        
        return share.ShareBackendLdb(samba_lp, params, file)

class TestShareBackendLdb(TestController):
    def setUp(self):
        self.mock = MockShareParams()
        
    def tearDown(self):
        pass
        
    def test_add_new(self):
        backend = self.mock.create_backend_object();
        
        name = "TestShare"
        is_new = True
        
        assert backend.store(name, is_new) == True, backend.get_error_message()
        assert backend.share_name_exists(name) == True, backend.get_error_message()
        
    def test_share_exists(self):
        backend = self.mock.create_backend_object();
        
        name = "ThisShareDoesNotExist" + str(random.random())
        assert backend.share_name_exists(name) == False
        
        name = "TestShare"
        assert backend.share_name_exists(name) == True
        
    def test_rename_share(self):
        backend = self.mock.create_backend_object();
        
        name = "TestShareNewName"
        is_new = False
        old_name = "TestShare"
        
        assert backend.store(name, is_new, old_name) == True
        assert backend.share_name_exists(old_name) == False
        assert backend.share_name_exists(name) == True
        
        share = backend.get_share_by_name(name)
        
    def test_edit_share(self):
        params = {}
        params["share_path"] = "/usr/local/" + str(random.random())
        params["share_hosts_allow"] = "these, params, are, new"
        
        name = "TestShare"
        is_new = False
        
        backend = self.mock.create_backend_object(params);
        assert backend.store(name, is_new) == True, backend.get_error_message()
        assert backend.share_name_exists(name) == True
        
        # @see fixme in ShareBackend.get_share_by_name()
        backend = self.mock.create_backend_object();
        share = backend.get_share_by_name(name)
        
        assert share.get("name") == name
        assert share.get("hosts allow") == params["share_hosts_allow"]
        assert share.get("path") == params["share_path"]
        
    def test_share_attributes_add(self):
        params = {}
        
        new_param_key = "share_param_" + str(random.random())
        new_param_value = "random - " + str(random.random())
        
        params[new_param_key] = new_param_value
        
        name = "TestShare"
        is_new = False
        
        backend = self.mock.create_backend_object(params);
        assert backend.store(name, is_new) == True
        assert backend.share_name_exists(name) == True
        
        backend = self.mock.create_backend_object();
        share = backend.get_share_by_name(name)
        
        assert share.get(new_param_key) == new_param_value
    
    def test_share_attributes_modify(self):
        params = {}
        
        new_param_value = "random - " + str(random.random())
        params["share_path"] = new_param_value
        
        name = "TestShare"
        is_new = False
        
        backend = self.mock.create_backend_object(params);
        assert backend.store(name, is_new) == True
        assert backend.share_name_exists(name) == True
        
        backend = self.mock.create_backend_object();
        share = backend.get_share_by_name(name)
        
        assert share.get("path") == new_param_value

    def test_remove_ghost(self):
        name = "TestShareRandom" + str(random.random()) + "EvenMoreRandom"
        
        backend = self.mock.create_backend_object();
        
        assert backend.delete(name) == False
        assert backend.share_name_exists(name) == False
        
    def test_ghost_ldb(self):
        pass
    
    def test_copy(self):
        name = "TestShare"
        backend = self.mock.create_backend_object();
        
        # @see fixme in ShareBackendLdb.copy()
        assert backend.copy(name) == True
    
    def test_remove(self):
        name = "TestShare" + str(random.random()) + "EvenMoreRandomThanLastTime"
        is_new = True
        
        backend = self.mock.create_backend_object();
        
        assert backend.store(name, is_new) == True
        assert backend.share_name_exists(name) == True
        
        assert backend.delete(name) == True
        assert backend.share_name_exists(name) == False
        
    def test_crud(self):
        pass
        