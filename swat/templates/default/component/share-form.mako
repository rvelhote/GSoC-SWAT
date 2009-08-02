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
    ${h.hidden(c.p.get_value(id, "name"), 'no')}
    ${h.checkbox(c.p.get_value(id, "name"), 'yes', value, id=c.p.get_value(id, "id"), class_=c.p.get_value(id, "class"))}
    <label class="checkbox" for="${c.p.get_value(id, "id")}" title="${c.p.get_value(id, "title")}">${c.p.get_value(id, "label")}</label>                                    
</%def>
    
<%doc></%doc>
<%def name="permissions(id, value)">
    <p class="field-title">${c.p.get_value(id, "title")}</p>
    <% value = oct(value) %>

    <% permissions = [["0", _("Do Nothing")], ["4", _("Read Only")], ["2", _("Write Only")], ["6", _("Read and Write")], ["5", _("Read and Execute")], ["7", _("Read, Write and Execute")]]%>
    <% permissionGroups = [[_("Owner Can"), "owner", 6, 1], [_("Group Members Can"), "group", 4, 1], [_("Everyone Else Can"), "world", 4, 1]] %>
    <% name = c.p.get_value(id, 'permissions-name') %>
    
    <ul class="permissions-selection">
        <% i = 1 %>
        
        % for grp in permissionGroups:
            <li>
                <label for="${id}-${grp[1]}">${grp[0]}:</label>                                
                ${h.select(name + "_" + grp[1], value[i], permissions, style="float:left;font-size:85%;", id=id + "-" + grp[1], onchange='calcPermissions("' + id + '", "' + id + '");')}
            </li>
            <% i = i + 1 %>
        % endfor
    </ul>

    ${h.hidden(c.p.get_value(id, 'name'), value, id=id)}
</%def>
    
<%def name="path_selector(id, op)">
    <a href="${h.url_for(controller=c.p.get_value(id, 'field-ops-descriptor/' + op + '/link/controller'), action=c.p.get_value(id, 'field-ops-descriptor/' + op + '/link/action'))}?copyto=${c.p.get_value(id, 'id')}" class="popup-selector" title="${c.p.get_value(id, 'field-ops-descriptor/' + op + '/title')}"><img src="/default/images/icons/${c.p.get_value(id, 'field-ops-descriptor/' + op + '/image/name')}" alt="${c.p.get_value(id, 'field-ops-descriptor/' + op + '/image/alt')}" /></a>
</%def>
    
<%def name="field_ops(id, ops)">
    % if ops != "":
        <ol class="field-ops">
            % for op in ops:
                <li>
                    % if op == "path-selection":
                        <% path_selector(id, op) %>
                    % endif
                </li>
            % endfor
        </ol>
    % endif
</%def>
    
<%doc>Choose which type to call</%doc>
<%def name="put(id, param_value=None)">
    <%
    type = c.p.get_value(id, "type")
    
    param_name = id.replace('-', ' ')
    param_value = param_value or c.samba_lp.get(param_name, c.share_name)
    
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
		    <li>${put("name", c.share_name)}</li>
		    <li>${put("path")}</li>
		</ol>
		
		<ol class="col-2">
		    <li>${put("guest-ok")}</li>
		    <li>${put("browsable")}</li>
		    <li>${put("read-only")}</li>
                    <li>${put("guest-only")}</li>
		</ol>
		
		<div class="clear-both"></div>
	    </li>
	    
	    <li id="content-tab2">                            
		<ol class="col-1">
		    <li>${put("create-mask")}</li>
                    <li>${put("directory-mask")}</li>
		</ol>                            
	    </li>
	    
	    <li id="content-tab3">
		<ol class="col-1">
		    <li>                                    
			<p class="option-help">${_('List of users that are given read-write access to a read-only share.')}</p>
			
			<span class="field-wrapper">
			    <label for="share-insert-read-user" title="${_('Select Users/Groups that will have Read Access to this Share')}">${_('Read List')}:</label>
                            ${h.text("", "", id="share-insert-read-user", class_='big-text')}
			</span>

			<ol class="field-ops">
			    <li><a title="${_('Add this User/Group')}" href="#" onclick="userGroup.addManual('share-insert-read-user', 'user-list-read');return false;"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			    <li><a title="${_('Open User/Group Selection Popup')}" href="${h.url_for(controller='share', action='users_groups')}?copyto=user-list-read" class="popup-selector"><img src="/default/images/icons/users.png" alt="${_('Select Users/Groups Icon')}" /></a></li>
			</ol>
			
                        ${h.hidden('share_read_list', c.samba_lp.get("read list", share), id='user-list-read-textbox')}

			<ul id="user-list-read" class="user-list">
			</ul>
			
			<div class="clear-both"></div>
		    </li>                    
                    
		    <li>                                    
			<p class="option-help">${_('Specifies a list of users given read-only access to a writeable share.')}</p>
			
			<span class="field-wrapper">
			    <label for="share-insert-write-user" title="${_('Select Users/Groups that will have Write Access to this Share')}">${_('Write List')}:</label>
                            ${h.text("", "", id="share-insert-write-user", class_='big-text')}
			</span>

			<ol class="field-ops">
			    <li><a title="${_('Add this User/Group')}" href="#" onclick="userGroup.addManual('share-insert-write-user', 'user-list-write');return false;"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			    <li><a title="${_('Open User/Group Selection Popup')}" href="${h.url_for(controller='share', action='users_groups')}?copyto=user-list-write" class="popup-selector"><img src="/default/images/icons/users.png" alt="${_('Select Users/Groups Icon')}" /></a></li>
			</ol>
			
                        ${h.hidden('share_write_list', c.samba_lp.get("write list", share), id='user-list-write-textbox')}
			
			<ul id="user-list-write" class="user-list">
			</ul>
			
			<div class="clear-both"></div>
		    </li>
		    
                    <li>                                    
			<p class="option-help">${_('List of users who will be granted root permissions on the share by Samba.')}</p>
			
			<span class="field-wrapper">
			    <label for="share-insert-adminuser" title="${_('Select Users/Groups that will have Read Access to this Share')}">${_('Admin List')}:</label>
                            ${h.text("", "", id="share-insert-adminuser", class_='big-text')}
			</span>
			
			<ol class="field-ops">
                            <li><a title="${_('Add this User/Group')}" href="#" onclick="userGroup.addManual('share-insert-adminuser', 'user-list-admin');return false;"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			    <li><a title="${_('Open User/Group Selection Popup')}" href="${h.url_for(controller='share', action='users_groups')}?copyto=user-list-admin" class="popup-selector"><img src="/default/images/icons/users.png" alt="${_('Select Users/Groups Icon')}" /></a></li>
			</ol>

                        ${h.hidden('share_admin_list', c.samba_lp.get("admin list", share), id='user-list-admin-textbox')}
			
			<ul id="user-list-admin" class="user-list">
			</ul>
			
			<div class="clear-both"></div>
                    </li>
		</ol>                            
	    </li>
	    
	    <li id="content-tab4">
                <ol class="col-1">
                    <li>
			<p class="option-help">${_('A list of machines that can access a share or shares. If NULL (the default) any machine can access the share unless there is a hosts deny option.')}</p>
			
			<span class="field-wrapper">
			    <label for="share-insert-allowed-hosts" title="${_('List of Hostnames that will be able to access this Share')}">${_('Allowed Hosts')}:</label>
                            ${h.text("", "", id="share-insert-allowed-hosts", class_='big-text')}
			</span>
			
			<ol class="field-ops">
                            <li><a title="${_('Add this Host')}" href="#" onclick="userGroup.addManual('share-insert-allowed-hosts', 'allowed-hosts-list');return false;"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			</ol>
                        
                        <%
                        
                        hosts_allow = ""
                        if c.samba_lp.get("hosts allow", share) and  len(c.samba_lp.get("hosts allow", share)) > 0:
                            hosts_allow = ", ".join(["%s" % value for value in c.samba_lp.get("hosts allow", share)])
                        
                        %>
			
                        ${h.hidden('share_hosts_allow', hosts_allow, id='allowed-hosts-list-textbox')}
			
			<ul id="allowed-hosts-list" class="user-list">
                            % if  c.samba_lp.get("hosts allow", share):
                                <% i = 1 %>
                                % for host in c.samba_lp.get("hosts allow", share):
                                    <li>
                                        <a class="delete-link" id="delete-allowed-hosts-list-${i}" title="Remove this item from the list" href="#">${host}</a>
                                    </li>
                                    
                                    <% i = i + 1 %>
                                % endfor
                            % endif
			</ul>
			
			<div class="clear-both"></div>
                    </li>
                    
                    <li>
			<p class="option-help">${_('A list of machines that cannot connect to a share or shares. ')}</p>
			
			<span class="field-wrapper">
			    <label for="share-insert-deny-hosts" title="${_('List of Hostnames that will not be able to access this Share')}">${_('Denied Hosts')}:</label>
                            ${h.text("", "", id="share-insert-deny-hosts", class_='big-text')}
			</span>
			
			<ol class="field-ops">
                            <li><a title="${_('Add this Host')}" href="#" onclick="userGroup.addManual('share-insert-deny-hosts', 'denied-hosts-list');return false;"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			</ol>

                        <%
                        
                        hosts_deny = ""
                        if c.samba_lp.get("hosts deny", share) and len(c.samba_lp.get("hosts deny", share)) > 0:
                            hosts_deny = ", ".join(["%s" % value for value in c.samba_lp.get("hosts deny", share)])
                        
                        %>

                        ${h.hidden('share_hosts_deny', hosts_deny, id='denied-hosts-list-textbox')}
			
			<ul id="denied-hosts-list" class="user-list">
                            % if  c.samba_lp.get("hosts deny", share):
                                <% i = 1 %>
                                % for host in c.samba_lp.get("hosts deny", share):
                                    <li>
                                        <a class="delete-link" id="delete-denied-hosts-list-${i}" title="Remove this item from the list" href="#">${host}</a>
                                    </li>
                                    
                                    <% i = i + 1 %>
                                % endfor
                            % endif
			</ul>
			
			<div class="clear-both"></div>
                    </li>
                </ol>
	    </li>
	</ul>
	
	<div class="widget share-comment round-2px">
	    <div class="title-bar">
		<h2 class="title-icon" style="background-image:url('/default/images/icons/balloon.png');">${_('Comments')}</h2>
	    </div>
	    <div class="content">
		<textarea cols="80" rows="5" name="share_comment" id="share-comment">${c.samba_lp.get("comment", share)}</textarea>
	    </div>
	</div>
        
        <div>
            ${h.hidden("task", request.environ['pylons.routes_dict']['action'])}
            ${h.hidden("old_name", share)}
        </div>
        
    ${h.end_form()}
</%def>