#
# Account Management Controller file for SWAT
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
import logging

import param

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from swat.lib.base import BaseController, render

from pylons.i18n.translation import _

from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, SwatMessages, ParamConfiguration, filter_list

from samba.dcerpc import samr, security, lsa
from samba import credentials

log = logging.getLogger(__name__)

class AccountController(BaseController):
    """ """
    def __init__(self):
        """ """
        me = request.environ['pylons.routes_dict']['controller']
        action = request.environ['pylons.routes_dict']['action']
        
        log.debug("Controller: " + me)
        log.debug("Action: " + action)
        
        c.config = ControllerConfiguration(me, action)
        
        c.breadcrumb = BreadcrumbTrail(c.config)
        c.breadcrumb.build()
            
        c.samba_lp = param.LoadParm()
        c.samba_lp.load_default()
        
        self.__manager = SAMPipeManager(c.samba_lp)
        
        domains = self.__manager.fetch_and_get_domain_names()
        self.__manager.set_current_domain(0)
        self.__manager.fetch_users_and_groups()
        
        # FIXME just so that options may work
        c.current_page = int(request.params.get("page", 1))
        c.per_page =  int(request.params.get("per_page", 10))
        c.filter_name = request.params.get("filter_value", "")
        
    def index(self):
        c.user_list = self.__manager.user_list
        c.group_list = self.__manager.group_list
        
        c.list_users = True
        c.list_groups = True
        
        return render('/default/derived/account.mako')
    
    def user(self):
        c.user_list = self.__manager.user_list
        
        c.list_users = True
        c.list_groups = False
        
        return render('/default/derived/account.mako')
    
    def group(self):
        c.group_list = self.__manager.group_list
        
        c.list_users = False
        c.list_groups = True
        
        return render('/default/derived/account.mako')
        
    def edit(self, id, type, is_new = False):
        if type == "user":
            c.p = ParamConfiguration('user-account-parameters')
            
            if not is_new:
                c.user = self.__manager.fetch_user(id)
            else:
                c.user = User("", "", "", -1)
                
            return render('/default/derived/edit-user-account.mako')
            
        elif type == "group":
            c.p = ParamConfiguration('group-parameters')
            
            if not is_new:
                c.group = self.__manager.fetch_group(id)
            else:
                c.group = Group("", "", -1)
                
            return render('/default/derived/edit-group.mako')
        else:
            message = _("You did not specify the type of account you want to edit")
            SwatMessages.add(message, "critical")
            redirect_to(controller='account', action='index')
            
    def edituser(self):
        id = int(request.params.get("id", -1))
        return self.edit(id, "user", False)
    
    def editgroup(self):
        id = int(request.params.get("id", -1))
        return self.edit(id, "group", False)
        
    def adduser(self):
        id = int(request.params.get("id", -1))
        return self.edit(id, "user", True)
    
    def addgroup(self):
        id = int(request.params.get("id", -1))
        return self.edit(id, "group", True)
        
    def save(self):
        action = request.environ['pylons.routes_dict']['action']
        
        task = request.params.get("task", "").strip().lower()
        type = request.params.get("type", "").strip().lower()
        
        is_new = False
        
        if task.startswith("add"):
            is_new = True
        
        if type == "group":
            id = int(request.params.get("id", -1))
            name = request.params.get("group_name", "")
            description = request.params.get("group_description", "")

            group = Group(name, description, id)
            
            if is_new:
                self.__manager.add_group(group)
            else:
                self.__manager.update_group(group)
            
            if action == "apply" or action == "save":
                message = _("saved id %s" % (str(id)))
                SwatMessages.add(message)
                redirect_to(controller='account', action='editgroup', id = id)
        
        return "Not Implemented"
    
    def apply(self):
        self.save()

    def cancel(self):
        redirect_to(controller='account', action='user')

    def remove(self):
        return "Not Implemented Yet"
        
class SAMPipeManager:
    """ Support Class obtained from Calin Crisan's 2009 Summer of Code project
    Extensions to GTK Frontends
    
    See: http://github.com/ccrisan/samba-gtk
    
    """
    def __init__(self, lp):
        self.user_list = []
        self.group_list = []
        
        #
        # FIXME Don't know how I will store this between refreshes. Maybe the
        # pipe/connect_handle should be stored in the session?
        #
        username = "administrator"
        password = "x"
        
        creds = credentials.Credentials()
        creds.set_username(username)
        creds.set_password(password)
        creds.set_domain("")

        if request.environ.has_key("REMOTE_HOST"):
            creds.set_workstation(request.environ.get("REMOTE_HOST"));
        else:
            creds.set_workstation("")

        self.pipe = samr.samr("ncalrpc:", credentials = creds)
        self.connect_handle = self.pipe.Connect2(None, security.SEC_FLAG_MAXIMUM_ALLOWED)
        
    def close(self):
        if (self.pipe != None):
            self.pipe.Close(self.connect_handle)
            
    def fetch_and_get_domain_names(self):
        if (self.pipe == None): # not connected
            return None
        
        domain_name_list = []
        
        self.sam_domains = self.toArray(self.pipe.EnumDomains(self.connect_handle, 0, -1))
        for (rid, domain_name) in self.sam_domains:
            domain_name_list.append(self.get_lsa_string(domain_name))
        
        return domain_name_list
    
    def set_current_domain(self, domain_index):
        self.domain = self.sam_domains[domain_index]
        
        self.domain_sid = self.pipe.LookupDomain(self.connect_handle, self.domain[1])
        self.domain_handle = self.pipe.OpenDomain(self.connect_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, self.domain_sid)
        
    def fetch_users_and_groups(self):
        del self.user_list[:]
        del self.group_list[:]
        
        # fetch groups
        self.sam_groups = self.toArray(self.pipe.EnumDomainGroups(self.domain_handle, 0, -1))
        
        for (rid, groupname) in self.sam_groups:
            group = self.fetch_group(rid)
            self.group_list.append(group)
            
        # fetch users
        self.sam_users = self.toArray(self.pipe.EnumDomainUsers(self.domain_handle, 0, 0, -1))
        
        for (rid, username) in self.sam_users:
            user = self.fetch_user(rid)
            self.user_list.append(user)

        
    def add_user(self, user):
        (user_handle, rid) = self.pipe.CreateUser(self.domain_handle, self.set_lsa_string(user.username), security.SEC_FLAG_MAXIMUM_ALLOWED)        
        user = self.fetch_user(rid, user)
        
        self.update_user(user)
        user = self.fetch_user(rid, user) # just to make sure we have the updated user properties

        self.user_list.append(user)

    def add_group(self, group):
        (group_handle, rid) = self.pipe.CreateDomainGroup(self.domain_handle, self.set_lsa_string(group.name), security.SEC_FLAG_MAXIMUM_ALLOWED)        
        group.rid = rid
        group = self.fetch_group(rid, group)
        
        self.update_group(group)
        group = self.fetch_group(rid, group) # just to make sure we have the updated group properties
        
        
        self.group_list.append(group)

    def update_user(self, user):
        user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, user.rid)

        info = self.pipe.QueryUserInfo(user_handle, samr.UserNameInformation)
        info.account_name = self.set_lsa_string(user.username)
        info.full_name = self.set_lsa_string(user.fullname)
        self.pipe.SetUserInfo(user_handle, samr.UserNameInformation, info)
        
        info = self.pipe.QueryUserInfo(user_handle, samr.UserAdminCommentInformation)
        info.description = self.set_lsa_string(user.description)
        self.pipe.SetUserInfo(user_handle, samr.UserAdminCommentInformation, info)
        
        info = self.pipe.QueryUserInfo(user_handle, samr.UserControlInformation)
        if (user.must_change_password):
            info.acct_flags |= 0x00020000
        else:
            info.acct_flags &= ~0x00020000

        if (user.password_never_expires):
            info.acct_flags |= 0x00000200
        else:
            info.acct_flags &= ~0x00000200
            
        if (user.account_disabled):
            info.acct_flags |= 0x00000001
        else:
            info.acct_flags &= ~0x00000001

        if (user.account_locked_out):
            info.acct_flags |= 0x00000400
        else:
            info.acct_flags &= ~0x00000400
        self.pipe.SetUserInfo(user_handle, samr.UserControlInformation, info)
            
        # TODO: cannot_change_password

        info = self.pipe.QueryUserInfo(user_handle, samr.UserProfileInformation)
        info.profile_path = self.set_lsa_string(user.profile_path)
        self.pipe.SetUserInfo(user_handle, samr.UserProfileInformation, info)
        
        info = self.pipe.QueryUserInfo(user_handle, samr.UserScriptInformation)
        info.logon_script = self.set_lsa_string(user.logon_script)
        self.pipe.SetUserInfo(user_handle, samr.UserScriptInformation, info)

        info = self.pipe.QueryUserInfo(user_handle, samr.UserHomeInformation)
        info.home_directory = self.set_lsa_string(user.homedir_path)
        
        
        if (user.map_homedir_drive == -1):
            info.home_drive = self.set_lsa_string("")
        else:
            info.home_drive = self.set_lsa_string(chr(user.map_homedir_drive + ord('A')) + ":")
        self.pipe.SetUserInfo(user_handle, samr.UserHomeInformation, info)
        
        
        # update user's groups
        group_list = self.rwa_list_to_group_list(self.pipe.GetGroupsForUser(user_handle).rids)
 
        # groups to remove
        for group in group_list:
            if (user.group_list.count(group) == 0):
                group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, group.rid)
                self.pipe.DeleteGroupMember(group_handle, user.rid)

        # groups to add
        for group in user.group_list:
            if (group_list.count(group) == 0):
                group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, group.rid)
                self.pipe.AddGroupMember(group_handle, user.rid, samr.SE_GROUP_ENABLED)

    def update_group(self, group):
        group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, group.rid)

        info = self.set_lsa_string(group.name)
        self.pipe.SetGroupInfo(group_handle, 2, info)
        
        info = self.set_lsa_string(group.description)
        self.pipe.SetGroupInfo(group_handle, 4, info)
        
    def delete_user(self, user):
        user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, user.rid)
        self.pipe.DeleteUser(user_handle)

    def delete_group(self, group):
        group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, group.rid)
        self.pipe.DeleteDomainGroup(group_handle)
    
    def fetch_user(self, rid, user = None):
        user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, rid)
        info = self.pipe.QueryUserInfo(user_handle, samr.UserAllInformation)
        user = self.query_info_to_user(info, user)
        group_rwa_list = self.pipe.GetGroupsForUser(user_handle).rids
        user.group_list = self.rwa_list_to_group_list(group_rwa_list)
        
        return user
    
    def fetch_group(self, rid, group = None):
        group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, rid)
        info = self.pipe.QueryGroupInfo(group_handle, 1)
        group = self.query_info_to_group(info, group)
        group.rid = rid
        
        return group
    
    def query_info_to_user(self, query_info, user = None):
        if (user == None):
            user = User(self.get_lsa_string(query_info.account_name), 
                        self.get_lsa_string(query_info.full_name), 
                        self.get_lsa_string(query_info.description), 
                        query_info.rid)
        else:
            user.username = self.get_lsa_string(query_info.account_name)
            user.full_name = self.get_lsa_string(query_info.full_name)
            user.description = self.get_lsa_string(query_info.description)
            user.rid = query_info.rid
        
        user.must_change_password = (query_info.acct_flags & 0x00020000) != 0
        user.password_never_expires = (query_info.acct_flags & 0x00000200) != 0
        user.account_disabled = (query_info.acct_flags & 0x00000001) != 0
        # TODO: account locked out does get updated!!!
        user.account_locked_out = (query_info.acct_flags & 0x00000400) != 0
        user.profile_path = self.get_lsa_string(query_info.profile_path)
        user.logon_script = self.get_lsa_string(query_info.logon_script)
        user.homedir_path = self.get_lsa_string(query_info.home_directory)
        
        drive = self.get_lsa_string(query_info.home_drive)
        if (len(drive) == 2):
            user.map_homedir_drive = ord(drive[0]) - ord('A')
        else:
            user.map_homedir_drive = -1
            
        return user
    
    def rwa_list_to_group_list(self, rwa_list):
        group_list = []
        
        for rwa in rwa_list:
            group_rid = rwa.rid
            group_to_add = None
            
            for group in self.group_list:
                if (group.rid == group_rid):
                    group_to_add = group
                    break
                
            if (group_to_add != None):
                group_list.append(group_to_add)
            else:
                raise Exception("group not found for rid = %d" % group_rid)
            
        return group_list

    def query_info_to_group(self, query_info, group = None):
        if (group == None):
            group = Group(self.get_lsa_string(query_info.name), 
                          self.get_lsa_string(query_info.description),  
                          0)
        else:
            group.name = self.get_lsa_string(query_info.name)
            group.description = self.get_lsa_string(query_info.description)
        
        return group

    @staticmethod
    def toArray((handle, array, num_entries)):
        ret = []
        for x in range(num_entries):
            ret.append((array.entries[x].idx, array.entries[x].name))
        return ret

    @staticmethod
    def get_lsa_string(str):
        return str.string
    
    @staticmethod
    def set_lsa_string(str):
        lsa_string = lsa.String()
        lsa_string.string = unicode(str)
        lsa_string.length = len(str)
        lsa_string.size = len(str)
        
        return lsa_string
    
class User:
    """ Support Class obtained from Calin Crisan's 2009 Summer of Code project
    Extensions to GTK Frontends
    
    See: http://github.com/ccrisan/samba-gtk
    
    """
    def __init__(self, username, fullname, description, rid):
        self.username = username
        self.fullname = fullname
        self.description = description
        self.rid = rid
        
        self.password = ""
        self.must_change_password = True
        self.cannot_change_password = False
        self.password_never_expires = False
        self.account_disabled = False
        self.account_locked_out = False
        self.group_list = []
        self.profile_path = ""
        self.logon_script = ""
        self.homedir_path = ""
        self.map_homedir_drive = -1
        
        None

    def list_view_representation(self):
        return [self.username, self.fullname, self.description, self.rid]

class Group:
    """ Support Class obtained from Calin Crisan's 2009 Summer of Code project
    Extensions to GTK Frontends
    
    See: http://github.com/ccrisan/samba-gtk
    
    """
    def __init__(self, name, description, rid):
        self.name = name
        self.description = description
        self.rid = rid
        
    def list_view_representation(self):
        return [self.name, self.description, self.rid]    
