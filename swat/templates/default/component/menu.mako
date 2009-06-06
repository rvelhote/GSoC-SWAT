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
    <ul id="breadcrumb" class="breadcrumb-trail">
	<li>&raquo;&nbsp;Dashboard</li>
    </ul>
</%def>