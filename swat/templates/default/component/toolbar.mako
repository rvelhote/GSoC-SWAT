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
<%def name="write(toolbar)">
    <div id="task-toolbar">
	<ul class="task-toolbar">
	    % if len(toolbar) > 0:
		% for action in toolbar:
		    <% write_item(action) %>
		% endfor
	    % endif
	</ul>
	
	<div class="clear-both"></div>
    </div>
</%def>
    
<%def name="write_item(action)">
    <%
    
    if len(c.config.get_action_info('link/subaction', action)) > 0:
	link = h.url_for(controller = c.config.get_controller(), action = c.config.get_action_info('link/action', action), subaction = c.config.get_action_info('link/subaction', action))
    else:
	link = h.url_for(controller = c.config.get_controller(), action = c.config.get_action_info('link/action', action))
	
    submit = ''
    mass_submit = ''
    confirmation = ''

    if c.config.get_action_info('link/submit', action):
	submit = ' form-submit-button '
	
    if c.config.get_action_info('link/mass_submit', action):
	mass_submit = ' form-mass-submit-buttton '
	
    if c.config.get_action_info('link/require_confirm', action):
	confirmation = ' form-require-confirm '
    
    %>
    
    <li>
	% if len(confirmation) > 0:
	    ${h.hidden("", c.config.get_action_info('link/confirm_message', action), id="confirm-action-" + action)}
	% endif
	
	<a id="action-${action}" class="item-icon-link ${submit} ${mass_submit} ${confirmation}" title="${c.config.get_action_info('link/title', action)}" href="${link}">
	    <img alt="${c.config.get_action_info('image/alt', action)}" src="/default/images/icons/${c.config.get_action_info('image/name', action)}"/>
	    <span>${c.config.get_action_info('link/name', action)}</span>
	</a>
    </li>
</%def>
