<%doc>
#
# Account Management Index Mako Template file for SWAT
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
<%inherit file="/default/base/base.mako" />
<%namespace name="toolbar" file="/default/component/toolbar.mako" />
<%namespace name="pagination" file="/default/component/pagination.mako" />

${parent.action_title(c.config.get_action_info('friendly_name'))}
${toolbar.write(c.config.get_toolbar_items())}
${options(c.config.get_action())}
<div class="account-list">
    % if c.list_users == True:
        ${user_table(c.user_list)}
    % endif
    
    % if c.list_groups == True:
        ${group_table(c.group_list)}
    % endif
</div>

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: ${c.config.get_action_info('friendly_name')}
</%def>

<%doc>TODO make tabs or mix them up?</%doc>
<%def name="user_table(users, table_id='user-list', table_class='')">

    % if len(users) > 0:
        <% table_class = table_class + " not-empty" %>
    % endif

    % if c.list_groups == True:
        <h3>${_("User List")}</h3>
    % endif

    <table id="${table_id}" class="list ${table_class}">
	<thead>
	    <tr>
		<td class="check-all"><input title="${_('Check All Items')}" onchange="checkAllRows(this, 'check-row-user')" type="checkbox" id="check-all-user"/></td>
		<td class="user-row-id">${_('#')}</td>
		<td class="user-gid">${_('UID')}</td>
		<td class="user-name">${_('Username')}</td>
		<td class="user-description">${_('Description')}</td>
		<td class="user-quick-operations"></td>
	    </tr>
	</thead>
	
        % if len(users) > 0:
            <tfoot>
                <tr>
                    <td colspan="6">		    
                        <div class="pagination">
                            <% pagination.numbers(_("Users"), len(users), c.per_page, c.current_page) %>
                            <% pagination.paginate(len(users), c.per_page, c.current_page) %>
                        </div>
                    </td>
                </tr>
            </tfoot>
        % endif
        
        <%
        
        i = 1
        
        begin = (c.current_page - 1) * c.per_page
        end = begin + c.per_page
        
        %>
        
        % for user in users[begin:end]:
            <% tr_class = '' %>
            
            % if i % 2 == 0:
                <% tr_class = " alternate-row " %>
            % endif
        
            <tr id="row-user-${i}" title="${_('Edit User')}" class="${tr_class}">
                <td><input value="${user.username}" onchange="selectShareRow(this);" name="name" type="checkbox" id="check-row-user-${i}" /></td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='user', subaction='edit', id=user.rid)}');">${i}</td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='user', subaction='edit', id=user.rid)}');">${user.rid}</td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='user', subaction='edit', id=user.rid)}');">${user.username}</td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='user', subaction='edit', id=user.rid)}');">${user.description}</td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='user', subaction='edit', id=user.rid)}');">${quick_tasks(user.rid, "User", False)}</td>
            </tr>
            
            <% i = i + 1 %>
        % endfor
    </table>
</%def>

<%def name="group_table(groups, table_id='group-list', table_class='')">
    % if len(groups) > 0:
        <% table_class = table_class + " not-empty" %>
    % endif

    % if c.list_users == True:
        <h3>${_("Group List")}</h3>
    % endif
    
    <table id="${table_id}" class="list ${table_class}">
	<thead>
	    <tr>
		<td class="check-all"><input title="${_('Check All Items')}" onchange="checkAllRows(this, 'check-row-group')" type="checkbox" id="check-all-group"/></td>
		<td class="group-row-id">${_('#')}</td>
		<td class="group-gid">${_('GID')}</td>
		<td class="group-name">${_('Group Name')}</td>
		<td class="group-description">${_('Description')}</td>
		<td class="group-quick-operations"></td>
	    </tr>
        </thead>

        % if len(groups) > 0:
            <tfoot>
                <tr>
                    <td colspan="6">		    
                        <div class="pagination">
                            <% pagination.numbers(_("Groups"), len(groups), c.per_page, c.current_page) %>
                            <% pagination.paginate(len(groups), c.per_page, c.current_page) %>
                        </div>
                    </td>
                </tr>
            </tfoot>
        % endif
        
        <%
        
        i = 1
        
        begin = (c.current_page - 1) * c.per_page
        end = begin + c.per_page
        
        %>
        
        % for group in groups[begin:end]:
        
            <% tr_class = '' %>
            
            % if i % 2 == 0:
                <% tr_class = " alternate-row " %>
            % endif
        
            <tr id="row-group-${i}" title="${_('Edit Group')}" class="${tr_class}">
                <td><input value="${group.name}" onchange="selectShareRow(this);" name="name" type="checkbox" id="check-row-group-${i}" /></td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='group', subaction='edit', id = group.rid)}');">${i}</td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='group', subaction='edit', id = group.rid)}');">${group.rid}</td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='group', subaction='edit', id = group.rid)}');">${group.name}</td>
                <td onclick="clickableRow('${h.url_for('account_action', controller='account', action='group', subaction='edit', id = group.rid)}');">${group.description}</td>
                <td>${quick_tasks(group.rid, "Group", False)}</td>
            </tr>
            
            <% i = i + 1 %>
        % endfor
    </table>
</%def>
    
<%def name="quick_tasks(id, type, is_disabled=False)">
    <ul class="quick-tasks">
        <li><a href="${h.url_for('account_action', action=type.lower(), subaction='edit', id=id)}" title="${_('Edit %s' % (type))}"><img src="/default/images/icons/folder-pencil.png" alt="${_('Edit %s Icon' % (type))}"/></a></li>
	<li><a href="${h.url_for('account_action', action=type.lower(), subaction='remove', id=id)}" title="${_('Remove %s' % (type))}"><img src="/default/images/icons/folder-minus.png" alt="${_('Remove %s Icon' % (type))}"/></a></li>
    </ul>
</%def>

<%def name="options(action_name)">
    ${h.form(h.url_for(controller = 'account', action = action_name), method="get", id="options")}
        <div style="font-size:85%;margin-bottom:15px;">
            <span>
                <label title="${_("You may use Regular Expressions")}" for="filter_account_by_name">${_('Filter')}:</label>
                ${h.text("filter_value", c.filter_name, id="filter_account_by_name")}
            </span>
            
            % if len(c.filter_name) > 0 or int(c.per_page) != 10:
                <a class="reset-view round-2px" href="${h.url_for(controller = 'account', action = action_name)}">${_("reset view")}</a>
            % endif
            
            <span style="float:right;">
                <label for="items_per_page">${_('Per Page')}:</label>
                <select name="per_page" id="items_per_page" onchange="submitForm('options');">
                    % for i in range(5, 30, 5):
                        <option
                        
                        % if i == c.per_page:
                            ${'selected="selected"'}
                        
                        % endif
                        
                        value="${i}">${i}</option>
                    % endfor
                </select>
            </span>
            
        </div>
    ${h.end_form()}
</%def>