<%doc>
#
# Navigation Mako Template file for SWAT
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

<%doc>Writes the Top menu for SWAT</%doc>
<%def name="top()"><%
    menu = h.MenuConfiguration("top")
    items = menu.get_items() %>

    % if len(items) > 0:
	<ul id="swat-top-nav" class="useful-links">
	    % for item in items:
		<li>
		    <%
		    
		    controller = menu.get_item_configuration(item, 'link/controller')
		    params = ""
		    
		    if len(menu.get_item_configuration(item, 'link/params/name')) > 0:
			params = "?name=" + request.environ['pylons.routes_dict']['controller']
		    
		    if len(menu.get_item_configuration(item, 'link/params/action')) > 0:
			params = params + "&action=" + request.environ['pylons.routes_dict']['action']

		    if controller == '_current_':
			controller = request.environ['pylons.routes_dict']['controller']
		    
		    %>
		    
		    <a href="${h.url_for(controller=controller, action=menu.get_item_configuration(item, 'link/action'))}${params}">
		        ${menu.get_item_configuration(item, 'link/name')}			
		    </a>
		</li>
	    % endfor
	</ul>
    % endif
</%def>

<%def name="breadcrumb()">
    <%
    
    items = c.breadcrumb.get()
    split = []
    
    %>
    
    % if len(items) > 0:
	<ul id="breadcrumb" class="breadcrumb-trail">
	    <% split = items[:len(items) - 1] %>

	    % for item in split:
		<% breadcrumb_item(item) %>
	    % endfor
	    
	    <% split = items[len(items) - 1] %>
	    <% breadcrumb_item(split, False) %>
	</ul>
    % endif
</%def>

<%def name="breadcrumb_item(item, with_link=True)">
    <li>
	&raquo;&nbsp;
	
	% if with_link == True:
	    <a href="${item['link']}">${item['name']}</a>
	% else:
	    ${item['name']}
	% endif

	&nbsp;
    </li>
</%def>