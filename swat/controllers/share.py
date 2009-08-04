#
# Share Management Controller file for SWAT
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
import param, shares

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from swat.lib.base import BaseController, render

from pylons.templating import render_mako_def
from pylons.i18n.translation import _
from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, swat_messages, ParamConfiguration

log = logging.getLogger(__name__)

class ShareController(BaseController):
    """ Share Management controller Will handle all operations concerning
    Shares in SWAT.
    
    """

    def __init__(self):
        """ Initialization. Load the controller's configuration, builds the
        breadcrumb trail based on that information and load the backend
        information
        
        There are a few operations that don't require this initialization e.g.
        save, apply, cancel; they always redirect somewhere. therefore, there
        is a list of allowed operations that is checked to see if it's ok to
        load the configuration
        
        """
        me = request.environ['pylons.routes_dict']['controller']
        action = request.environ['pylons.routes_dict']['action']
        
        allowed = ('index', 'add', 'edit', 'add_assistant')
        
        if action in allowed:
            c.config = ControllerConfiguration(me, action)
            
            c.breadcrumb = BreadcrumbTrail(c.config)
            c.breadcrumb.build()

        c.samba_lp = param.LoadParm()
        c.samba_lp.load_default()

        c.share_list = shares.SharesContainer(c.samba_lp)
    
    def index(self):        
        """ Point of entry. Loads the Share List Template """
        return render('/default/derived/share.mako')
        
    def add(self):
        """ Add a New Share. Loads the Share Edition Template. It's the same as
        calling the edit template but with an empty share name
        
        """
        return self.edit('')
    
    def add_assistant(self):
        pass
    
    def edit(self, name):
        """ Edit a share. Loads the Share Edition Template.
        
        Keyword arguments:
        name -- the share name to load the information from
        
        """
        
        if name not in c.share_list:
            swat_messages.add(_("Can't edit a Share that doesn't exist"), "warning")
            redirect_to(controller='share', action='index')
        else:
            c.p = ParamConfiguration('share-parameters')
            c.share_name = name
            return render('/default/derived/edit-share.mako')
        
    def save(self):
        """ Save a Share. We enter here either from the 'edit' or 'add' """
        backend = None
        is_new = False
        
        if request.params.get("task", "edit") == "add":
            is_new = True
        
        if c.samba_lp.get("share backend") == "classic":
            backend = ShareBackendClassic(c.samba_lp, request.params)
            stored = backend.store(is_new)
            
            if stored:
                message = _("Share Information was Saved")
                swat_messages.add(message)
            else:
                swat_messages.add(backend.get_error_message(), backend.get_error_type())
        else:
            message = _("Your chosen backend is not yet supported", "critical")
            swat_messages.add(message)

        if request.environ['pylons.routes_dict']['action'] == "save":
            redirect_to(controller='share', action='index')

    def apply(self):
        """ Apply changes done to a Share. This action is merely an alias for
        the save action but it redirects to the Share's edit page instead.
        
        """
        self.save()

        if len(request.params.get("name", "")) == 0:
            redirect_to(controller='share', action='add')
        else:
            redirect_to(controller='share', action='edit', name=request.params.get("name", ""))
    
    def cancel(self, name=''):
        """ Cancel the current editing/addition of the current Share """
        if request.params.get("task", "edit") == "add":
            message = _("Cancelled New Share. No Share was added!")
        elif request.params.get("task", "edit") == "edit":
            message = _("Cancelled Share editing. No changes were saved!")
        
        swat_messages.add(message, "warning")
        redirect_to(controller='share', action='index')
        
    def path(self):
        """ Returns the contents of the selected folder. Usually called via
        AJAX using the Popup that allows the user to select a path
        
        """
        path = request.params.get('path', '/')
        return render_mako_def('/default/component/popups.mako', 'select_path', \
                               current=path)
        
    def users_groups(self):
        """ Returns the HTML containing a list of the System's Users and Groups.
        Usually called via AJAX using the Popup that allows the user to select
        Users and Groups.
        
        """
        return render_mako_def('/default/component/popups.mako', \
                               'select_user_group')
        
    def remove(self, name):
        """ Deletes a Share from the current Backend
        
        Keyword arguments:
        name -- the name of the share to be deleted
        
        """
        if c.samba_lp.get("share backend") == "classic":
            backend = ShareBackendClassic(c.samba_lp, {'name':name})
            deleted = backend.delete()
            
            message = ""
            type = "cool"
            
            if deleted:
                message = _("Share Deleted Sucessfuly")
            else:
                message = backend.get_error_message()
                type = backend.get_error_type()
            
            swat_messages.add(message, type)
        else:
            message = _("Your chosen backend is not yet supported", "critical")
            swat_messages.add(message)
        
        redirect_to(controller='share', action='index')
    
    def copy(self, name):
        """ Clones the chosen Share
        
        Keyword arguments:
        name -- the name of the share to be duplicated
        
        """
        if c.samba_lp.get("share backend") == "classic":
            backend = ShareBackendClassic(c.samba_lp, {'name': name})
            deleted = backend.copy()
        
            message = ""
            type = "cool"
            
            if deleted:
                message = _("Share Duplicated Sucessfuly")
            else:
                message = backend.get_error_message()
                type = backend.get_error_type()

            swat_messages.add(message, type)
        else:
            message = _("Your chosen backend is not yet supported", "critical")
            swat_messages.add(message)
            
        redirect_to(controller='share', action='index')
    
    def toggle(self, name):
        """ Toggles a Share's state (enabled/disabled).
        
        At the moment it is disabled because I'm not sure how I can implement
        this sucessfuly.
        
        Keyword arguments:
        name -- the name of the share to be toggled
        
        """
        if c.samba_lp.get("share backend") == "classic":
            backend = ShareBackendClassic(c.samba_lp, {'name':name})
            toggled = backend.toggle()
            
            if toggled:
                message = _("Share Toggled successfuly")
                swat_messages.add(message)
            else:
                swat_messages.add(backend.get_error_message(), backend.get_error_type())
        else:
            message = _("Your chosen backend is not yet supported", "critical")
            swat_messages.add(message)
        
        redirect_to(controller='share', action='index')

class ShareBackendClassic():
    """ Handles operations regarding the Classic Backend method to store share
    information. The classic method stores shares in the smb.conf file
    
    """
    def __init__(self, lp, params):
        """ Constructor. Loads the smb.conf contents into a List to be used
        by each of the operations allowed by this backend
        
        Keyword arguments
        smbconf -- last smb.conf file loaded by the param module
        params -- request parameters passed by the share information form
        
        """
        self.__lp = lp
        self.__smbconf = self.__lp.configfile
        
        #   Important values
        self.__share_name = params.get("name")
        self.__share_old_name = params.get("old_name")
        
        #   Cleanup names from the 'share_' form into the valid Samba name
        self.__params = self.__clean_params(params)
        
        self.__smbconf_content = []
        self.__error = ""
        self.__share_list = shares.SharesContainer(self.__lp)
        
        #   Errors
        self.__error = {}
        self.__error['message'] = ""
        self.__error['type'] = "critical"

        self.__load_smb_conf_content()
    
    def __clean_params(self, params):
        """ Copies all parameters starting with 'share_' in the current request
        object to a clean dictionary.
        
        All parameters submited through the form related to the share always
        use the prefix. This is so I can distinguish them from other random
        parameters that may be around.
        
        Keyword arguments:
        params -- contains the request.params object from Pylons
        
        """
        clean_params = {}
        
        for param in params:
            if param.startswith('share_'):
                value = params.get(param)
                new_param = param[6:].replace('_', ' ')

                clean_params[new_param] = value

        return clean_params

    def __share_name_exists(self, name):
        """ Checks if a Share exists in the ShareContainer object
        
        Keyword arguments:
        name -- the name of the share to check
        
        """
        if name not in self.__share_list:
            return False
        
        return True
        
    def __load_smb_conf_content(self):
        """ Loads the smb.conf into a List using readlines()
        
        Returns a boolean value indicating if the file's content was loaded or
        not.
        
        """
        file_exists = False
        
        try:
            stream = open(self.__smbconf, 'r')
        except IOError:
            file_exists = False
        else:
            file_exists = True
            
        if file_exists:
            self.__smbconf_content = stream.readlines()
            stream.close()

        return file_exists
    
    def __section_exists(self, name):
        """ Checks if a section exists in the loaded smb.conf file. Also reloads
        the contents of the backend so we can always check against an updated
        copy without reloading LoadParm.
        
        I think it's better to reload param.LoadParm but I'll keep it like this
        for now :)
        
        Keyword arguments:
        name -- the share name
        
        Returns a Boolean value indicating if the section exists or not
        
        """
        self.__load_smb_conf_content()
        
        exists = False
        position = -1
        
        try:
            position = self.__smbconf_content.index('[' + name + ']\n')
            exists = True
        except ValueError:
            self.set_error("Share doesn't exist!", "critical")
            position = -1
        
        return exists
        
    def __get_section_position(self, name):
        """ Gets the position (in terms of line numbers) of where the section
        we are handling starts and ends.
        
        Keyword arguments
        name -- the name of the current section. normally the share name we are
        taking care of
        
        Returns a dictionary containing the start and end line numbers.
        
        """
        import re
        
        position = {}
        position['start'] = self.__smbconf_content.index('[' + name + ']\n')
        position['end'] = -1
        
        line_number = position['start'] + 1

        for line in self.__smbconf_content[line_number:]:
            m = re.search("\[(.+)\]", line)
            
            if m is not None:
                position['end'] = line_number - 1
                break
            
            line_number = line_number + 1
            
        if position['end'] == -1:
            position['end'] = len(self.__smbconf_content)

        return position
    
    def store(self, is_new=False):
        """ Store a Share, either from an edit or add.
        
        Breaks down the current smb.conf to find the chosen section (if editing)
        and recreates that section with the new values. Maintains comments that
        may be around that section.
        
        If we are adding a new share it's just added to the end of the file
        
        Keyword arguments:
        is_new -- indicates if it's a new share (or not)
        
        Returns a boolean value indicating if the share was stored correctly
        
        """
        stored = False
        section = []
        
        if len(self.__share_name) == 0:
            self.set_error(_("Can't create Share with an empty name"), "critical")
        else:
            if not is_new:
                
                if self.__share_name_exists(self.__share_old_name):
                    pos = self.__get_section_position(self.__share_old_name)
                    section = self.__smbconf_content[pos['start']:pos['end']]
                    
                    before = self.__smbconf_content[0:pos['start'] - 1]
                    after = self.__smbconf_content[pos['end']:]
                else:
                    #
                    #   Have to break it here to avoid "tricks" downstairs :P
                    #
                    self.set_error(_("You are trying to save a Share\
                                    that doesn't exist"), "critical")
                    return False
            else:
                before = self.__smbconf_content
                after = []
            
            new_section = self.__recreate_section(self.__share_name, section)
            self.__save_smbconf([before, new_section, after])
            
            if self.__section_exists(self.__share_name):
                stored = True
            else:
                self.set_error(_("Could not add/edit that Share. No idea why..."), "warning")

        return stored
    
    def delete(self):
        """ Deletes a share from the backend
        
        Returns a boolean value indicating if the Share was deleted sucessfuly
        
        """
        deleted = False
        
        if self.__share_name_exists(self.__share_name):
            pos = self.__get_section_position(self.__share_name)
    
            before = self.__smbconf_content[0:pos['start'] - 1]
            after = self.__smbconf_content[pos['end']:]
            
            self.__save_smbconf([before, after])

            if self.__section_exists(self.__share_name):
                self.set_error(_("Could not delete that Share.\
                                 The Share is still in the Backend.\
                                 No idea why..."), "critical")
            else:
                deleted = True
        else:
            self.set_error(_("Can't delete a Share that doesn't exist!"), "warning")
        
        return deleted
    
    def copy(self):
        """ Copies a Share.
        
        Returns a boolean value indicating if the Share was copied sucessfuly
        
        BUG: Can't repeat the same share twice due to name conflict. If you try
        to copy 'test' once it will create 'copy of test'. If you try copy again
        it will fail because 'copy of test' already exists.
        
        """
        new_name = _("copy of") + " " + self.__share_name
        copied = False
                
        if not self.__share_name_exists(new_name):
            if self.__share_name_exists(self.__share_name):
                pos = self.__get_section_position(self.__share_name)
                section = self.__smbconf_content[pos['start']:pos['end']]
                
                new_section = self.__recreate_section(new_name, section)
            
                before = self.__smbconf_content[0:pos['start'] - 1]
                after = self.__smbconf_content[pos['end']:]
    
                self.__save_smbconf([before, section, new_section, after])
                
                if self.__section_exists(new_name):
                    copied = True
                else:
                    self.set_error(_("Could not copy that Share. No idea why..."), "warning")
            else:
                self.set_error(_("Did not duplicate Share because the original doesn't exist!"), "critical")
        
        else:
            self.set_error(_("Did not duplicate Share because the copy already exists!"), "critical")
        
        return copied
    
    def toggle(self):
        self.set_error("Toggle Not Implemented", "warning")
        return False
    
    def __recreate_section(self, name, section):
        """ Recreate the section we are editing/adding with the new values
        
        Keyword arguments:
        name -- the name of the section
        section -- split list of the smb.conf contents containing just the
        information from the chosen section. to obtain the section "coordinates"
        call self.__get_section_position(name)
        
        Returns the new section to write to the backend
        
        """
        import re
        
        new_section = ['\n[' + name + ']\n']
        
        #   Scan the current section in search for existing values. I could
        #   just dump the content of params but this will keep other things
        #   that the user might have written to the file; a comment on a param
        #   for example
        #
        for line in section[1:]:
            line_param = re.search("(.+)=(.+)", line)
            
            if line_param is not None:
                param = line_param.group(1).strip()
                value = line_param.group(2).strip()

                if param in self.__params:
                    if len(self.__params[param]) > 0:
                        line = "\t" + param + " = " + self.__params[param] + "\n"
                        del self.__params[param]
                else:
                    line = "\t" + param + " = " + value + "\n"
            
            new_section.append(line)
            
        #   Now we dump the params file.
        #   With the already handled key=>values deleted we can safely add all
        #   of the available parameters from the POST
        #
        for param, value in self.__params.items():
            if len(value) > 0:
                line = "\t" + param + " = " + value + "\n"
                new_section.append(line)

        return new_section
    
    def __save_smbconf(self, what):
        """ Saves the changes made to smb.conf """
        import shutil
        import os
        
        stream = open(self.__smbconf + ".new", 'w')
        ok = True
        
        for area in what:
            for line in area:
                try:
                    stream.write(line)
                except:
                    ok = False   
                    break;
                
            if not ok:
                break
        
        if ok:
            try:
                shutil.move(self.__smbconf, self.__smbconf + ".old")
                shutil.move(self.__smbconf + ".new", self.__smbconf)
            except:
                pass

        try:
            os.remove(self.__smbconf + ".new")
        except:
            pass
    
    def set_error(self, message, type='critical'):
        """ Sets the error message to indicate what has failed with the operation
        that was being done using this Backend
        
        Keyword arguments:
        message -- the error message
        type -- the type of error
        
        """
        self.__error['message'] = message
        self.__error['type'] = type

    def get_error_message(self):
        """ Gets the current error message """
        return self.__error['message'] or _('I have nooooo idea...')
    
    def get_error_type(self):
        """ Gets the current error type """
        return self.__error['type'] or 'critical'
