<%doc>
#
# Toolbar Mako Template file for SWAT
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
<%def name="write(items)">
    <div id="task-toolbar">
	<ul class="task-toolbar">
	    % if len(items) > 0:	    
		% for item in items['actions']:
		    <% write_item(item) %>
		% endfor
	    % endif
	</ul>
	
	<div class="clear-both"></div>
    </div>
</%def>
    
<%def name="write_item(item)">
    <li>
	<a class="item-icon-link" title="${item['link_title']}" href="${item['link']}">
	    <img alt="${item['icon_alt']}" src="/default/images/icons/${item['icon']}"/>
	    <span>${item['title']}</span>
	</a>
    </li>
</%def>
