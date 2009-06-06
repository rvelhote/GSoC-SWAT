<%def name="top()">

    <% menu_items = h.get_top_menu_items() %>
    
    <ul id="swat-top-nav" class="useful-links">
	% for item in menu_items:
	    <li><a href="${item['link']}">${item['name']}</a></li>
	% endfor
    </ul>
</%def>