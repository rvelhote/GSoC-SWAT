<%def name="write(share=[])">
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
			<p class="option-help">Set the Share Name</p>
			<label for="share-name" title="Set this Share's Name">Name:</label>
			<input type="text" id="share-name" name="share_name" />                                                                        
		    </li>
		    
		    <li>
			<p class="option-help">Sets the comment that appears beside a share in a NET VIEW or the details list of a Microsoft directory window. See also the server string configuration option.</p>                                    
			<label for="share-comment" title="Set this Share's Comment Value">Comment:</label>
			<input type="text" id="share-comment" name="share_comment" />
		    </li>
		    
		    <li>
			<p class="option-help">Sets the path to the directory provided by a file share or used by a printer share. Set automatically in [homes] share to user's home directory, otherwise defaults to  /tmp. Honors the %u (user) and %m (machine) variables.</p>                                    
			<label for="share-path" title="Set the Path to be Shares">Path:</label>
			<input type="text" id="share-path" name="share_path" />
		    </li>                                                                
		</ol>
		
		<ol class="col-2">
		    <li>
			<p class="option-help">If checked, passwords are not needed for this share.</p>
			<input type="checkbox" id="share-guest-ok" name="share_guestok" />
			<label class="checkbox" for="share-guest-ok" title="Check to make this share">Public?</label>                                    
		    </li>
		    
		    <li>
			<p class="option-help">Allows a share to be announced in browse lists.</p>
			<input type="checkbox" id="share-browsable" name="share_guestok" />
			<label class="checkbox" for="share-browsable" title="Check to make this share Browsable">Browsable?</label>
		    </li>
		    
		    <li>
			<p class="option-help">Sets a share to read-only.</p>
			<input type="checkbox" id="share-readonly" name="share_readonly" />
			<label class="checkbox" for="share-readonly" title="Check to make this share Read Only">Read Only?</label>
		    </li>
		    
		    <li>
			<p class="option-help">Sets a share to be a print share. Required for all printers.</p>
			<input type="checkbox" id="share-printable" name="share_printable" />
			<label class="checkbox" for="share-printable" title="Check to make this share Printable">Printable?</label>
		    </li>
		</ol>
		
		<div class="clear-both"></div>
	    </li>
	    
	    <li id="content-tab2">                            
		<ol>
		    <li>                                    
			<p class="option-help">Sets the maximum allowable permissions for new files (e.g., 0755). See also directory mask. To require certain permissions to be set, see force create mask/force directory mask.</p>                                    
			<label style="float:none;text-align:center;width:auto;margin-bottom:10px;" title="">Create Mask</label>
			
			<table class="chmod-permissions" summary="Permissions for Create Mask">
			    <thead>
				<tr>
				    <td></td>
				    <td>User</td>
				    <td>Group</td>
				    <td>World</td>
				</tr>
			    </thead>
			    <tbody>  
				<tr>
				    <td class="thead">Read</td>
				    <td><input checked="checked" type="checkbox" value="4" name="create_mask_ur"/></td>
				    <td><input checked="checked" type="checkbox" value="4" name="create_mask_gr"/></td>
				    <td><input checked="checked" type="checkbox" value="4" name="create_mask_wr"/></td>
				</tr>
				
				<tr>
				    <td class="thead">Write</td>
				    <td><input checked="checked" type="checkbox" value="2" name="create_mask_uw"/></td>
				    <td><input type="checkbox" value="2" name="create_mask_gw"/></td>
				    <td><input type="checkbox" value="2" name="create_mask_ww"/></td>
				</tr>
				
				<tr>
				    <td class="thead">Execute</td>
				    <td><input checked="checked" type="checkbox" value="1" name="create_mask_ux"/></td>
				    <td><input type="checkbox" value="1" name="create_mask_gx"/></td>
				    <td><input type="checkbox" value="1" name="create_mask_wx"/></td>
				</tr>
				
				<tr>
				    <td class="thead">Permission</td>
				    <td><input type="text" readonly="readonly" size="1" name="create_mask_u" value="7"/></td>    
				    <td><input type="text" readonly="readonly" size="1" name="create_mask_g" value="4"/></td>
				    <td><input type="text" readonly="readonly" size="1" name="create_mask_w" value="4"/></td>
				</tr>           
			    </tbody>
			</table>
			
			<span style="display:block;text-align:center;margin-top:20px;">
			    <input style="margin-left:0;" type="checkbox" id="share-force-create-mask" name="share_forcecreatemask" />
			    <label class="checkbox" for="share-force-create-mask" title="Check to Force the Create Mask">Force Create Mask?</label>
			</span>
		    </li>
		    
		    <li>                                    
			<p class="option-help">Also called directory mode. Sets the maximum allowable permissions for newly created directories. To require certain permissions be set, see the force create mask and force directory mask options</p>
			<label style="float:none;text-align:center;width:auto;margin-bottom:10px;" title="">Directory Mask</label>
			
			<table class="chmod-permissions" summary="Permission for Directory Mask">
			    <thead>
				<tr>
				    <td></td>
				    <td>User</td>
				    <td>Group</td>
				    <td>World</td>
				</tr>
			    </thead>
			    <tbody>  
				<tr>
				    <td class="thead">Read</td>
				    <td><input type="checkbox" checked="checked" value="4" name="directory_mask_ur"/></td>
				    <td><input type="checkbox" checked="checked" value="4" name="directory_mask_gr"/></td>
				    <td><input type="checkbox" checked="checked" value="4" name="directory_mask_wr"/></td>
				</tr>
				
				<tr>
				    <td class="thead">Write</td>
				    <td><input type="checkbox" checked="checked" value="2" name="directory_mask_uw"/></td>
				    <td><input type="checkbox" value="2" name="directory_mask_gw"/></td>
				    <td><input type="checkbox" value="2" name="directory_mask_ww"/></td>    
				</tr>
				
				<tr>
				    <td class="thead">Execute</td>
				    <td><input type="checkbox" checked="checked" value="1" name="directory_mask_ux"/></td>
				    <td><input type="checkbox" checked="checked" value="1" name="directory_mask_gx"/></td>
				    <td><input type="checkbox" checked="checked" value="1" name="directory_mask_wx"/></td>
				</tr>
				
				<tr>
				    <td class="thead">Permission</td>
				    <td><input type="text" readonly="readonly" size="1" name="directory_mask_u" value="7"/></td>    
				    <td><input type="text" readonly="readonly" size="1" name="directory_mask_g" value="5"/></td>
				    <td><input type="text" readonly="readonly" size="1" name="directory_mask_w" value="5"/></td>
				</tr>           
			    </tbody>
			</table>
			
			<span style="display:block;text-align:center;margin-top:20px;">
			    <input style="margin-left:0;" type="checkbox" id="share-force-directory-mask" name="share_forcedirectorymask" />
			    <label class="checkbox" for="share-force-directory-mask" title="Check to Force the Directory Mask">Force Directory Mask?</label>
			</span>                                    
		    </li>                                
		</ol>                            
	    </li>
	    
	    <li id="content-tab3">
		<ol>
		    <li>                                    
			<p class="option-help">Specifies a list of users given read-only access to a writeable share. </p>
			
			<span class="floated-field">
			    <label for="share-insert-user" title="Select Users/Groups that will have Read Access to this Share">Read List:</label>
			    <input type="text" name="add_new_read_user" id="share-insert-user" />
			</span>

			<ol class="user-list-operations">
			    <li><a title="Add this User/Group" href="#"><img src="images/icons/plus-small.png" alt="Add User/Group Icon" /></a></li>
			    <li><a title="Open User/Group Selection Popup" href="#"><img src="images/icons/users.png" alt="Select Users/Groups Icon" /></a></li>
			</ol>
			
			<input type="hidden" name="share_read_list" />
			
			<ul class="user-list">
			    <li><a id="delete-read-list-1" title="Remove this User/Group" href="#"><span>@vandelay</span><img src="images/icons/minus-small.png" alt="Remove User/Group Icon" /></a></li>
			    <li><a id="delete-read-list-2" title="Remove this User/Group" href="#"><span>art.vandelay</span><img src="images/icons/minus-small.png" alt="Remove User/Group Icon" /></a></li>
			    <li><a id="delete-read-list-3" title="Remove this User/Group" href="#"><span>@board</span><img src="images/icons/minus-small.png" alt="Remove User/Group Icon" /></a></li>
			    <li><a id="delete-read-list-4" title="Remove this User/Group" href="#"><span>crusader</span><img src="images/icons/minus-small.png" alt="Remove User/Group Icon" /></a></li>
			</ul>
			
			<div class="clear-both"></div>
		    </li>
		    
		    <li>                                    
			<p class="option-help">List of users who will be granted root permissions on the share by Samba.</p>
			
			<span class="floated-field">
			    <label for="share-insert-adminuser" title="Select Users/Groups that will have Read Access to this Share">Admin List:</label>
			    <input type="text" name="add_new_admin_user" id="share-insert-adminuser" />
			</span>
			
			<ol class="user-list-operations">
			    <li><a title="Add this User/Group" href="#"><img src="images/icons/plus-small.png" alt="Add User/Group Icon" /></a></li>
			    <li><a title="Open User/Group Selection Popup" href="#"><img src="images/icons/users.png" alt="Select Users/Groups Icon" /></a></li>
			</ol>
			
			<input type="hidden" name="share_admin_list" />
			
			<ul class="user-list">                                        
			    <li><a title="Remove this User/Group" href="#"><span>@board</span><img src="images/icons/minus-small.png" alt="Remove User/Group Icon" /></a></li>                                        
			</ul>
			
			<div class="clear-both"></div>
		    </li>                                
		</ol>                            
	    </li>
	    
	    <li id="content-tab4">
		<p class="dev-notes">here, the user will be able to configure the 'allow/deny hosts' options</p>
	    </li>                        
	</ul>
    </form>
</%def>