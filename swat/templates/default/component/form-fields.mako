<%doc>
#
# Form Fields Mako Template file for SWAT
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

<%doc>Help Text Associated with this Parameter</%doc>
<%def name="help(id, no_margin=False)">
    <% extra_class = "" %>
    % if no_margin:
        <% extra_class = "no-margin" %>
    % endif
    
    <p class="option-help ${extra_class}">${c.p.get_value(id, "help")}</p>
</%def>
    
<%def name="disabled(id)">
    <p class="disabled-param">${_("This parameter is not yet handled by Samba4!")}</p>
</%def>

<%doc>Text</%doc>
<%def name="text(id, value)">
    <label for="${c.p.get_value(id, "id")}" title="${c.p.get_value(id, "title")}">${c.p.get_value(id, "label")}:</label>
    ${h.text(c.p.get_value(id, "name"), value, id=c.p.get_value(id, "id"), style="float:left;", class_=c.p.get_value(id, "class") + " " + c.p.get_value(id, "validation"))}
</%def>
    
<%doc>Boolean</%doc>
<%def name="checkbox(id, value)">
    <%
    
    if value == True or value == "yes":
        value = True
    else:
        value = False
        
    %>

    ${h.hidden(c.p.get_value(id, "name"), 'no')}
    ${h.checkbox(c.p.get_value(id, "name"), 'yes', value, id=c.p.get_value(id, "id"), class_=c.p.get_value(id, "class"))}
    <label class="checkbox" for="${c.p.get_value(id, "id")}" title="${c.p.get_value(id, "title")}">${c.p.get_value(id, "label")}</label>                                    
</%def>
    
<%doc></%doc>
<%def name="permissions(id, value)">
    <p class="field-title">${c.p.get_value(id, "title")}</p>
    <%
    
    # 
    # Classic returns Octal
    # LDB returns Decimal
    #
    if c.share.is_classic():
        value = value or 0
        value = oct(value)

    %>

    <% permissions = [["0", _("Do Nothing")], ["4", _("Read Only")], ["2", _("Write Only")], ["6", _("Read and Write")], ["5", _("Read and Execute")], ["7", _("Read, Write and Execute")]]%>
    <% permissionGroups = [[_("Owner Can"), "owner", 6, 1], [_("Group Members Can"), "group", 4, 1], [_("Everyone Else Can"), "world", 4, 1]] %>
    <% name = c.p.get_value(id, 'permissions-name') %>
    
    <ul class="permissions-selection">
        <% i = 1 %>
        
        % for grp in permissionGroups:
            <li>
                <label for="${id}-${grp[1]}">${grp[0]}:</label>
                
                <%
                
                try:
                    perm_value = value[i]
                except:
                    perm_value = grp[2]
                
                %>
                
                ${h.select(name + "_" + grp[1], perm_value, permissions, style="float:left;font-size:85%;", id=id + "-" + grp[1], onchange='calcPermissions("' + id + '", "' + id + '");')}
            </li>
            <% i = i + 1 %>
        % endfor
    </ul>

    ${h.hidden(c.p.get_value(id, 'name'), value, id=id)}
</%def>
    
<%def name="popup(id, op)">
    <% copy_to = c.p.get_value(id, 'field-ops-descriptor/' + op + '/link/copy-to') or c.p.get_value(id, 'id') %>
    <a href="${h.url_for(controller=c.p.get_value(id, 'field-ops-descriptor/' + op + '/link/controller'), action=c.p.get_value(id, 'field-ops-descriptor/' + op + '/link/action'))}?copyto=${copy_to}" class="popup-selector ${op}" title="${c.p.get_value(id, 'field-ops-descriptor/' + op + '/title')}"><img src="/default/images/icons/${c.p.get_value(id, 'field-ops-descriptor/' + op + '/image/name')}" alt="${c.p.get_value(id, 'field-ops-descriptor/' + op + '/image/alt')}" /></a>
</%def>
    
<%def name="manual_add(id, op)">
    <% copy_to = c.p.get_value(id, 'field-ops-descriptor/' + op + '/link/copy-to') or c.p.get_value(id, 'id') %>
    <% copy_from = c.p.get_value(id, 'field-ops-descriptor/' + op + '/link/copy-from') or c.p.get_value(id, 'id') %>
    <a class="${op}" href="?copyto=${copy_to}&amp;copyfrom=${copy_from}" title="${c.p.get_value(id, 'field-ops-descriptor/' + op + '/title')}"><img src="/default/images/icons/${c.p.get_value(id, 'field-ops-descriptor/' + op + '/image/name')}" alt="${c.p.get_value(id, 'field-ops-descriptor/' + op + '/image/alt')}" /></a>
</%def>
    
<%def name="modifiers(id, op)">
    <% modifier_list = c.p.get_value(id, 'field-ops-descriptor/' + op + '/list') %>
    
    % if len(modifier_list) > 0:
        <select style="font-size:77%;" onchange="var p = $('share-path'); p.setProperty('value', p.getProperty('value') + this.value);">
            % for m in modifier_list:
                <option value="${c.p.get_value(id, 'modifiers-descriptor/' + m + '/value')}">
                    ${c.p.get_value(id, 'modifiers-descriptor/' + m + '/title')}
                </option>
            % endfor
        </select>
    % endif
</%def>
    
<%def name="field_ops(id, ops)">
    % if ops != "":
        <ol class="field-ops">
            % for op in ops:
                <li>
                    <%
                    
                    #
                    # FIXME not specific to shares anymore. do this elsewhere
                    #
                    
                    %>
                    
                    % if op == "user-group-selection" or op == "path-selection":
                        <% popup(id, op) %>
                    % elif op == "manual-add":
                        <% manual_add(id, op) %>
                    % elif op == "modifiers":
                        <% modifiers(id, op) %>
                    % endif
                </li>
            % endfor
        </ol>
    % endif
</%def>
        
<%def name="list(id, value)">
    <label for="${c.p.get_value(id, "id")}" title="${c.p.get_value(id, "title")}">${c.p.get_value(id, "label")}:</label>
    ${h.text('', '', id=c.p.get_value(id, "id"), style="float:left;", class_=c.p.get_value(id, "class"))}
    
    <%
    
    field_ops(id, c.p.get_value(id, "field-ops"))
    list_values = ""

    if value and len(value) > 0:
        list_values = ",".join(["%s" % v for v in value])
    
    %>
    
    ${h.hidden(c.p.get_value(id, "name"), list_values, id=c.p.get_value(id, "id") + '-list-textbox', class_=c.p.get_value(id, "validation"))}
    <% list_id = c.p.get_value(id, "id") + "-list" %>
    
    <ul id="${list_id}" class="user-list">
        % if list_values:
            <% i = 1 %>
            % for v in value:
                <li>
                    <a class="delete-link" id="delete-${list_id}-${i}" title="Remove this item from the list" href="#">${v}</a>
                </li>
                <% i = i + 1 %>
            % endfor
        % endif
    </ul>
</%def>
    
<%doc>Choose which type to call</%doc>
<%def name="put(id, param_value=None)">
    <%
    
    type = c.p.get_value(id, "type")
    help(id, c.p.get_value(id, "disabled"))
        
    if c.p.get_value(id, "disabled") == True:
        disabled(id)

    validations = c.p.get_value(id, "validation-message")

    %>
    
    % if len(validations) > 0:
        % for validation in validations:
            <%
            #
            # FIXME a little hack just to make a little test with the validators.
            # I was testing if it validated hidden fields.
            # One thing that's missing in some of the fields is the inclusion of
            # the validator class
            #
            %>
            % if type == "list":
                <p class="validation-message round-2px" id="${c.p.get_value(id, "id")}-list-textbox-error-${validation}">
                    ${c.p.get_value(id, "validation-message/" + validation)}
                </p>
            % else:
                <p class="validation-message round-2px" id="${c.p.get_value(id, "id")}-error-${validation}">
                    ${c.p.get_value(id, "validation-message/" + validation)}
                </p>
            % endif
        % endfor
    % endif

    <%
    #   locals() is not working here otherwise I could just call this once
    #   based on type
    #
    #   TODO: figure out a way to use it for mako defs
    #
    if type == "text":    
        text(id, param_value)
    elif type == "checkbox":
        checkbox(id, param_value)
    elif type == "permissions":
        permissions(id, param_value)
    elif type == "list":
        list(id, param_value)

    if type != "list":
        field_ops(id, c.p.get_value(id, "field-ops"))

    %>
</%def>