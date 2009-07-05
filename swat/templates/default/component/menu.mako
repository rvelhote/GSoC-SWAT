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
<%def name="top()">
    <% menu_items = h.get_menu("top") %>

    % if len(menu_items) > 0:
	<ul id="swat-top-nav" class="useful-links">
	    % for item in menu_items.values():
		<li>
		
		    % if item['link']['controller'] == '_current_':
			<% item['link']['controller'] = request.environ['pylons.routes_dict']['controller'] %>
		    % endif
		    
		    <a href="${h.url_for(controller=item['link']['controller'], action=item['link']['action'])}">
		        ${item['link']['name']}
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