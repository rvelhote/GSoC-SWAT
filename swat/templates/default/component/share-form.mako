<%doc>
#
# Share Editing Form Mako Template file for SWAT
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

<%def name="to_list(s)">
    <%
    #
    # Classic returns a list and LDB returns the actual string so we need to
    # split it in different ways
    #
    if not c.share.is_classic():
        return s.split(",")
    
    return s

    %>
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
		    <li>${field.put("name", c.share.get_share_name())}</li>
		    <li>${field.put("path", c.share.get("path"))}</li>
		</ol>
		
		<ol class="col-2" style="overflow:auto;">
		    <li>${field.put("guest-ok", c.share.get("guest-ok"))}</li>
		    <li>${field.put("browsable", c.share.get("browsable"))}</li>
		    <li>${field.put("read-only", c.share.get("read-only"))}</li>
                    <li>${field.put("guest-only", c.share.get("guest-only"))}</li>
		</ol>
	    </li>
	    
	    <li id="content-tab2">                            
		<ol class="col-1">
		    <li>${field.put("create-mask", c.share.get("create-mask"))}</li>
                    <li>${field.put("directory-mask", c.share.get("directory-mask"))}</li>
		</ol>                            
	    </li>
	    
	    <li id="content-tab3">
		<ol class="col-1">
		    <li>${field.put("read-list", to_list(c.share.get("read-list")))}</li>
		    <li>${field.put("write-list", to_list(c.share.get("write-list")))}</li>
		    <li>${field.put("admin-list", to_list(c.share.get("admin-list")))}</li>
		</ol>                            
	    </li>

	    <li id="content-tab4">
                <ol class="col-1">
                    <li>${field.put("hosts-allow", to_list(c.share.get("hosts-allow")))}</li>
                    <li>${field.put("hosts-deny", to_list(c.share.get("hosts-deny")))}</li>
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