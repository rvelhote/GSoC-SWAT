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
    ${h.text(c.p.get_value(id, "name"), value, id=c.p.get_value(id, "id"), style="float:left;", class_=c.p.get_value(id, "class"))}
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
    
    # FIXME this was working... hmm...
    value = value or 0
    value = oct(int(value))

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
    
    <% field_ops(id, c.p.get_value(id, "field-ops")) %>
    <% list_values = "" %>

    % if value and  len(value) > 0:
        <% list_values = ", ".join(["%s" % v for v in value]) %>
    % endif
    
    ${h.hidden(c.p.get_value(id, "name"), list_values, id=c.p.get_value(id, "id") + '-list-textbox')}
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
    
    param_name = id.replace('-', ' ')
    param_value = param_value or c.share.get(param_name) or ""
    
    help(id, c.p.get_value(id, "disabled"))
    
    if c.p.get_value(id, "disabled") == True:
        disabled(id)

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

<%def name="write(share='')">
<%

    
    
    

%>

    ${h.form('', method="post", id="share-form", class_="share-configuration")}
        <ol class="tab-list">
	    <li id="tab1" class="active">
		<h3><a title="${_('Basic Share Configuration')}" class="title-icon basic-tab" href="#">${_('Basic')}</a></h3>                           
	    </li>
	    
	    <li id="tab2">
		<h3><a title="${_('Advanced Permissions for this Share')}" class="title-icon permissions-tab" href="#">${_('Permissions')}</a></h3>                       
	    </li>
	    
	    <li id="tab3">
		<h3><a title="${_('Share User Management')}" class="title-icon users-tab" href="#">${_('Users')}</a></h3>
	    </li>
	    
	    <li id="tab4">
		<h3><a title="${_('Share Host Management')}" class="title-icon hosts-tab" href="#">${_('Hosts')}</a></h3>
	    </li>                        
	</ol>
        
        <ul class="tab-list-items"> 
	    <li id="content-tab1" class="active tab">
		<ol class="col-1">
		    <li>${put("name", c.share.get_share_name())}</li>
		    <li>${put("path")}</li>
		</ol>
		
		<ol class="col-2" style="overflow:auto;">
		    <li>${put("guest-ok")}</li>
		    <li>${put("browsable")}</li>
		    <li>${put("read-only")}</li>
                    <li>${put("guest-only")}</li>
		</ol>
	    </li>
	    
	    <li id="content-tab2">                            
		<ol class="col-1">
		    <li>${put("create-mask")}</li>
                    <li>${put("directory-mask")}</li>
		</ol>                            
	    </li>
	    
	    <li id="content-tab3">
		<ol class="col-1">
		    <li>${put("read-list")}</li>
		    <li>${put("write-list")}</li>
		    <li>${put("admin-list")}</li>
		</ol>                            
	    </li>
	    
	    <li id="content-tab4">
                <ol class="col-1">
                    <li>${put("hosts-allow")}</li>
                    <li>${put("hosts-deny")}</li>
                </ol>
	    </li>
	</ul>
	
	<div class="widget share-comment round-2px">
	    <div class="title-bar">
		<h2 class="title-icon" style="background-image:url('/default/images/icons/balloon.png');">${_('Comments')}</h2>
	    </div>
	    <div class="content">
		<textarea cols="80" rows="5" name="share_comment" id="share-comment">${c.share.get("comment")}</textarea>
	    </div>
	</div>
        
        <div>
            ${h.hidden("task", request.environ['pylons.routes_dict']['action'])}
            ${h.hidden("old_name", c.share.get_share_name())}
        </div>
        
    ${h.end_form()}
</%def>