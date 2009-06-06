<%doc>Writes the Top menu for SWAT</%doc>
<%def name="top()">
    <% menu_items = h.get_menu("top") %>
    
    <ul id="swat-top-nav" class="useful-links">
	% for item in menu_items:
	    <li><a href="${item['link']}">${item['name']}</a></li>
	% endfor
    </ul>
</%def>