#
# SAMR Manager file for SWAT
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
from pylons import session, request
from samba.dcerpc import samr, security, lsa
from samba import credentials, samdb, ldb
from samba.auth import system_session

import samba.ndr

class AccountManager(samdb.SamDB):
    __users = "CN=Users,"
    
    def __init__(self, lp):
        super(AccountManager, self).__init__(lp=lp, session_info=system_session())
        self.get_users()
        
    def __convert_to_user_object(self, user):
        rid = str(samba.ndr.ndr_unpack(security.dom_sid, str(user["objectSid"])))
        rid = int(rid[rid.rfind("-") + 1:])
        
        username = self.__get_key(user, "sAMAccountName")
        fullname = self.__get_key(user, "name")
        description = self.__get_key(user, "description")
        
        u = User(username, fullname, description, rid)
        
        u.must_change_password = True
        u.cannot_change_password = False
        u.password_never_expires = False
        u.account_disabled = False
        u.account_locked_out = False
        u.group_list = []
        u.profile_path = ""
        u.logon_script = ""
        u.homedir_path = ""
        u.map_homedir_drive = -1
        
    def __get_key(self, object, key):
        try:
            return str(object[key])
        except KeyError:
            return ""
        
    def __get_boolean(self, value):
        pass
        
    def get_users(self):
        users = self.search(base=self.__users + self.domain_dn(), scope=ldb.SCOPE_SUBTREE, expression="objectClass=user")
        user_list = []
        
        for user in users:
            user_list.append(self.__convert_to_user_object(user))
                
        return user_list
    
    def get_groups(self):
        pass
    #    groups = self.search(base=self.__users + self.domain_dn(), scope=ldb.SCOPE_SUBTREE, expression="objectClass=group")
    #    accounts = []
    #    
    #    for group in groups:
    #        account = SambaAccount()
    #
    #        for k, v in group.items():
    #            if k == "dn":
    #                continue
    #            
    #            account.add(k, v)
    #            
    #        accounts.append(account)
    #            
    #    return accounts

class SAMPipeManager:
    """ Support Class obtained from Calin Crisan's 2009 Summer of Code project
    Extensions to GTK Frontends
    
    See: http://github.com/ccrisan/samba-gtk
    
    """
    def __init__(self, lp):
        self.user_list = []
        self.group_list = []

        #
        # TODO Must find a better way!
        #
        creds = credentials.Credentials()
        creds.set_username(session["samr_u"])
        creds.set_password(session["samr_p"])
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
    
    def group_exists(self, id):
        """ Checks if a certain Group (identified by its ID) exists in the
        Database
        
        Keyword arguments:
        id -- The ID of the Group to check
        
        Returns:
        Boolean indicating if the Group exists or not
        
        TODO Handle Exception
        
        """
        exists = False
        
        try:
            self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, id)
            exists = True
        except RuntimeError:
            pass
        
        return exists
    
    def user_exists(self, id):
        """ Checks if a certain User (identified by its ID) exists in the
        Database
        
        Keyword arguments:
        id -- The ID of the User to check
        
        Returns:
        Boolean indicating if the User exists or not
        
        TODO Handle Exception
        
        """
        exists = False
        
        try:
            self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, id)
            exists = True
        except RuntimeError:
            pass
        
        return exists
    
    def get_users_in_group(self, gid):
        """ Gets all users in a certain group
        
        Keyword arguments:
        id -- The Group ID
        
        Returns:
        A list of Users that belong to the specified Group
        
        FIXME Will probably be very heavy if there are many users
        TODO Handle Exception
        
        """
        list = []
        for user in self.user_list:
            try:
                user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, user.rid)
                group_list = self.rwa_list_to_group_list(self.pipe.GetGroupsForUser(user_handle).rids)
                
                for group in group_list:
                    if gid == group.rid:
                        list.append(user)
                        break
                
            except RuntimeError:
                pass
            
        return list
    
    def filter_enabled_disabled(self, status):
        """ Filters the list of users by their Account Status (this means
        Enabled or Disabled)
        
        Keyword arguments:
        status -- Boolean indicating if we want only the Enabled Accounts (True)
        or Disabled Accounts (False)
        
        Returns:
        A list of Users with the specified status
        
        """
        list = []
        
        for user in self.user_list:
            if status == True and user.account_disabled == False:
                list.append(user)
            elif status == False and user.account_disabled == True:
                list.append(user)
                
        return list
    
    def toggle_user(self, id):
        """ Toggles a User Account's disabled status. If the account if disabled
        it will become enabled and vice-versa
        
        Keyword arguments:
        id -- The ID of the User to Toggle
        
        Returns:
        Boolean indicating if the operation was successful
        
        TODO Handle Exception
        
        """
        toggled = False
        new_status = True
        
        try:
            user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, id)
            info = self.pipe.QueryUserInfo(user_handle, samr.UserControlInformation)

            current_status = (info.acct_flags & 0x00000001) != 0
            
            ##
            ## Note: current_status == True means the account is currently
            ## disabled
            ##
            if (current_status == True):
                info.acct_flags &= ~0x00000001
            else:
                info.acct_flags |= 0x00000001
                
            new_status = not current_status
                
            self.pipe.SetUserInfo(user_handle, samr.UserControlInformation, info)
            toggled = True
        except RuntimeError:
            pass
    
        return (toggled, new_status)

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