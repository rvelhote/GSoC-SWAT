<%doc>
#
# Group Editing Form Mako Template file for SWAT
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
    ${h.form('', method="post", id="group-form", class_="share-configuration")}
        <ol class="tab-list">
            <li id="tab1" class="active">
                <h3><a title="${_('Basic Group Configuration')}" class="title-icon basic-tab" href="#">${_('Basic')}</a></h3>                           
            </li>
            <li id="tab2">
                <h3><a title="${_('Group Members')}" class="title-icon basic-tab" href="#">${_('Members')}</a></h3>                           
            </li>   
        </ol>
    
        <ul class="tab-list-items"> 
            <li id="content-tab1" class="active tab">
                <ol class="col-1">
                    <li>${field.put("name", c.group.name)}</li>
                    <li>${field.put("description", c.group.description)}</li>
                </ol>
            </li>
            
            <li id="content-tab2" class="tab">
                % if c.user_group_list is not None and len(c.user_group_list) > 0:
                    <b>${_("There are %d Users assigned to this Group" % (len(c.user_group_list)))}</b>
                    
                    <ol>
                        % for user in c.user_group_list:
                            <li style="list-style-type:decimal-leading-zero;list-style-position:inside;">
                                <a target="_blank" title="${_('Edit this User. Will open in a New Window')}" href="${h.url_for("account_action", action="user", subaction="edit", id=user.rid)}">${user.username}</a>
                            </li>
                        % endfor
                    </ol>
                    
                % else:
                    ${_("There are no Users assigned to this Group")}
                % endif
            </li>            
        </ul>
        
        <div>
            ${h.hidden("task", request.environ['pylons.routes_dict']['subaction'])}
            ${h.hidden("id", c.group.rid)}
            ${h.hidden("type", "group")}
        </div>
    ${h.end_form()}
</%def>