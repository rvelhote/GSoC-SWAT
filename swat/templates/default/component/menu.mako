<%doc>Writes the Top menu for SWAT</%doc>
<%def name="top()">
    <% menu_items = h.get_menu("top") %>
    
    % if menu_items is not None and len(menu_items) > 0:
	<ul id="swat-top-nav" class="useful-links">
	    % for item in menu_items:
		<li><a href="${item['link']}">${item['name']}</a></li>
	    % endfor
	</ul>
    % endif
</%def>

<%def name="breadcrumb()">
    <%
    
    controller_name = request.environ['pylons.routes_dict']['controller']
    action_name = request.environ['pylons.routes_dict']['action']
    
    %>

    <ul id="breadcrumb" class="breadcrumb-trail">
	<li>
	    &raquo;&nbsp;

	    % if controller_name != "dashboard" or (controller_name == "dashboard" and action_name != 'index'):
		<a href="${h.url_for(controller = 'dashboard')}">Dashboard</a>
	    % else:
		Dashboard
	    % endif
	</li>
	
	% if controller_name != "dashboard" or (controller_name == "dashboard" and action_name != 'index'):
	
	    <li>
		&raquo;&nbsp;
		
		% if action_name != 'index' and len(action_name) > 0:
		    <a href="${h.url_for(controller = controller_name)}">
			% if hasattr(c, "friendly_controller"):
			    ${c.friendly_controller}
			% else:
			    ${controller_name}
			% endif
		    </a>
		% else:
		    % if hasattr(c, "friendly_controller"):
			${c.friendly_controller}
		    % else:
			${controller_name}
		    % endif
		% endif
	    </li>
	
	% endif
	
	% if action_name != "index":
	    <li>
		&raquo;&nbsp;
		
		% if hasattr(c, "friendly_action"):
		    ${c.friendly_action}
		% else:
		    ${action_name}
		% endif
	    </li>
	% endif
    </ul>
</%def>

