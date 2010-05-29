<%doc>
#
# Dashboard Mako Template file for SWAT
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
<%inherit file="/default/base/base.mako" />

${build_dashboard(c.dash)}

<%doc>Specific Page title for the Dashboard Template</%doc>
<%def name="page_title()">
    ${parent.page_title()}
    ::
    ${c.config.get_action_info('friendly_name')}
</%def>

<%doc>Build the Dashboard Layout. Takes a parameter containing the layout
information (DashboardConfiguration object)</%doc>
<%def name="build_dashboard(dashboard)">
    % for row in dashboard.get_layout():
	<div class="dashboard-row col${row['display']}">
	    % for name in row['names']:
		<% item = dashboard.get_item(name) %>
                
                % if item is not None and len(item.get_dashboard_items()) > 0:
                    <% write_widget(item) %>
                % endif
	    % endfor
            
            <div class="clear-both"></div>
	</div>
    % endfor
</%def>

<%doc>Writes the Controller's Widget data i.e. the actions it will perform
and the title bar.</%doc>
<%def name="write_widget(item)">
    <div class="widget round-2px">
        
        <div class="title-bar">
            <% link = h.url_for(controller = item.get_controller(), action = item.get_dashboard_info('link/action')) %>
	    <h2 class="title-icon" style="background-image:url('/default/images/icons/${item.get_dashboard_info('image/name')}')"><a href="${link}" title="${item.get_dashboard_info('link/title')}">${item.get_dashboard_info('link/name')}</a></h2>

	    <ul>                                
		<li><a href="${link}" title="${item.get_dashboard_info('link/title')}"><img src="/default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>                                
	    </ul>
	</div>
        
        <div class="content">
            <ul class="widget-task-list">
                <% actions = item.get_dashboard_items() %>
        
                % for action in actions:
                    % if len(item.get_action_info('link/subaction', action)) > 0:
                        <% link = h.url_for("with_subaction", controller = item.get_controller(), action = item.get_action_info('link/action', action), subaction = item.get_action_info('link/subaction', action)) %>
                    % else:
                        <% link = h.url_for(controller = item.get_controller(), action = action) %>
                    % endif
                                        
                    <li>
                        <a href="${link}" title="${item.get_action_info('link/title', action)}" class="item-icon-link">
                            <img src="/default/images/icons/${item.get_action_info('image/name', action)}" alt="${item.get_action_info('image/alt', action)}" />
                            <span>${item.get_action_info('link/name', action)}</span>
                        </a>
                    </li>
                % endfor
            </ul>
            <div class="clear-both"></div>
        </div>
    </div>
</%def>