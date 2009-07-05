<%def name="permission_zone(name, id)">
    <% permissions = [["0", _("None")], ["4", _("Read Only")], ["2", _("Write Only")], ["6", _("Read and Write")]]%>
    <% permissionGroups = [[_("Owner Can"), "owner", 6, 1], [_("Group Members Can"), "group", 4, 1], [_("Everyone Else Can"), "world", 4, 1]] %>
    
    <ul class="permissions-selection">
        % for grp in permissionGroups:
        
            <li>
                <label for="${id}-${grp[1]}-rw">${grp[0]}:</label>                                
                ${h.select(name + "_" + grp[1] + "_rw", grp[2], permissions, style="float:left;font-size:85%;", id=id + "-" + grp[1] + "-rw")}
    
                <span>
                    ${h.checkbox(name + "_" + grp[1] + '_x', grp[3], True, style="margin-left:15px;", id=id + "-" + grp[1] + '-x')}
                    <label class="checkbox" for="${id}-${grp[1]}-x">${_('Execute?')}</label>
                </span>
            </li>
        % endfor
    </ul>
</%def>

<%def name="write(share='')">

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
		    <li>
			<p class="option-help">${_('Set the Share Name')}</p>
			<label for="share-name" title="Set this Share's Name">${_('Name')}:</label>
                        ${h.text("share_name", share, id="share-name", class_='big-text')}
		    </li>
		    
		    <li>
                        <p class="option-help">${_("Sets the path to the directory provided by a file share or used by a printer share. Set automatically in [homes] share to user\'s home directory, otherwise defaults to  /tmp. Honors the %u (user) and %m (machine) variables.")}</p>
                        
			<span class="field-with-ops">
                            <label for="share-path" title="${_('Set the Path to be Shared')}">${_('Path')}:</label>
                            ${h.text("share_path", c.samba_lp.get("path", share), id="share-path", class_='big-text')}
			</span>

			<ol class="field-ops">
			    <li><a href="${h.url_for(controller='share', action='path')}" class="popup-selector" title="${_('Select the Share Location')}"><img src="/default/images/icons/layer-select-point.png" alt="${_('Add User/Group Icon')}" /></a></li>
			</ol>
		    </li>                                                                
		</ol>
		
		<ol class="col-2">
		    <li>
			<p class="option-help">${_('If checked, passwords are not needed for this share.')}</p>
                        ${h.checkbox('share_guestok', 1, c.samba_lp.get("guest ok", share), id='share-guest-ok', class_='big-margin')}
                        <label class="checkbox" for="share-guest-ok" title="${_('Check to make this Share Public')}">${_('Public?')}</label>                                    
		    </li>
		    
		    <li>
			<p class="option-help">${_('Allows a share to be announced in browse lists.')}</p>
                        ${h.checkbox('share_browsable', 1, c.samba_lp.get("browsable", share), id='share-browsable', class_='big-margin')}
			<label class="checkbox" for="share-browsable" title="${_('Check to make this share Browsable')}">${_('Browsable?')}</label>
		    </li>
		    
		    <li>
			<p class="option-help">${_('Sets a share to read-only.')}</p>
                        ${h.checkbox('share_readonly', 1, c.samba_lp.get("browsable", share), id='share-readonly', class_='big-margin')}
			<label class="checkbox" for="share-readonly" title="${_('Check to make this Share Read Only')}">${_('Read Only?')}</label>
		    </li>
                    
		    <li>
			<p class="option-help">${_('Forces user of a share to do so as the guest account')}</p>
                        ${h.checkbox('share_guestonly', 1, c.samba_lp.get("guest only", share), id='share-guestonly', class_='big-margin')}
			<label class="checkbox" for="share-guestonly" title="${_('Check to make this Guest Only')}">${_('Guest Only?')}</label>
		    </li>                    
		</ol>
		
		<div class="clear-both"></div>
	    </li>
	    
	    <li id="content-tab2">                            
		<ol class="col-1">
		    <li>                                    
			<p class="option-help">${_('Sets the maximum allowable permissions for new files (e.g., 0755). See also directory mask. To require certain permissions to be set, see force create mask/force directory mask.')}</p>
                        <p class="field-title">${_('Create Mask')}</p>
                        
                        ${permission_zone('create_mask', 'create-mask')}
		    </li>
		    
		    <li>                                    
			<p class="option-help">${_('Also called directory mode. Sets the maximum allowable permissions for newly created directories. To require certain permissions be set, see the force create mask and force directory mask options')}</p>
			<p class="field-title">${_('Directory Mask')}</p>
			
                        ${permission_zone('directory_mask', 'directory-mask')}
		    </li>                                
		</ol>                            
	    </li>
	    
	    <li id="content-tab3">
		<ol class="col-1">
		    <li>                                    
			<p class="option-help">${_('List of users that are given read-write access to a read-only share.')}</p>
			
			<span class="field-with-ops">
			    <label for="share-insert-writeuser" title="${_('Select Users/Groups that will have Read Access to this Share')}">${_('Read List')}:</label>
                            ${h.text("", "", id="share-insert-read-user", class_='big-text')}
			</span>

			<ol class="field-ops">
			    <li><a title="${_('Add this User/Group')}" href="#" onclick="userGroup.addManual('share-insert-read-user', 'user-list-read');return false;"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			    <li><a title="${_('Open User/Group Selection Popup')}" href="${h.url_for(controller='share', action='users_groups')}?copyto=user-list-read" class="popup-selector"><img src="/default/images/icons/users.png" alt="${_('Select Users/Groups Icon')}" /></a></li>
			</ol>
			
			<input type="hidden" name="share_read_list" />
			
			<ul id="user-list-read" class="user-list">
			</ul>
			
			<div class="clear-both"></div>
		    </li>                    
                    
		    <li>                                    
			<p class="option-help">${_('Specifies a list of users given read-only access to a writeable share.')}</p>
			
			<span class="field-with-ops">
			    <label for="share-insert-write-user" title="${_('Select Users/Groups that will have Write Access to this Share')}">${_('Write List')}:</label>
                            ${h.text("", "", id="share-insert-write-user", class_='big-text')}
			</span>

			<ol class="field-ops">
			    <li><a title="${_('Add this User/Group')}" href="#" onclick="userGroup.addManual('share-insert-write-user', 'user-list-write');return false;"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			    <li><a title="${_('Open User/Group Selection Popup')}" href="${h.url_for(controller='share', action='users_groups')}?copyto=user-list-write" class="popup-selector"><img src="/default/images/icons/users.png" alt="${_('Select Users/Groups Icon')}" /></a></li>
			</ol>
			
			<input type="hidden" name="share_write_list" />
			
			<ul id="user-list-write" class="user-list">
			</ul>
			
			<div class="clear-both"></div>
		    </li>
		    
                    <li>                                    
			<p class="option-help">${_('List of users who will be granted root permissions on the share by Samba.')}</p>
			
			<span class="field-with-ops">
			    <label for="share-insert-adminuser" title="${_('Select Users/Groups that will have Read Access to this Share')}">${_('Admin List')}:</label>
                            ${h.text("", "", id="share-insert-adminuser", class_='big-text')}
			</span>
			
			<ol class="field-ops">
                            <li><a title="${_('Add this User/Group')}" href="#" onclick="userGroup.addManual('share-insert-adminuser', 'user-list-admin');return false;"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			    <li><a title="${_('Open User/Group Selection Popup')}" href="${h.url_for(controller='share', action='users_groups')}?copyto=user-list-admin" class="popup-selector"><img src="/default/images/icons/users.png" alt="${_('Select Users/Groups Icon')}" /></a></li>
			</ol>
			
			<input type="hidden" name="share_admin_list" />
			
			<ul id="user-list-admin" class="user-list">
			</ul>
			
			<div class="clear-both"></div>
                    </li>
		</ol>                            
	    </li>
	    
	    <li id="content-tab4">
	    </li>
	</ul>
	
	<div class="widget share-comment round-2px">
	    <div class="title-bar">
		<h2 class="title-icon" style="background-image:url('/default/images/icons/balloon.png');">${_('Comments')}</h2>
	    </div>
	    <div class="content">
		<textarea cols="80" rows="5" name="share_notes" id="share-notes">${c.samba_lp.get("comment", share)}</textarea>
	    </div>
	</div>        
        
        
    ${h.end_form()}
</%def>