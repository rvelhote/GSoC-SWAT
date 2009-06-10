<%def name="write(controller, action='')">
    <div id="task-toolbar">
	<ul class="task-toolbar">
	    <% item_list = c.controller_config.get_toolbar_items() %>
	    
	    % if len(item_list) > 0:	    
		% for item in item_list['actions']:
		    <% write_item(item) %>
		% endfor
	    % endif
	</ul>
	
	<div class="clear-both"></div>
    </div>
</%def>
    
<%def name="write_item(item)">
    <li>
	<a class="item-icon-link" title="${item['link_title']}" href="${item['link']}">
	    <img alt="${item['icon_alt']}" src="/default/images/icons/${item['icon']}"/>
	    <span>${item['title']}</span>
	</a>
    </li>
</%def>
