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

class ExtSamDB(samdb.SamDB):
    """ Warning: Experimental Class
    
    FIXME throw exceptions or return None?
    TODO Better error checking and exception throwing/catching
    TODO Perhaps LDAP filters should be used like in the SamDB class
    
    """
    def __init__(self, lp):
        super(ExtSamDB, self).__init__(lp=lp, session_info=system_session())
    
    def get_object_with_dn(self, dn):
        """ Gets information from the SAM Database using the object's DN
        
        Keyword arguments:
        dn -- The DN of the Object
        
        Returns:
        LDB Elements with Object's information
        
        """
        obj = self.search(base=dn, scope=ldb.SCOPE_SUBTREE)
        if len(obj) > 0:
            return obj[0]
        return None

    def get_user_group_membership(self, username):
        """ Gets the groups that a user if a part of.
        
        Keyword arguments:
        username -- The username that we want to get the group membership from
        
        Returns:
        A list of LDB Elements with the Group's information
        
        """
        user_group_list = self.search(base=self.domain_dn(), \
                                      scope=ldb.SCOPE_SUBTREE, \
                                      expression="sAMAccountName=" + username, \
                                      attrs=["memberOf"])
        group_list = []
        
        if len(user_group_list) > 0:
            try:
                for g in user_group_list[0]["memberOf"]:
                    group_list.append(self.get_object_with_dn(g))
            except KeyError:
                pass
        
        return group_list
    
    def get_group_members(self, groupname):
        """ Gets the group members of a certain group.
        
        Keyword arguments:
        groupname -- The name of the group
        
        Returns:
        A list of members for the chosen group
        
        """
        members = self.search(base=self.domain_dn(), scope=ldb.SCOPE_SUBTREE, \
                              expression="sAMAccountName=" + groupname, \
                              attrs=["member"])
        member_list = []
        
        if len(members) > 0:
            try:
                for m in members[0]["member"]:
                    member_list.append(self.get_object_with_dn(m))
            except KeyError:
                pass
            
        return member_list
        
    def get_users(self):
        """ Gets and returns a list of Users from SamDB with all of the
        available information on each of the existing users.
        
        Returns:
        A list of LDB elements with their complete information
        
        """
        return self.search(base="CN=Users," + self.domain_dn(), \
                           scope=ldb.SCOPE_SUBTREE, \
                           expression="objectClass=user")

    def user_exists(self, username):
        """ Checks if a certain User exists on the SAM Database.
        
        Keyword arguments:
        username -- The username to check
        
        Returns:
        Boolean indicating if the User exists or not
        
        """
        user = self.search(base=self.domain_dn(), \
                           scope=ldb.SCOPE_SUBTREE, \
                           expression="(sAMAccountName=" + username + ")(objectClass=user)")
        if len(user) > 0:
            return True
        return False
                
    def get_user(self, username):
        """ Gets a single User and all of its information from the SAM Database.
        
        Keyword arguments:
        username -- The username to fetch
        
        Returns:
        LDB Elements with the user information or none if the user doesn't exist
        
        """
        user = self.search(base=self.domain_dn(), scope=ldb.SCOPE_SUBTREE, \
                           expression="(sAMAccountName=" + username + ")(objectClass=user)")
        if len(user) > 0:
            return user[0]
        return None

    def add_user(self, group):
        l = self.get_groups_for_user(group.username)
        for x in l:
            self.get_group(x)
        
        
        raise Exception

    def delete_user(self, user):
        user_ldb = self.search(base=self.domain_dn(), scope=ldb.SCOPE_SUBTREE, \
                               expression="(sAMAccountName=" + user.username + ")(objectClass=user)")[0]
        self.delete(user_ldb.dn)
        
    def add_group(self, groupname, description):
        """ """
        dn = "CN=%s,CN=Users,%s" % (groupname, self.domain_dn())
        self.add({"dn": str(dn), \
                  "sAMAccountName": groupname, \
                  "description": description, \
                  "objectClass": "group"})
    
    def is_member_of_group(self, username, groupname):
        """ Checks if a user is a member of a certain group
        
        Keyword arguments:
        username -- The username of the user we want to check
        groupname -- The name of the group that we want to check
        
        Returns:
        Boolean indicating if the user belongs to the group or not
        
        """
        is_member = False
        user = self.get_user(username)
        group = self.get_group(groupname)
        
        if user is None or group is None:
            return False
        
        groups = user["memberOf"]
        for g in groups:
            if group.dn == g:
                is_member = True
                break
            
        return is_member

    def delete_user_group_membership(self, username, groupname):
        """ Deletes a user's membership from a certain group
        
        Keyword arguments:
        username -- The Username of the user that we want to remove the group from
        groupname -- The name of the group that we want to remove
        
        Returns:
        Boolean indicating if the operation was sucessful or not
        
        """
        deleted = False
        user = self.get_user(username)
        group = self.get_group(groupname)
        
        if user is None or group is None or not self.is_member_of_group(username, groupname):
            return False
        
        try:
            new_list = []
            groups = user["memberOf"]
            
            for g in groups:
                if g != dn:
                    new_list.append(g)
                    
            msg = ldb.Message(ldb.Dn(self, group.dn))
            msg["memberOf"] = ldb.MessageElement(new_list, ldb.FLAG_MOD_REPLACE, "memberOf")
            
            self.modify(msg)
            deleted = True
        except ldb.LdbError, error_message:
            pass
        
        return deleted
    
    def add_user_group_membership(self, username, group):
        pass
        
    def delete_group(self, groupname):
        """ Deletes a Group from the SAM Database and group references in each
        of its user members.
        
        Keyword arguments:
        groupname -- The name of the group we want to delete

        """
        dn = "CN=%s,CN=Users,%s" % (groupname, self.domain_dn())
        self.delete(str(dn))
        
        members = self.get_group_members(groupname)
        for m in members:
            self.delete_user_group_membership(self.__get_key(m, "sAMAccountName"), groupname)

    def update_group(self, name, description):
        """ Updates the Group's information on the Database
        
        FIXME: The name of the group is not changeable
        
        Keyword arguments:
        name -- The name of the group
        description -- The group's description

        """
        dn = "CN=%s,CN=Users,%s" % (name, self.domain_dn())
        
        if len(description) > 0:
            changeset = """dn: %s\nchangetype:replace\nreplace:description\ndescription: %s""" % (dn, description)
        else:
            changeset = """dn: %s\nchangetype:replace\nreplace:description\n-""" % (dn)
            
        self.modify_ldif(changeset)
        
    def group_exists(self, groupname):
        """ Checks if a group exists in the SAM Database
        
        Keyword arguments:
        groupname -- The name of the group we are searching for
        
        Returns:
        Boolean indicating if the group exists or not
        
        """
        group = self.search(base=self.domain_dn(), scope=ldb.SCOPE_SUBTREE, \
                            expression="(sAMAccountName=" + groupname + ")(objectClass=group)")
        if len(group) > 0:
            return True
        return False

    def get_group(self, groupname):
        """ Gets a single Group from the SAM Database.
        
        Keyword arguments:
        groupname -- The name of the group we want to get
        
        Returns:
        An LDB element with the Group's information. If the group doesn't exist
        it will return None
        
        """
        group = self.search(base=self.domain_dn(), scope=ldb.SCOPE_SUBTREE, \
                            expression="(sAMAccountName=" + groupname + ")(objectClass=group)")
        if len(group) > 0:
            return group[0]
        return None
        
    def get_groups(self):
        """ Gets and returns a list of Groups from SamDB with all of the
        available information on each of the existing groups.
        
        Returns:
        A list of LDB elements with their complete information
        
        """
        return self.search(base="CN=Users," + self.domain_dn(), \
                           scope=ldb.SCOPE_SUBTREE, \
                           expression="objectClass=group")
        
    def disable_account(self, username):
        user = self.get_user(username)
        
        uac = int(self.__get_key(user, "userAccountControl"))
        uac |= 0x00000002
        
        mod = """dn: %s\nchangetype: modify\nreplace: userAccountControl\nuserAccountControl: %u""" % (user.dn, uac)
        self.modify_ldif(mod)

    def __get_key(self, object, key):
        """ """
        try:
            return str(object[key])
        except KeyError:
            return ""

class AccountManager(object):
    """ Warning: Highly Experimental Class """
    def __init__(self, lp):
        """ """
        self.samr = ExtSamDB(lp)
    
    def __convert_to_user_object(self, user):
        """ """
        rid = str(samba.ndr.ndr_unpack(security.dom_sid, str(user["objectSid"])))
        rid = int(rid[rid.rfind("-") + 1:])
        
        username = self.__get_key(user, "sAMAccountName")
        fullname = self.__get_key(user, "name")
        description = self.__get_key(user, "description")
        
        u = User(username, fullname, description, rid)
        
        uac = int(self.__get_key(user, "userAccountControl"))

        u.must_change_password = (uac & 0x00800000) != 0
        u.cannot_change_password = (uac & 0x00000040) != 0
        u.password_never_expires = (uac & 0x00010000) != 0
        u.account_disabled = (uac & 0x00000002) != 0
        u.account_locked_out = (uac & 0x00000010) != 0
        
        u.group_list = self.get_user_group_membership(username)
        u.profile_path = self.__get_key(user, "profilePath")
        u.logon_script = self.__get_key(user, "scriptPath")
        u.homedir_path = self.__get_key(user, "homeDirectory")
        u.map_homedir_drive = -1
        
        print u.account_disabled
        
        return u

    def __convert_to_group_object(self, group):
        """ """
        rid = str(samba.ndr.ndr_unpack(security.dom_sid, str(group["objectSid"])))
        rid = int(rid[rid.rfind("-") + 1:])
        
        name = self.__get_key(group, "sAMAccountName")
        description = self.__get_key(group, "description")

        return Group(name, description, rid)

    def __get_key(self, object, key):
        """ """
        try:
            return str(object[key])
        except KeyError:
            return ""
        
    def get_group(self, groupname):
        """ """
        return self.__convert_to_group_object(self.samr.get_group(groupname))
        
    def get_user(self, username):
        """ """
        return self.__convert_to_user_object(self.samr.get_user(username))
    
    def get_groups(self):
        """ Gets the group list from SamDB, converts them to the a Group Object
        and returns the list
        
        Returns:
        A list of the Groups that exist in the SAM database
        
        """
        groups = self.samr.get_groups();
        group_list = []
        
        for group in groups:
            group_list.append(self.__convert_to_group_object(group))
                
        return group_list
    
    def get_users(self):
        """ Gets the user list from SamDB, converts them to the a User Object
        and returns the list
        
        Returns:
        A list of the Users that exist in the SAM database
        
        """
        users = self.samr.get_users();
        user_list = []
        
        for user in users:
            user_list.append(self.__convert_to_user_object(user))
                
        return user_list
    
    def get_group_members(self, groupname):
        """ """
        members = self.samr.get_group_members(groupname)
        user_list = []
        
        for m in members:
            user_list.append(self.__convert_to_user_object(m))
        
        return user_list
    
    def get_user_group_membership(self, username):
        """ """
        membership_group_list = self.samr.get_user_group_membership(username)
        group_list = []
        
        for m in membership_group_list:
            ##
            ## FIXME temporary
            ##
            o = self.__convert_to_group_object(m)
            group_list.append(o.name)
        
        return group_list
    
    def update_group(self, group):
        """ """
        self.samr.update_group(group.name, group.description)
    
    def add_group(self, group):
        """ """
        self.samr.add_group(group.name, group.description)
        
    def delete_group(self, group):
        """ """
        self.samr.delete_group(group.name)
        
    def toggle_user(self, username):
        """ Toggles a User Account's disabled status. If the account if disabled
        it will become enabled and vice-versa
        
        Keyword arguments:
        username -- The username of the user to toggle
        
        Returns:
        Boolean indicating if the operation was successful
        
        """
        user = self.__convert_to_user_object(self.samr.get_user(username))
        if user.account_disabled:
            self.samr.enable_account("sAMAccountName=%s" % (username))
        else:
            self.samr.disable_account(username)
            
        return (True, not user.account_disabled)

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
        
#class SAMPipeManager:
#    """ Support Class obtained from Calin Crisan's 2009 Summer of Code project
#    Extensions to GTK Frontends
#    
#    See: http://github.com/ccrisan/samba-gtk
#    
#    """
#    def __init__(self, lp):
#        self.user_list = []
#        self.group_list = []
#
#        #
#        # TODO Must find a better way!
#        #
#        creds = credentials.Credentials()
#        creds.set_username(session["samr_u"])
#        creds.set_password(session["samr_p"])
#        creds.set_domain("")
#
#        if request.environ.has_key("REMOTE_HOST"):
#            creds.set_workstation(request.environ.get("REMOTE_HOST"));
#        else:
#            creds.set_workstation("")
#
#        self.pipe = samr.samr("ncalrpc:", credentials = creds)
#        self.connect_handle = self.pipe.Connect2(None, security.SEC_FLAG_MAXIMUM_ALLOWED)
#        
#    def close(self):
#        if (self.pipe != None):
#            self.pipe.Close(self.connect_handle)
#            
#    def fetch_and_get_domain_names(self):
#        if (self.pipe == None): # not connected
#            return None
#        
#        domain_name_list = []
#        
#        self.sam_domains = self.toArray(self.pipe.EnumDomains(self.connect_handle, 0, -1))
#        for (rid, domain_name) in self.sam_domains:
#            domain_name_list.append(self.get_lsa_string(domain_name))
#        
#        return domain_name_list
#    
#    def set_current_domain(self, domain_index):
#        self.domain = self.sam_domains[domain_index]
#        
#        self.domain_sid = self.pipe.LookupDomain(self.connect_handle, self.domain[1])
#        self.domain_handle = self.pipe.OpenDomain(self.connect_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, self.domain_sid)
#        
#    def fetch_users_and_groups(self):
#        del self.user_list[:]
#        del self.group_list[:]
#        
#        # fetch groups
#        self.sam_groups = self.toArray(self.pipe.EnumDomainGroups(self.domain_handle, 0, -1))
#        
#        for (rid, groupname) in self.sam_groups:
#            group = self.fetch_group(rid)
#            self.group_list.append(group)
#            
#        # fetch users
#        self.sam_users = self.toArray(self.pipe.EnumDomainUsers(self.domain_handle, 0, 0, -1))
#        
#        for (rid, username) in self.sam_users:
#            user = self.fetch_user(rid)
#            self.user_list.append(user)
#
#        
#    def add_user(self, user):
#        (user_handle, rid) = self.pipe.CreateUser(self.domain_handle, self.set_lsa_string(user.username), security.SEC_FLAG_MAXIMUM_ALLOWED)        
#        user = self.fetch_user(rid, user)
#        
#        self.update_user(user)
#        user = self.fetch_user(rid, user) # just to make sure we have the updated user properties
#
#        self.user_list.append(user)
#
#    def add_group(self, group):
#        (group_handle, rid) = self.pipe.CreateDomainGroup(self.domain_handle, self.set_lsa_string(group.name), security.SEC_FLAG_MAXIMUM_ALLOWED)        
#        group.rid = rid
#
#        self.update_group(group)
#        group = self.fetch_group(rid, group) # just to make sure we have the updated group properties
#                
#        self.group_list.append(group)
#
#    def update_user(self, user):
#        user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, user.rid)
#
#        info = self.pipe.QueryUserInfo(user_handle, samr.UserNameInformation)
#        info.account_name = self.set_lsa_string(user.username)
#        info.full_name = self.set_lsa_string(user.fullname)
#        self.pipe.SetUserInfo(user_handle, samr.UserNameInformation, info)
#        
#        info = self.pipe.QueryUserInfo(user_handle, samr.UserAdminCommentInformation)
#        info.description = self.set_lsa_string(user.description)
#        self.pipe.SetUserInfo(user_handle, samr.UserAdminCommentInformation, info)
#        
#        info = self.pipe.QueryUserInfo(user_handle, samr.UserControlInformation)
#        if (user.must_change_password):
#            info.acct_flags |= 0x00020000
#        else:
#            info.acct_flags &= ~0x00020000
#
#        if (user.password_never_expires):
#            info.acct_flags |= 0x00000200
#        else:
#            info.acct_flags &= ~0x00000200
#            
#        if (user.account_disabled):
#            info.acct_flags |= 0x00000001
#        else:
#            info.acct_flags &= ~0x00000001
#
#        if (user.account_locked_out):
#            info.acct_flags |= 0x00000400
#        else:
#            info.acct_flags &= ~0x00000400
#        self.pipe.SetUserInfo(user_handle, samr.UserControlInformation, info)
#            
#        # TODO: cannot_change_password
#
#        info = self.pipe.QueryUserInfo(user_handle, samr.UserProfileInformation)
#        info.profile_path = self.set_lsa_string(user.profile_path)
#        self.pipe.SetUserInfo(user_handle, samr.UserProfileInformation, info)
#        
#        info = self.pipe.QueryUserInfo(user_handle, samr.UserScriptInformation)
#        info.logon_script = self.set_lsa_string(user.logon_script)
#        self.pipe.SetUserInfo(user_handle, samr.UserScriptInformation, info)
#
#        info = self.pipe.QueryUserInfo(user_handle, samr.UserHomeInformation)
#        info.home_directory = self.set_lsa_string(user.homedir_path)
#        
#        
#        if (user.map_homedir_drive == -1):
#            info.home_drive = self.set_lsa_string("")
#        else:
#            info.home_drive = self.set_lsa_string(chr(user.map_homedir_drive + ord('A')) + ":")
#        self.pipe.SetUserInfo(user_handle, samr.UserHomeInformation, info)
#
#        # update user's groups
#        group_list = self.rwa_list_to_group_list(self.pipe.GetGroupsForUser(user_handle).rids)
# 
#        # groups to remove
#        for group in group_list:
#            if (user.group_list.count(group) == 0):
#                group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, group.rid)
#                self.pipe.DeleteGroupMember(group_handle, user.rid)
#
#        # groups to add
#        for group in user.group_list:
#            if (group_list.count(group) == 0):
#                group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, group.rid)
#                self.pipe.AddGroupMember(group_handle, user.rid, samr.SE_GROUP_ENABLED)
#
#    def update_group(self, group):
#        group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, group.rid)
#
#        info = self.set_lsa_string(group.name)
#        self.pipe.SetGroupInfo(group_handle, 2, info)
#        
#        info = self.set_lsa_string(group.description)
#        self.pipe.SetGroupInfo(group_handle, 4, info)
#        
#    def delete_user(self, user):
#        user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, user.rid)
#        self.pipe.DeleteUser(user_handle)
#
#    def delete_group(self, group):
#        group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, group.rid)
#        self.pipe.DeleteDomainGroup(group_handle)
#    
#    def fetch_user(self, rid, user = None):
#        user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, rid)
#        info = self.pipe.QueryUserInfo(user_handle, samr.UserAllInformation)
#        user = self.query_info_to_user(info, user)
#        group_rwa_list = self.pipe.GetGroupsForUser(user_handle).rids
#        user.group_list = self.rwa_list_to_group_list(group_rwa_list)
#        
#        return user
#    
#    def fetch_group(self, rid, group = None):
#        group_handle = self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, rid)
#        info = self.pipe.QueryGroupInfo(group_handle, 1)
#        group = self.query_info_to_group(info, group)
#        group.rid = rid
#        
#        return group
#    
#    def query_info_to_user(self, query_info, user = None):
#        if (user == None):
#            user = User(self.get_lsa_string(query_info.account_name), 
#                        self.get_lsa_string(query_info.full_name), 
#                        self.get_lsa_string(query_info.description), 
#                        query_info.rid)
#        else:
#            user.username = self.get_lsa_string(query_info.account_name)
#            user.full_name = self.get_lsa_string(query_info.full_name)
#            user.description = self.get_lsa_string(query_info.description)
#            user.rid = query_info.rid
#
#        user.must_change_password = (query_info.acct_flags & 0x00020000) != 0
#        user.password_never_expires = (query_info.acct_flags & 0x00000200) != 0
#        user.account_disabled = (query_info.acct_flags & 0x00000001) != 0
#        # TODO: account locked out does get updated!!!
#        user.account_locked_out = (query_info.acct_flags & 0x00000400) != 0
#        user.profile_path = self.get_lsa_string(query_info.profile_path)
#        user.logon_script = self.get_lsa_string(query_info.logon_script)
#        user.homedir_path = self.get_lsa_string(query_info.home_directory)
#        
#        drive = self.get_lsa_string(query_info.home_drive)
#        if (len(drive) == 2):
#            user.map_homedir_drive = ord(drive[0]) - ord('A')
#        else:
#            user.map_homedir_drive = -1
#            
#        return user
#    
#    def rwa_list_to_group_list(self, rwa_list):
#        group_list = []
#        
#        for rwa in rwa_list:
#            group_rid = rwa.rid
#            group_to_add = None
#            
#            for group in self.group_list:
#                if (group.rid == group_rid):
#                    group_to_add = group
#                    break
#                
#            if (group_to_add != None):
#                group_list.append(group_to_add)
#            else:
#                raise Exception("group not found for rid = %d" % group_rid)
#            
#        return group_list
#
#    def query_info_to_group(self, query_info, group = None):
#        if (group == None):
#            group = Group(self.get_lsa_string(query_info.name), 
#                          self.get_lsa_string(query_info.description),  
#                          0)
#        else:
#            group.name = self.get_lsa_string(query_info.name)
#            group.description = self.get_lsa_string(query_info.description)
#        
#        return group
#    
#    def group_exists(self, id):
#        """ Checks if a certain Group (identified by its ID) exists in the
#        Database
#        
#        Keyword arguments:
#        id -- The ID of the Group to check
#        
#        Returns:
#        Boolean indicating if the Group exists or not
#        
#        TODO Handle Exception
#        
#        """
#        exists = False
#        
#        try:
#            self.pipe.OpenGroup(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, id)
#            exists = True
#        except RuntimeError:
#            pass
#        
#        return exists
#    
#    def user_exists(self, id):
#        """ Checks if a certain User (identified by its ID) exists in the
#        Database
#        
#        Keyword arguments:
#        id -- The ID of the User to check
#        
#        Returns:
#        Boolean indicating if the User exists or not
#        
#        TODO Handle Exception
#        
#        """
#        exists = False
#        
#        try:
#            self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, id)
#            exists = True
#        except RuntimeError:
#            pass
#        
#        return exists
#    
#    def get_users_in_group(self, gid):
#        """ Gets all users in a certain group
#        
#        Keyword arguments:
#        id -- The Group ID
#        
#        Returns:
#        A list of Users that belong to the specified Group
#        
#        FIXME Will probably be very heavy if there are many users
#        TODO Handle Exception
#        
#        """
#        list = []
#        for user in self.user_list:
#            try:
#                user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, user.rid)
#                group_list = self.rwa_list_to_group_list(self.pipe.GetGroupsForUser(user_handle).rids)
#                
#                for group in group_list:
#                    if gid == group.rid:
#                        list.append(user)
#                        break
#                
#            except RuntimeError:
#                pass
#            
#        return list
#    
#    def filter_enabled_disabled(self, status):
#        """ Filters the list of users by their Account Status (this means
#        Enabled or Disabled)
#        
#        Keyword arguments:
#        status -- Boolean indicating if we want only the Enabled Accounts (True)
#        or Disabled Accounts (False)
#        
#        Returns:
#        A list of Users with the specified status
#        
#        """
#        list = []
#        
#        for user in self.user_list:
#            if status == True and user.account_disabled == False:
#                list.append(user)
#            elif status == False and user.account_disabled == True:
#                list.append(user)
#                
#        return list
#    
#    def toggle_user(self, id):
#        """ Toggles a User Account's disabled status. If the account if disabled
#        it will become enabled and vice-versa
#        
#        Keyword arguments:
#        id -- The ID of the User to Toggle
#        
#        Returns:
#        Boolean indicating if the operation was successful
#        
#        TODO Handle Exception
#        
#        """
#        toggled = False
#        new_status = True
#        
#        try:
#            user_handle = self.pipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, id)
#            info = self.pipe.QueryUserInfo(user_handle, samr.UserControlInformation)
#
#            current_status = (info.acct_flags & 0x00000001) != 0
#            
#            ##
#            ## Note: current_status == True means the account is currently
#            ## disabled
#            ##
#            if (current_status == True):
#                info.acct_flags &= ~0x00000001
#            else:
#                info.acct_flags |= 0x00000001
#                
#            new_status = not current_status
#                
#            self.pipe.SetUserInfo(user_handle, samr.UserControlInformation, info)
#            toggled = True
#        except RuntimeError:
#            pass
#    
#        return (toggled, new_status)
#
#    @staticmethod
#    def toArray((handle, array, num_entries)):
#        ret = []
#        for x in range(num_entries):
#            ret.append((array.entries[x].idx, array.entries[x].name))
#        return ret
#
#    @staticmethod
#    def get_lsa_string(str):
#        return str.string
#    
#    @staticmethod
#    def set_lsa_string(str):
#        lsa_string = lsa.String()
#        lsa_string.string = unicode(str)
#        lsa_string.length = len(str)
#        lsa_string.size = len(str)
#        
#        return lsa_string
