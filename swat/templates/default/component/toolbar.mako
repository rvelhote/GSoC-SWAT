<%def name="write(items)">
    <div id="task-toolbar">
	<ul class="task-toolbar">
	    % if len(items) > 0:	    
		% for item in items['actions']:
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
