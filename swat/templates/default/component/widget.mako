<%def name="get_all(area)">

    <% layout = h.get_widget_area_configuration(area) %>
    
    % for configuration in layout:
	<div class="dashboard-row col${configuration['display']}">
	    
	    % for name in configuration['names']:
	    
		<% controller_config = h.get_widget_configuration(name) %>
		
		% if controller_config != None:
	    
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
		
		% endif
		
	    % endfor
	</div>
    % endfor
</%def>
