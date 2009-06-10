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
		<% item_list = dashboard.get_item(name).get_dashboard_items() %>

		% if len(item_list) > 0:
		    <% write_widget(item_list) %>
		% endif
	    % endfor
	</div>
    % endfor    
</%def>

<%doc>Writes the Controller's Widget data i.e. the actions it will perform
and the title bar.</%doc>
<%def name="write_widget(controller)">
    <div class="widget round-2px">
	<div class="title-bar">
	    <h2 class="title-icon" style="background-image:url('default/images/icons/${controller['title_bar']['title_icon']}')"><a href="${controller['title_bar']['title_link']}" title="${controller['title_bar']['title_link_title']}">${controller['title_bar']['title']}</a></h2>

	    <ul>                                
		<li><a href="${controller['title_bar']['title_link']}" title="${controller['title_bar']['title_link']}"><img src="default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>                                
	    </ul>
	</div>

	<div class="content">
	    <ul class="widget-task-list">
		% for action in controller['actions']:
		    <li>
			<a href="${action['link']}" title="${action['link_title']}" class="item-icon-link">
			    <img src="default/images/icons/${action['icon']}" alt="${action['icon_alt']}" />
			    <span>${action['title']}</span>
			</a>
		    </li>
		% endfor
	    </ul>
	    
	    <div class="clear-both"></div>
	</div>
    </div>
</%def>