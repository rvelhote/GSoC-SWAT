#
# Test Cases for the ShareBackendClassic Class
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

import param
import random

class MockShareParams(object):
    def create_backend_object(self, params=None):
        file = config["backend.testfiles"] + config["backend.classic.testfile"]
        
        samba_lp = param.LoadParm()
        samba_lp.load(file)
        
        if params is None:
            params = {}
            params["share_path"] = "/usr/local/path"
            params["share_hosts_allow"] = "a,b,c,d"
        
        return share.ShareBackendClassic(samba_lp, params)

class TestShareBackendClassic(TestController):
    def setUp(self):
        self.mock = MockShareParams()
        
    def tearDown(self):
        backend = self.mock.create_backend_object();
        list = backend.get_share_list();
        
        for l in list:
            backend.delete(l.get_share_name());
      
    def test_crud(self):
        self.test_backend = self.mock.create_backend_object();

        name = "TestShare"
        
        # Add a New Share With Name
        self.__add(name)
        self.__add_existing(name)
        
        # Edit Some Parameters
        self.__edit(name)
        
        # Copy The Share
        self.__copy(name)
        self.__many_copies(name)
        
        # Change the Share Name
        new_name = "TestShareRename"
        self.__rename(new_name, name)
        
        # Restore the Share Name
        self.__rename(name, new_name)
        
        # Test Existance
        self.__exists(name)
        self.__exists_ghost(new_name)
        
        # Test SambaShare
        self.__get_share(name)
        
        # Delete this Share
        self.__many_deletes()
        self.__delete(name)
        
    def __exists(self, name):
        self.assertEqual(self.test_backend.share_name_exists(name), True)
        
    def __exists_ghost(self, name):
        self.assertEqual(self.test_backend.share_name_exists(name), False)
        
    def __get_share(self, name):
        tmp_backend = self.mock.create_backend_object();
        share = tmp_backend.get_share_by_name(name)
        
        self.assertNotEqual(share, None)
        
        # Non Existing Attribute
        self.assertEqual(share.get("does-not-exist"), None)
        
        # Existing Attribute
        self.assertEqual(share.get_share_name(), name)
        
    def __add_existing(self, name):
        is_new = True
        self.assertEqual(self.test_backend.store(name, is_new), False)
        
    def __add(self, name):
        is_new = True
        
        self.assertEqual(self.test_backend.store(name, is_new), True)
        self.assertEqual(self.test_backend.share_name_exists(name), True)
        
        # Must have the Name attribute
        tmp_backend = self.mock.create_backend_object();
        share = tmp_backend.get_share_by_name(name)
        self.assertNotEqual(share, None)
        self.assertEqual(share.get_share_name(), name)
        
    def __edit(self, name):        
        params = {}
        params["share_path"] = "/usr/local/new-path"
        params["share_hosts_allow"] = "these, params, are, new"
        
        # Recreate the Backend Object with a new Parameters List
        tmp_backend = self.mock.create_backend_object(params);
        
        is_new = False
        
        self.assertEqual(tmp_backend.share_name_exists(name), True)
        self.assertEqual(tmp_backend.store(name, is_new), True)
        self.assertEqual(tmp_backend.share_name_exists(name), True)
        
        # Check if parameters were well inserted
        # @see fixme in ShareBackend.get_share_by_name()
        tmp_backend = self.mock.create_backend_object();
        share = tmp_backend.get_share_by_name(name)
        
        self.assertNotEqual(share, None)
        
        self.assertEqual(share.get_share_name(), name)
        self.assertEqual(share.get("path"), params["share_path"])
        
        share_hosts_allow_list = ['these', 'params', 'are', 'new']
        self.assertEqual(share.get("hosts allow"), share_hosts_allow_list)
        
    def __rename(self, name, old_name):
        is_new = False
        
        self.assertEqual(self.test_backend.share_name_exists(old_name), True)
        self.assertEqual(self.test_backend.store(name, is_new, old_name), True)
        self.assertEqual(self.test_backend.share_name_exists(name), True)
        
    def __copy(self, name):
        self.assertEqual(self.test_backend.copy(name), True)
        
    def __many_copies(self, name):
        for i in range(1, 5):
            self.__copy(name)
        
    def __delete(self, name):
        self.assertEqual(self.test_backend.share_name_exists(name), True)
        self.assertEqual(self.test_backend.delete(name), True)
        self.assertEqual(self.test_backend.share_name_exists(name), False)
        
    def __many_deletes(self):
        list = ['copy of copy of TestShare', 'copy of TestShare', \
                'copy of copy of copy of TestShare']
        for l in list:
            self.__delete(l)
 