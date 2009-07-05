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

${build_dashboard(c.dashboard_config)}

<%doc>Specific Page title for the Dashboard Template</%doc>
<%def name="page_title()">
    ${parent.page_title()}
    ::
    ${c.controller_config.get_action_info('friendly_name')}
</%def>

<%doc>Build the Dashboard Layout. Takes a parameter containing the layout
information (DashboardConfiguration object)</%doc>
<%def name="build_dashboard(dashboard)">
    % for row in dashboard.get_layout():
	<div class="dashboard-row col${row['display']}">
	    % for name in row['names']:
		<% items = dashboard.get_item(name).get_dashboard_items() %>

		% if len(items) > 0:
		    <% write_widget(name, items) %>
		% endif
	    % endfor
	</div>
    % endfor
</%def>

<%doc>Writes the Controller's Widget data i.e. the actions it will perform
and the title bar.</%doc>
<%def name="write_widget(name, controller)"><%

    link = h.url_for(controller = name, action = controller['title_bar']['link']['action']) %>

    <div class="widget round-2px">
	<div class="title-bar">
	    <h2 class="title-icon" style="background-image:url('/default/images/icons/${controller['title_bar']['image']['name']}')"><a href="${link}" title="${controller['title_bar']['link']['title']}">${controller['title_bar']['link']['name']}</a></h2>

	    <ul>                                
		<li><a href="${link}" title="${controller['title_bar']['link']['title']}"><img src="/default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>                                
	    </ul>
	</div>

	<div class="content">
	    <ul class="widget-task-list">
		% for action in controller['actions'].values():
                    <% link =  h.url_for(controller = name, action = action['link']['action']) %>
                    
		    <li>
			<a href="${link}" title="${action['link']['title']}" class="item-icon-link">
			    <img src="/default/images/icons/${action['image']['name']}" alt="${action['image']['alt']}" />
			    <span>${action['link']['name']}</span>
			</a>
		    </li>
		% endfor
	    </ul>
	    
	    <div class="clear-both"></div>
	</div>
    </div>
</%def>