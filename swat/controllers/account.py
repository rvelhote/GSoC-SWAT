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

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from swat.lib.base import BaseController, render
from swat.lib.samr_manager import SAMPipeManager, User, Group

from pylons.i18n.translation import _

from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, SwatMessages, ParamConfiguration, filter_list

from pylons.templating import render_mako_def

from samba import param

log = logging.getLogger(__name__)

class AccountController(BaseController):
    """ Account Management Controller.
    
    TODO Too many *group/user actions. I think this should be improved. No idea
    how yet :)
    
    """
    def __init__(self):
        """ """
        me = request.environ['pylons.routes_dict']['controller']
        action = request.environ['pylons.routes_dict']['action']
        
        log.debug("Controller: " + me)
        log.debug("Action: " + action)
        
        if(request.environ['pylons.routes_dict'].has_key("subaction")):
            action = request.environ['pylons.routes_dict']['subaction'] + action
        
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
    
    def user(self, subaction="index", id=-1):
        id = int(id)        
        user_manager = UserManager(self.__manager)

        is_new = False
        
        if id == -1:
            is_new = True
                
        ##
        ## Edit a User
        ##
        if subaction == "edit" or subaction == "add":
            c.p = ParamConfiguration('user-account-parameters')
            c.user = user_manager.edit(id, is_new)

            if c.user is not None:
                template = "/default/derived/edit-user-account.mako"
            else:
                message = _("Unable to get User to edit")
                type = "critical"
                SwatMessages.add(message, type)
        ##
        ## Save the changes made to a User
        ##
        elif subaction == "save" or subaction == "apply":
            saved = user_manager.save(id, is_new)
            
            if saved:
                type = "cool"
                message = _("Sucessfuly saved the User with the ID %s" % (id))
            else:
                type = "critical"
                cause = _("Unkown Reason")
                
                if user_manager.has_message():
                    cause = user_manager.get_message()
                
                message = _("Error saving the User with the ID %s: %s" % (id, cause))
                
            SwatMessages.add(message, type)
            
            if subaction == "save":
                redirect_to(controller='account', action='user')
            elif subaction == "apply":
                redirect_to("account_action", action='user', subaction='edit', id=id)
            
        ## 
        ## Remove a Certain User
        ## 
        elif subaction == "remove":
            removed = user_manager.remove(id)
            
            if removed:
                type = "cool"
                message = _("Sucessfuly deleted the User with the ID %s" % (id))
            else:
                type = "critical"
                cause = _("Unkown Reason")
                
                if user_manager.has_message():
                    cause = user_manager.get_message()
                
                message = _("Error deleting the User with the ID %s  " % (id, cause))
                
            SwatMessages.add(message, type)
            redirect_to(controller='account', action='user')
            
        ##
        ## 
        ##
        else:
            c.user_list = self.__manager.user_list        
            c.list_users = True
            c.list_groups = False
            template = "/default/derived/account.mako"

        return render(template)
    
    def group(self, subaction="index", id=-1):
        id = int(id)        
        group_manager = GroupManager(self.__manager)

        is_new = False
        
        if id == -1:
            is_new = True
            
        ##
        ## Edit a Group
        ##
        if subaction == "edit" or subaction == "add":
            c.p = ParamConfiguration('group-parameters')
            c.group = group_manager.edit(id, is_new)

            if c.group is not None:
                template = "/default/derived/edit-group.mako"
            else:
                type = "critical"
                cause = _("Unkown Reason")
                
                if user_manager.has_message():
                    cause = user_manager.get_message()
                    
                message = _("Unable to get Group to edit - %s", (cause))
                SwatMessages.add(message, type)

        ##
        ## Save the changes made to a Group
        ##
        elif subaction == "save" or subaction == "apply":
            saved = group_manager.save(id, is_new)
            
            if saved:
                type = "cool"
                message = _("Sucessfuly saved the Group with the ID %s" % (id))
            else:
                type = "critical"
                cause = _("Unkown Reason")
                
                if group_manager.has_message():
                    cause = group_manager.get_message()
                
                message = _("Error saving the Group with the ID %s: %s" % (id, cause))
                
            SwatMessages.add(message, type)
            
            if subaction == "save":
                redirect_to(controller='account', action='group')
            elif subaction == "apply":
                redirect_to("account_action", action='group', subaction='edit', id=id)
            
        ## 
        ## Remove a Certain Group
        ## 
        elif subaction == "remove":
            removed = group_manager.remove(id)
            
            if removed:
                type = "cool"
                message = _("Sucessfuly deleted the Group with the ID %s" % (id))
            else:
                type = "critical"
                cause = _("Unkown Reason")
                
                if user_manager.has_message():
                    cause = user_manager.get_message()
                
                message = _("Error deleting the Group with the ID %s - %s" % (id, cause))
                
            SwatMessages.add(message, type)
            redirect_to(controller='account', action='user')
        ##
        ## 
        ##
        else:        
            c.group_list = self.__manager.group_list
            
            c.list_users = False
            c.list_groups = True
            
            template = '/default/derived/account.mako'
            
        return render(template)
        
    def save(self):
        """ """
        id = request.params.get("id", -1)
        
        action = request.environ['pylons.routes_dict']['action']
        task = request.params.get("task", "").strip().lower()
        type = request.params.get("type", "").strip().lower()

        if type == "user":
            self.user(action, id)
        elif type == "group":
            self.group(action, id)
    
    def apply(self):
        """ """
        self.save()

    def cancel(self):
        """ """
        type = request.params.get("type", "").strip().lower()
        
        message = _("Editing canceled. No changes were saved.")
        SwatMessages.add(message, "warning")
        
        redirect_to(controller='account', action=type)
        
    def show_groups(self):
        """ """
        already_selected = request.params.get('as', '')
        log.debug("These are selected: " + already_selected)
        
        if len(already_selected) > 0:
            already_selected = already_selected.split(',')
        
        return render_mako_def('/default/component/popups.mako', \
                               'group_list', \
                               already_selected=already_selected)

class UserManager(object):
    """ Manager CRUD Operations for User Accounts """
    def __init__(self, manager):
        """ Class Constructor
        
        Keyword arguments
        manager -- A SAMPipeManager Instance with a valid connection to Samba
        
        """
        self.__manager = manager
        self.__message = ""
        
    def edit(self, id, is_new):
        """ Gets a User for editing. If we are adding a new User an empty
        User object will be returned
        
        Keyword arguments:
        id -- The ID of the User we are editing
        is_new -- Indicated if the User we are editing is new (actually means
        we are adding one) or not
        
        Returns:
        A User Object or None if there is an error
        
        """
        user = None

        try:
            if not is_new:
                user = self.__manager.fetch_user(id)
            else:
                user = User("", "", "", -1)
        except RuntimeError as message:
            log.debug(message)
            self.__set_message(message)
            
        return user
    
    def remove(self, id):
        """ Removes a User with a certain ID from the User Database
        
        Keyword arguments:
        id -- The ID of the User to remove
        
        Returns:
        Boolean indicating if the operation suceeded or not
        
        """
        removed = False
        
        try:
            self.__manager.delete_user(User("", "", "", id))
            removed = True
        except RuntimeError as message:
            log.debug(message)
            self.__set_message(message)
        
        return removed

    def save(self, id, is_new):
        """ Saves User Information to the Database
        
        Keyword arguments:
        id -- If the User already exists this will be his ID
        is_new -- Indicates if we are the user we are adding if new or not
        
        Returns:
        Boolean indicating if the operation suceeded or not
        
        """
        saved = False
        
        try:
            ##
            ## Basic
            ##
            username = request.params.get("account_username", "")
            fullname = request.params.get("account_fullname", "")
            description = request.params.get("account_description", "")
            
            password = request.params.get("account_password", "")
            confirm_password = request.params.get("confirm_password", "")
            
            if len(password) > 0 and password != confirm_password:
                return False
            
            user = User(username, fullname, description, id)
            
            ##
            ## Account Status
            ## FIXME too complicated
            ##
            user.must_change_password = request.params.get("account_must_change_password", "no")
            if user.must_change_password == "yes":
                user.must_change_password = True
            else:
                user.must_change_password = False
                
            user.cannot_change_password = request.params.get("account_cannot_change_password", "no")
            if user.cannot_change_password == "yes":
                user.cannot_change_password = True
            else:
                user.cannot_change_password = False
        
            user.password_never_expires = request.params.get("account_password_never_expires", "no")
            if user.password_never_expires == "yes":
                user.password_never_expires = True
            else:
                user.password_never_expires = False
            
            user.account_disabled = request.params.get("account_account_disabled", "no")
            if user.account_disabled == "yes":
                user.account_disabled = True
            else:
                user.account_disabled = False
            
            user.account_locked_out = request.params.get("account_account_locked_out", "no")
            if user.account_locked_out == "yes":
                user.account_locked_out = True
            else:
                user.account_locked_out = False
                
            ##
            ## Profile
            ##
            user.profile_path = request.params.get("account_profile_path", "")
            user.logon_script = request.params.get("account_logon_script", "")
            user.homedir_path = request.params.get("account_homedir_path", "")
            user.map_homedir_drive = int(request.params.get("account_map_homedir_drive", ""))
            
            ##
            ## Groups
            ##
            user.group_list = []
            for g in request.params.get("account_group_list", "").split(","):
                for gg in self.__manager.group_list:
                    if gg.name == g.strip():
                        user.group_list.append(gg)
            
            if is_new:
                self.__manager.add_user(user)
                id = user.rid
            else:
                self.__manager.update_user(user)
            
            saved = True
        except RuntimeError as message:
            log.debug(message)
            self.__set_message(message)
        except TypeError, error:
            log.debug(message)
            self.__set_message(message)
 
        return saved
    
    def get_message(self):
        """ Gets the Status Message set by this Class """
        return self.__message
    
    def __set_message(self, message):
        """ Sets the Status Message for this Class """
        self.__message = str(message[1])
        
    def has_message(self):
        """ Checks if there is a Status Message to show to the User """
        if len(self.__message) > 0:
            return True
        return False

class GroupManager(object):
    def __init__(self, manager):
        """ Class Constructor
        
        Keyword arguments
        manager -- A SAMPipeManager Instance with a valid connection to Samba
        
        """
        self.__manager = manager
        self.__message = ""

    def edit(self, id, is_new):
        """ Gets a Group for editing. If we are adding a new Group an empty
        Group object will be returned
        
        Keyword arguments:
        id -- The ID of the Group we are editing
        is_new -- Indicated if the Group we are editing is new (actually means
        we are adding one) or not
        
        Returns:
        A Group Object or None if there is an error
        
        """
        group = None

        try:
            if not is_new:
                group = self.__manager.fetch_group(id)
            else:
                group = Group("", "", -1)
        except RuntimeError as message:
            log.debug(message)
            self.__set_message(message)
            
        return group
    
    def remove(self, id):
        """ Removes a Group with a certain ID from the Group Database
        
        Keyword arguments:
        id -- The ID of the Group to remove
        
        Returns:
        Boolean indicating if the operation suceeded or not
        
        """
        removed = False
        
        try:
            self.__manager.delete_group(Group("", "", id))
            removed = True
        except RuntimeError as message:
            log.debug(message)
            self.__set_message(message)
        
        return removed
    
    def save(self, id, is_new):
        """ Saves Group Information to the Database
        
        Keyword arguments:
        id -- If the Group already exists this will be its ID
        is_new -- Indicates if we are the Group we are adding if new or not
        
        Returns:
        Boolean indicating if the operation suceeded or not
        
        """
        saved = False
        
        name = request.params.get("group_name", "")
        description = request.params.get("group_description", "")

        try:
            group = Group(name, description, id)
            
            if is_new:
                self.__manager.add_group(group)
                id = group.rid
            else:
                self.__manager.update_group(group)
                
            saved = True
        except RuntimeError as message:
            log.debug(message)
            self.__set_message(message)
            
        return saved

    """ Manager CRUD Operations for Groups """
    def get_message(self):
        """ Gets the Status Message set by this Class """
        return self.__message
    
    def __set_message(self, message):
        """ Sets the Status Message for this Class """
        self.__message = str(message[1])
        
    def has_message(self):
        """ Checks if there is a Status Message to show to the User """
        if len(self.__message) > 0:
            return True
        return False
