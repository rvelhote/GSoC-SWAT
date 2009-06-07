<%def name="write(controller, action='')">
    <div id="task-toolbar">
	<ul class="task-toolbar">
	    
	    <% link_list = h.get_links_for("toolbar", controller, action) %>
	    
	    % if link_list is not None and len(link_list) > 0:	    
		% for link in link_list['actions']:
		    <li>
			<a class="item-icon-link" title="${link['link_title']}" href="${link['link']}">
			    <img alt="${link['icon_alt']}" src="/default/images/icons/${link['icon']}"/>
			    <span>${link['title']}</span>
			</a>
		    </li>
		% endfor
	    % endif
	</ul>
	
	<div class="clear-both"></div>
    </div>
</%def>
