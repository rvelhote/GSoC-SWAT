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