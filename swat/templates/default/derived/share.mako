<%inherit file="/default/base/base.mako" />
<%namespace name="toolbar" file="/default/component/toolbar.mako" />

${parent.action_title(c.controller_config.get_action_info('page_title'))}
${toolbar.write(c.controller_config.get_toolbar_items())}

${share_table(['test'])}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: ${c.controller_config.get_action_info('page_title')}
</%def>

<%def name="share_table(shares)">
    <table summary="List of Shares for Samba Server: Vandelay Industries" class="list" id="share-list">
	<thead>
	    <tr>
		<td><input type="checkbox" id="check-all"/></td>
		<td>#</td>
		<td>Name</td>
		<td>Path</td>
		<td>Comment</td>
		<td> </td>
	    </tr>
	</thead>
	
	<tfoot>
	    <tr>
		<td colspan="6">		    
		    <div class="pagination">
			<p class="number-pages">${len(shares)} Shares Total</p>
		    </div>
		</td>
	    </tr>
	</tfoot>                    
	
	<tbody>
	
	    <% i = 1 %>
	    
	    % for share in shares:
		<% tr_class = '' %>
		
		% if i % 2 == 0:
		    <% tr_class += " alternate-row " %>
		% endif
		
		<tr class="${tr_class}">
		    <td><input name="select_share${i}" type="checkbox"/></td>
		    <td>${i}</td>
		    <td>${share}</td>
		    <td>
			
			% if g.samba_lp.get('path', share) is not None:
			    ${g.samba_lp.get('path', share)}
			% else:
			    No Path Defined
			% endif
		    </td>
		    <td>
			% if g.samba_lp.get('comment', share):
			    ${g.samba_lp.get('comment', share)}
			% else:
			    No Comment Defined
			% endif
		    </td>
		    <td>
                        ${quick_tasks(share, False)}   
		    </td>                            
		</tr>
		
		<% i += 1 %>
	    
	    % endfor
	</tbody>
    </table>
</%def>
    
<%def name="quick_tasks(name, is_disabled)">
    <ul class="quick-tasks">
	<li><a href="${h.url_for(action = 'edit', name = name)}" title="Edit Share"><img src="/default/images/icons/folder-pencil.png" alt="Edit Share Icon"/></a></li>
	<li><a href="${h.url_for(action = 'remove', name = name)}" title="Remove Share"><img src="/default/images/icons/folder-minus.png" alt="Remove Share Icon"/></a></li>
	<li><a href="${h.url_for(action = 'copy', name = name)}" title="Copy this Share"><img src="/default/images/icons/folders-plus.png" alt="Copy Share Icon"/></a></li>
	<li><a href="${h.url_for(action = 'toggle', name = name)}" title="Enable this Share"><img src="/default/images/icons/switch-plus.png" alt="Enable Share Icon"/></a></li>
    </ul>
</%def>
