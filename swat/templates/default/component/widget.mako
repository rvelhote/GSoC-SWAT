<%def name="write_layout(dashboard)">
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
	
<%def name="write_widget(controller_config)">
    <div class="widget round-2px">
	<div class="title-bar">
	    <h2 class="title-icon" style="background-image:url('default/images/icons/${controller_config['title_bar']['title_icon']}')"><a href="${controller_config['title_bar']['title_link']}" title="${controller_config['title_bar']['title_link_title']}">${controller_config['title_bar']['title']}</a></h2>

	    <ul>                                
		<li><a href="${controller_config['title_bar']['title_link']}" title="${controller_config['title_bar']['title_link']}"><img src="default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>                                
	    </ul>
	</div>

	<div class="content">
	    <ul class="widget-task-list">
		% for action in controller_config['actions']:
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
