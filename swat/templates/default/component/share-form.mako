<%def name="write(share='')">
    <form class="create-form create-share" action="" method="post">
	<p class="dev-notes">some of this text is taken from the book "Using Samba". it serves just a filler for now. in the future there will be an option to remove the help items for more knowledgeable users :)</p>
	
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
	    <li id="content-tab1" class="active">
		<ol>
		    <li>
			<p class="option-help">${_('Set the Share Name')}</p>
			<label for="share-name" title="Set this Share's Name">${_('Name')}:</label>
			<input type="text" id="share-name" name="share_name" value="${share}" />                                                                        
		    </li>
		    
		    <li>
			<p class="option-help">${_("Sets the path to the directory provided by a file share or used by a printer share. Set automatically in [homes] share to user\'s home directory, otherwise defaults to  /tmp. Honors the %u (user) and %m (machine) variables.")}</p>
			<label for="share-path" title="${_('Set the Path to be Shares')}">${_('Path')}:</label>
			<input type="text" id="share-path" name="share_path" value="${c.samba_lp.get("path", share)}" />
		    </li>                                                                
		</ol>
		
		<ol class="col-2">
		    <li><%
		    
			checked = ""

			if c.samba_lp.get("guest ok", share):
			    checked = ' checked="checked" '
			
			%>
			<p class="option-help">${_('If checked, passwords are not needed for this share.')}</p>
			<input ${checked} type="checkbox" id="share-guest-ok" name="share_guestok" />
			<label class="checkbox" for="share-guest-ok" title="${_('Check to make this Share Public')}">${_('Public?')}</label>                                    
		    </li>
		    
		    <li><%
		    
			checked = ""

			if c.samba_lp.get("browsable", share):
			    checked = ' checked="checked" '
			
			%>
			<p class="option-help">${_('Allows a share to be announced in browse lists.')}</p>
			<input ${checked} type="checkbox" id="share-browsable" name="share_guestok" />
			<label class="checkbox" for="share-browsable" title="${_('Check to make this share Browsable')}">${_('Browsable?')}</label>
		    </li>
		    
		    <li><%
		    
			checked = ""

			if c.samba_lp.get("read only", share):
			    checked = ' checked="checked" '
			
			%>

			<p class="option-help">${_('Sets a share to read-only.')}</p>
			<input ${checked} type="checkbox" id="share-readonly" name="share_readonly" />
			<label class="checkbox" for="share-readonly" title="${_('Check to make this Share Read Only')}">${_('Read Only?')}</label>
		    </li>
		</ol>
		
		<div class="clear-both"></div>
	    </li>
	    
	    <li id="content-tab2">                            
		<ol>
		    <li>                                    
			<p class="option-help">${_('Sets the maximum allowable permissions for new files (e.g., 0755). See also directory mask. To require certain permissions to be set, see force create mask/force directory mask.')}</p>
			<label style="float:none;text-align:center;width:auto;margin-bottom:10px;" title="">${_('Create Mask')}</label>
			
			<table class="chmod-permissions" summary="Permissions for Create Mask">
			    <thead>
				<tr>
				    <td></td>
				    <td>${_('User')}</td>
				    <td>${_('Group')}</td>
				    <td>${_('World')}</td>
				</tr>
			    </thead>
			    <tbody>  
				<tr>
				    <td class="thead">${_('Read')}</td>
				    <td><input checked="checked" type="checkbox" value="4" name="create_mask_ur"/></td>
				    <td><input checked="checked" type="checkbox" value="4" name="create_mask_gr"/></td>
				    <td><input checked="checked" type="checkbox" value="4" name="create_mask_wr"/></td>
				</tr>
				
				<tr>
				    <td class="thead">${_('Write')}</td>
				    <td><input checked="checked" type="checkbox" value="2" name="create_mask_uw"/></td>
				    <td><input type="checkbox" value="2" name="create_mask_gw"/></td>
				    <td><input type="checkbox" value="2" name="create_mask_ww"/></td>
				</tr>
				
				<tr>
				    <td class="thead">${_('Execute')}</td>
				    <td><input checked="checked" type="checkbox" value="1" name="create_mask_ux"/></td>
				    <td><input type="checkbox" value="1" name="create_mask_gx"/></td>
				    <td><input type="checkbox" value="1" name="create_mask_wx"/></td>
				</tr>
				
				<tr>
				    <td class="thead">${_('Permission')}</td>
				    <td><input type="text" readonly="readonly" size="1" name="create_mask_u" value="7"/></td>    
				    <td><input type="text" readonly="readonly" size="1" name="create_mask_g" value="4"/></td>
				    <td><input type="text" readonly="readonly" size="1" name="create_mask_w" value="4"/></td>
				</tr>           
			    </tbody>
			</table>
			
			<span style="display:block;text-align:center;margin-top:20px;">
			    <input style="margin-left:0;" type="checkbox" id="share-force-create-mask" name="share_forcecreatemask" />
			    <label class="checkbox" for="share-force-create-mask" title="${_('Check to Force the Create Mask')}">${_('Force Create Mask?')}</label>
			</span>
		    </li>
		    
		    <li>                                    
			<p class="option-help">Also called directory mode. Sets the maximum allowable permissions for newly created directories. To require certain permissions be set, see the force create mask and force directory mask options</p>
			<label style="float:none;text-align:center;width:auto;margin-bottom:10px;" title="">Directory Mask</label>
			
			<table class="chmod-permissions" summary="Permission for Directory Mask">
			    <thead>
				<tr>
				    <td></td>
				    <td>${_('User')}</td>
				    <td>${_('Group')}</td>
				    <td>${_('World')}</td>
				</tr>
			    </thead>
			    <tbody>  
				<tr>
				    <td class="thead">${_('Read')}</td>
				    <td><input type="checkbox" checked="checked" value="4" name="directory_mask_ur"/></td>
				    <td><input type="checkbox" checked="checked" value="4" name="directory_mask_gr"/></td>
				    <td><input type="checkbox" checked="checked" value="4" name="directory_mask_wr"/></td>
				</tr>
				
				<tr>
				    <td class="thead">${_('Write')}</td>
				    <td><input type="checkbox" checked="checked" value="2" name="directory_mask_uw"/></td>
				    <td><input type="checkbox" value="2" name="directory_mask_gw"/></td>
				    <td><input type="checkbox" value="2" name="directory_mask_ww"/></td>    
				</tr>
				
				<tr>
				    <td class="thead">${_('Execute')}</td>
				    <td><input type="checkbox" checked="checked" value="1" name="directory_mask_ux"/></td>
				    <td><input type="checkbox" checked="checked" value="1" name="directory_mask_gx"/></td>
				    <td><input type="checkbox" checked="checked" value="1" name="directory_mask_wx"/></td>
				</tr>
				
				<tr>
				    <td class="thead">${_('Permission')}</td>
				    <td><input type="text" readonly="readonly" size="1" name="directory_mask_u" value="7"/></td>    
				    <td><input type="text" readonly="readonly" size="1" name="directory_mask_g" value="5"/></td>
				    <td><input type="text" readonly="readonly" size="1" name="directory_mask_w" value="5"/></td>
				</tr>           
			    </tbody>
			</table>
			
			<span style="display:block;text-align:center;margin-top:20px;">
			    <input style="margin-left:0;" type="checkbox" id="share-force-directory-mask" name="share_forcedirectorymask" />
			    <label class="checkbox" for="share-force-directory-mask" title="${_('Check to Force the Directory Mask')}">${_('Force Directory Mask?')}</label>
			</span>                                    
		    </li>                                
		</ol>                            
	    </li>
	    
	    <li id="content-tab3">
		<ol>
		    <li>                                    
			<p class="option-help">${_('Specifies a list of users given read-only access to a writeable share.')}</p>
			
			<span class="floated-field">
			    <label for="share-insert-user" title="${_('Select Users/Groups that will have Read Access to this Share')}">${_('Read List')}:</label>
			    <input type="text" name="add_new_read_user" id="share-insert-user" />
			</span>

			<ol class="user-list-operations">
			    <li><a title="${_('Add this User/Group')}" href="#"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			    <li><a title="${_('Open User/Group Selection Popup')}" href="#"><img src="/default/images/icons/users.png" alt="${_('Select Users/Groups Icon')}" /></a></li>
			</ol>
			
			<input type="hidden" name="share_read_list" />
			
			<ul class="user-list">
			    <li><a id="delete-read-list-1" title="${_('Remove this User/Group')}" href="#"><span>@vandelay</span><img src="/default/images/icons/minus-small.png" alt="${_('Remove User/Group Icon')}" /></a></li>
			    <li><a id="delete-read-list-2" title="${_('Remove this User/Group')}" href="#"><span>art.vandelay</span><img src="/default/images/icons/minus-small.png" alt="${_('Remove User/Group Icon')}" /></a></li>
			    <li><a id="delete-read-list-3" title="${_('Remove this User/Group')}" href="#"><span>@board</span><img src="/default/images/icons/minus-small.png" alt="${_('Remove User/Group Icon')}" /></a></li>
			    <li><a id="delete-read-list-4" title="${_('Remove this User/Group')}" href="#"><span>crusader</span><img src="/default/images/icons/minus-small.png" alt="${_('Remove User/Group Icon')}" /></a></li>
			</ul>
			
			<div class="clear-both"></div>
		    </li>
		    
		    <li>                                    
			<p class="option-help">${_('List of users who will be granted root permissions on the share by Samba.')}</p>
			
			<span class="floated-field">
			    <label for="share-insert-adminuser" title="${_('Select Users/Groups that will have Read Access to this Share')}">${_('Admin List')}:</label>
			    <input type="text" name="add_new_admin_user" id="share-insert-adminuser" />
			</span>
			
			<ol class="user-list-operations">
			    <li><a title="${_('Add this User/Group')}" href="#"><img src="/default/images/icons/plus-small.png" alt="${_('Add User/Group Icon')}" /></a></li>
			    <li><a title="${_('Open User/Group Selection Popup')}" href="#"><img src="/default/images/icons/users.png" alt="${_('Select Users/Groups Icon')}" /></a></li>
			</ol>
			
			<input type="hidden" name="share_admin_list" />
			
			<ul class="user-list">                                        
			    <li><a title="${_('Remove this User/Group')}" href="#"><span>@board</span><img src="/default/images/icons/minus-small.png" alt="${_('Remove User/Group Icon')}" /></a></li>
			</ul>
			
			<div class="clear-both"></div>
		    </li>                                
		</ol>                            
	    </li>
	    
	    <li id="content-tab4">
		<p class="dev-notes">here, the user will be able to configure the 'allow/deny hosts' options</p>
	    </li>                        
	</ul>
	
	<div class="widget share-notes round-2px" style="margin-top:15px;">                    
	    <div class="title-bar">
		<h2 class="title-icon" style="background-image:url('/default/images/icons/balloon.png');">${_('Comments')}</h2>
	    </div>
	    <div class="content">
		<textarea cols="80" rows="5" name="share_notes" id="share-notes">${c.samba_lp.get("comment", share)}</textarea>
	    </div>
	</div>  
    </form>
</%def>