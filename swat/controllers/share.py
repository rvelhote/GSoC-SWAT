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
BreadcrumbTrail, swat_messages

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
        c.share_name = name
        return render('/default/derived/edit-share.mako')
        
    def save(self):
        backend = None
        is_new = False
        
        if request.params.get("task", "edit") == "new":
            is_new = True
        
        if c.samba_lp.get("share backend") == "classic":
            backend = ShareBackendClassic(c.samba_lp, request.params)
            stored = backend.store(is_new)
            
            if stored:
                message = _("Share Information was Saved")
                swat_messages.add(message)
            else:
                swat_messages.add(backend.get_error(), backend.get_error_type())
        else:
            message = _("Your chosen backend is not yet supported")
            swat_messages.add(message)

        if request.environ['pylons.routes_dict']['action'] == "save":
            redirect_to(controller='share', action='index')

    def apply(self):
        self.save()
        redirect_to(controller='share', action='edit', name=request.params.get("name", ""))
    
    def cancel(self, name=''):
        message = _("Cancelled Share editing. No changes were saved!")
        swat_messages.add(message, "warning")
            
        redirect_to(controller='share', action='index')
        
    def path(self):
        path = request.params.get('path', '/')
        return render_mako_def('/default/component/popups.mako', 'select_path', \
                               current=path)
        
    def users_groups(self):
        return render_mako_def('/default/component/popups.mako', \
                               'select_user_group')
        
    def remove(self, name):
        backend = ShareBackendClassic(c.samba_lp, {'name':name})
        deleted = backend.delete()
        
        message = ""
        type = "cool"
        
        if deleted:
            message = _("Share Deleted Sucessfuly")
        else:
            message = _("Did not Delete Share")
            type = "warning"
        
        swat_messages.add(message, type)
        
        redirect_to(controller='share', action='index')
    
    def copy(self, name):
        backend = ShareBackendClassic(c.samba_lp, {'name':name})
        deleted = backend.copy()
    
        message = ""
        type = "cool"
        
        if deleted:
            message = _("Share Duplicated Sucessfuly")
        else:
            message = _("Did not Duplicate Share")
            type = "critical"

        swat_messages.add(message, type)
        
        redirect_to(controller='share', action='index')
    
    def toggle(self, name):
        backend = ShareBackendClassic(c.samba_lp, {'name':name})
        toggled = backend.toggle()
        
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

        if not self.__load_smb_conf_content():
            pass
    
    def __clean_params(self, params):
        clean_params = {}
        
        for param in params:
            if param.startswith('share_'):
                value = params.get(param)
                new_param = param[6:].replace('_', ' ')

                clean_params[new_param] = value

        return clean_params

    def __share_name_exists(self, name):
        if name not in self.__share_list:
            return False
        
        return True
        
    def __load_smb_conf_content(self):
        """ Loads the smb.conf into a Lists """
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
    
    def __get_section_position(self, name):
        """ Gets the position (in terms of line numbers) of where the section
        we are handling starts and ends.
        
        Returns a dictionary containing the start and end line numbers.
        
        Keyword arguments
        name -- the name of the current section. normally the share name we are
        taking care of
        
        """
        import re
        
        position = {}
        
        position['start'] = self.__smbconf_content.index('[' + name + ']\n')
        position['end'] = -1
        
        line_number = position['start'] + 1
        found = True

        for line in self.__smbconf_content[line_number:]:
            m = re.search("\[(.*)\]", line)
            
            if m is not None and found:
                position['end'] = line_number - 1
                break
            
            line_number = line_number + 1

        return position
    
    def store(self, is_new=False):
        pos = self.__get_section_position(self.__params.get("old_share_name", ""))
        section = self.__smbconf_content[pos['start']:pos['end']]
        
        new_section = self.__recreate_section(self.__params.get("name", ""), section)
        
        before = self.__smbconf_content[0:pos['start'] - 1]
        after = self.__smbconf_content[pos['end']:]
        
        self.__save_smbconf([before, new_section, after])
        
        return True
    
    def delete(self):
        pos = self.__get_section_position(self.__params["name"])

        before = self.__smbconf_content[0:pos['start'] - 1]
        after = self.__smbconf_content[pos['end']:]
        
        self.__save_smbconf([before, after])
        
        return True
    
    def copy(self):
        # Todo: bug, can't repeat the same twice due to name conflict
        new_name = "copy of " + self.__params["name"]
                
        if not self.__share_name_exists(new_name):
            pos = self.__get_section_position(self.__params["name"])
            section = self.__smbconf_content[pos['start']:pos['end']]
            
            new_section = self.__recreate_section(new_name, section)
        
            before = self.__smbconf_content[0:pos['start'] - 1]
            after = self.__smbconf_content[pos['end']:]

            self.__save_smbconf([before, section, new_section, after])
        
            return True
        
        return False
    
    def toggle(self):
        if self.__share_name_exists(self.__params["name"]):
            pos = self.__get_section_position(self.__params["name"])
            section = self.__smbconf_content[pos['start']:pos['end']]
            
            new_section = self.__recreate_section(self.__params["name"],
                                                                section, True)
        
            before = self.__smbconf_content[0:pos['start'] - 1]
            after = self.__smbconf_content[pos['end']:]

            self.__save_smbconf([before, new_section, after])
        
            return True
    
    def __recreate_section(self, name, section, deactivate=False):
        import re
        
        new_section = ['\n[' + name + ']\n']
        
        #for line in section[1:]:
            
        
        #if deactivate:
        #    name = "//" + name
        #
        #new_section = ['\n\n[' + name + ']\n']
        #already_handled = []
        #
        #for line in section[1:]:
        #    line_param = re.search("(.*)=(.*)", line)
        #
        #    if line_param is not None:
        #        value = line_param.group(2).strip()
        #        param = line_param.group(1).strip()
        #
        #        if 'share_' + param in self.__params:
        #            line = "\t" + param + " = " + self.__params.get("share_" + param) + "\n"
        #        else:
        #            line = "\t" + param + " = " + value + "\n"
        #            
        #        print param
        #            
        #        already_handled.append('share_' + param)
        #            
        #    if deactivate:
        #        line = "#" + line
        #
        #    new_section.append(line)
        #        
        #for param in self.__params:
        #    if param.startswith('share_') and param not in already_handled:
        #        value = self.__params.get(param)
        #        
        #        if len(value) > 0:
        #            param = param[6:].replace('_', ' ')
        #            
        #            line = "\t" + param + " = " + value + "\n"
        #            new_section.append(line)

        return new_section
    
    def __save_smbconf(self, what):
        stream = open(self.__smbconf, 'w')
        
        for area in what:
            for line in area:
                stream.write(line)
                
        stream.close()
    
    def set_error(self, message, type='critical'):
        pass

    def get_error(self):
        pass
