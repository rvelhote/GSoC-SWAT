<%doc>Creates a list of Folders in a specified folder</%doc>
<%def name="select_path(current='/')">
    <%
    
    import os
    
    up_link = h.url_for(controller='share', action='path', path=os.path.split(current)[:1])
    
    %>

    <h1>${current}</h1>
    <ul class="popup-list path-list">
        <li><a class="up" title="${_('Parent Folder')}" href="${up_link}">...</a>
        
        % try:
            <%
        
            folders = os.listdir(current)
            has_dirs = False
            
            %>
            
            % if len(folders) > 0:
                % for f in folders:
                    <% path = os.path.join(current, f) %>
                    
                    % if os.path.isdir(path):
                    
                        <% link = h.url_for(controller = 'share', action = 'path', path = path) %>
                        
                        <li>
                            <a class="folder" title="${_('List this Folder')}" href="${link}">
                                ${f}
                            </a>
                            
                            <input type="hidden" name="path" value="${path}" />
                            
                            <a class="add" title="${_('Copy this Path to the Textbox')}" href="#">
                                <img alt="Add Icon" class="add" src="/default/images/icons/plus-small.png" />
                            </a>
                        </li>
                        
                        <% has_dirs = True %>
                    % endif
                % endfor
                
                % if has_dirs == False:
                    <li>${_('No directories to choose here...')}</li>
                % endif
                
            % else:
                <li>${_('Nothing to see here')}</li>
            % endif
            
        % except OSError:
            <li>${_("Ooops, can't go there...")}</li>
        % endtry
    </ul>
</%def>

<%def name="select_user_group(already_selected)">
    <%
    
    user_list(already_selected)
    group_list(already_selected)
    
    %>
</%def>
    
<%def name="user_list(already_selected)">
    <% users = h.get_user_list() %>
    
    <h1>${_('User List')}</h1>
    <ul class="popup-list usr-list">
        % for g in users:
            <%
            
            selected = ""
            if g in already_selected:
                selected = "selected"
            
            %>
            <li class="${selected}">
                <span>${g}</span>
                <a class="add user" title="${_('Add this User/Group to the List')}" href="#">
                    <img class="add" src="/default/images/icons/plus-small.png" />
                </a>
            </li>
        % endfor
    </ul>
</%def>

<%def name="group_list(already_selected)">
    <% groups = h.get_group_list() %>
    
    <h1>${_('Group List')}</h1>
    <ul class="popup-list grp-list">
        % for g in groups:
            <%
            
            selected = ""
            if "@" + g.gr_name in already_selected:
                selected = "selected"
            
            %>
            <li class="${selected}">
                <span>${g.gr_name}</span>
                <a class="add group" title="${_('Add this User/Group to the List')}" href="#"><img class="add" src="/default/images/icons/plus-small.png" /></a>
            </li>
        % endfor
    </ul>
</%def>