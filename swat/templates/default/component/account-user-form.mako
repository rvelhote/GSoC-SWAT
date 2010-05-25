<%doc>
#
# User Account Editing Form Mako Template file for SWAT
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
</%doc>

<%namespace name="field" file="/default/component/form-fields.mako" />

<%def name="write()">
    ${h.form('', method="post", id="user-account-form", class_="share-configuration")}
        <ol class="tab-list">
            <li id="tab1" class="active">
                <h3><a title="${_('Basic User Configuration')}" class="title-icon basic-tab" href="#">${_('Basic')}</a></h3>                           
            </li>
            <li id="tab2">
                <h3><a title="${_('Account Status')}" class="title-icon basic-tab" href="#">${_('Status')}</a></h3>                           
            </li>
            <li id="tab3">
                <h3><a title="${_('User Profile Storage')}" class="title-icon basic-tab" href="#">${_('Profile')}</a></h3>                           
            </li>
            <li id="tab4">
                <h3><a title="${_('Assigned Groups')}" class="title-icon basic-tab" href="#">${_('Groups')}</a></h3>                           
            </li>
        </ol>
    
        <ul class="tab-list-items"> 
            <li id="content-tab1" class="active tab">
                <ol class="col-1">
                    <li>${field.put("username", c.user.username)}</li>
                    <li>${field.put("fullname", c.user.fullname)}</li>
                    <li>${field.put("description", c.user.description)}</li>
                    <li>${field.put("password", "")}</li>
                    <li>${field.put("confirmpassword", "")}</li>
                </ol>
            </li>
            
            <li id="content-tab2" class="tab">
                <ol class="col-1">
                    <li>${field.put("mustchange", c.user.must_change_password)}</li>
                    <li>${field.put("cannotchange", c.user.cannot_change_password)}</li>
                    <li>${field.put("neverexpires", c.user.password_never_expires)}</li>
                    <li>${field.put("disabled", c.user.account_disabled)}</li>
                    <li>${field.put("locked", c.user.account_locked_out)}</li>
                </ol>
            </li>
            
            <li id="content-tab3" class="tab">
                <ol class="col-1">
                    <li>${field.put("profilepath", c.user.profile_path)}</li>
                    <li>${field.put("logonscriptname", c.user.logon_script)}</li>
                    <li>${field.put("homedirpath", c.user.homedir_path)}</li>
                    <li>${field.put("maphomedirdrive", c.user.map_homedir_drive)}</li>
                </ol>
            </li>

            <li id="content-tab4" class="tab">
                <ol class="col-1">
                    <%
                    group_ids = []
                    for g in c.user.group_list:
                        group_ids.append(g.name)
                    %>
                    <li>${field.put("groups", group_ids)}</li>
                </ol>
            </li>
        </ul>
     
        <div>
            ${h.hidden("task", request.environ['pylons.routes_dict']['action'])}
            ${h.hidden("id", c.user.rid)}
            ${h.hidden("type", "user")}
        </div>
    ${h.end_form()}
</%def>
