<%doc>
#
# Share Index Mako Template file for SWAT
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#   
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#   
# You should have received a copy of the GNU General Public License
# 
</%doc>
<%inherit file="/default/base/base.mako" />
<%namespace name="toolbar" file="/default/component/toolbar.mako" />
<%namespace name="pagination" file="/default/component/pagination.mako" />

${parent.action_title(c.config.get_action_info('friendly_name'))}
${toolbar.write(c.config.get_toolbar_items())}
${options()}
${share_table(c.share_list)}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: ${c.config.get_action_info('friendly_name')}
</%def>

<%def name="share_table(shares)">

<script type="text/javascript">
    window.addEvent("domready", function() {
        formSubmission = new FormSubmit({formId: 'share-list'});
    });
</script>

${h.form('', method="post", id="share-list", class_="")}
    <table summary="${_('List of Shares for the current Samba Server')}" class="list" id="share-list">
	<thead>
	    <tr>
		<td class="check-all"><input title="${_('Check All Items')}" onchange="checkAllRows(this, 'check-row')" type="checkbox" id="check-all"/></td>
		<td class="share-row-id">${_('#')}</td>
		<td class="share-name">${_('Name')}</td>
		<td class="share-path">${_('Path')}</td>
		<td class="share-comment">${_('Comment')}</td>
		<td class="share-quick-operations"></td>
	    </tr>
	</thead>
	
        % if len(shares) > 0:
            <tfoot>
                <tr>
                    <td colspan="6">		    
                        <div class="pagination">
                            <%
                            
                            showing_floor = (c.current_page - 1) * c.per_page
                            showing_ceil = c.current_page * c.per_page
                            
                            if showing_ceil > len(shares):
                                showing_ceil = len(shares)

                            %>
                            
                            <p class="number-pages">${_('Showing %d-%d of %d Shares' % (showing_floor, showing_ceil, len(shares)))}</p>
                            <% pagination.paginate(shares, c.per_page, c.current_page) %>
                        </div>
                    </td>
                </tr>
            </tfoot>
        % endif

	<tbody>
	    <% i = 1 %>
	    
            <%doc>
            Workaround for SharesContainer not supporting slicing.
            Something to think about later
            </%doc>
            <%

            begin = (c.current_page - 1) * c.per_page
            end = begin + c.per_page

            %>
            
            % if len(shares) > 0:
                % for share in shares[begin:end]:
                    <%
                    
                    #if share.endswith("$"):
                    #    continue
                    
                    tr_class = ''
                    home_class = ''
                    
                    if share.get_share_name() == 'homes':
                        home_class = ' home-directory '
                        
                    %>
                    
                    % if i % 2 == 0:
                        <% tr_class = " alternate-row " %>
                    % endif
                    
                    <tr id="row-${i}" title="${_('Edit Share')}" class="${tr_class}">
                        <td><input value="${share.get_share_name()}" onchange="selectShareRow(this);" name="name" type="checkbox" id="check-row-${i}" /></td>
                        <td onclick="clickableRow('${h.url_for('share_action', action = 'edit', name = share.get_share_name())}');">${i}</td>
                        
                        <td onclick="clickableRow('${h.url_for('share_action', action = 'edit', name = share.get_share_name())}');" class='${home_class}'>${share.get_share_name()}</td>
                        <td onclick="clickableRow('${h.url_for('share_action', action = 'edit', name = share.get_share_name())}');">
                            % if len(share.get("path")) > 0:
                                ${share.get("path")}
                            % else:
                                ${_('No Path Defined or Required')}
                            % endif
                        </td>
                        <td onclick="clickableRow('${h.url_for('share_action', action = 'edit', name = share.get_share_name())}');">
                            % if share.get("comment"):
                                ${share.get("comment")}
                            % else:
                                ${_('No Comment Defined')}
                            % endif
                        </td>
                        <td>
                            ${quick_tasks(share.get_share_name(), False)}   
                        </td>                            
                    </tr>
                    
                    <% i = i + 1 %>
                % endfor
            % else:
                <tr>
                    <td colspan="5"><p style="font-weight:bold;text-align:center;">${_("No Shares Available")}</p></td>
                </tr>
            % endif
	</tbody>
    </table>
${h.end_form()}
</%def>
    
<%def name="quick_tasks(share_name, is_disabled=False)">
    <ul class="quick-tasks">
	<li><a href="${h.url_for('share_action', action = 'edit', name = share_name)}" title="${_('Edit Share')}"><img src="/default/images/icons/folder-pencil.png" alt="${_('Edit Share Icon')}"/></a></li>
	<li><a href="${h.url_for('share_action', action = 'remove', name = share_name)}" title="${_('Remove Share')}"><img src="/default/images/icons/folder-minus.png" alt="${_('Remove Share Icon')}"/></a></li>
	<li><a href="${h.url_for('share_action', action = 'copy', name = share_name)}" title="${_('Copy this Share')}"><img src="/default/images/icons/folders-plus.png" alt="${_('Copy Share Icon')}"/></a></li>
	<!--<li><a href="${h.url_for('share_action', action = 'toggle', name = share_name)}" title="${_('Enable this Share')}"><img src="/default/images/icons/switch-plus.png" alt="${_('Enable Share Icon')}"/></a></li>-->
    </ul>
</%def>

<%def name="options()">
    ${h.form(h.url_for(controller = 'share', action = 'index'), method="get", id="options")}
        <div style="font-size:85%;margin-bottom:15px;">
            <span>
                <label for="filter_share_by_name">${_('Filter')}:</label>
                ${h.text("filter_shares", c.filter_name, id="filter_share_by_name")}
            </span>
            
            % if len(c.filter_name) > 0 or int(c.per_page) != 10:
                <a class="reset-view round-2px" href="${h.url_for(controller = 'share', action = 'index')}">${_("reset view")}</a>
            % endif
            
            <span style="float:right;">
                <label for="items_per_page">${_('Per Page')}:</label>
                <select name="per_page" id="items_per_page" onchange="submitForm('options');">
                    % for i in range(5, 30, 5):
                        <option
                        
                        % if i == c.per_page:
                            ${'selected="selected"'}
                        
                        % endif
                        
                        value="${i}">${i}</option>
                    % endfor
                </select>
            </span>
            
        </div>
    ${h.end_form()}
</%def>