<%doc>Creates a list of Folders in a specified folder</%doc>
<%def name="select_path(current='/')">
    <%
    
    import os
    
    up_link = h.url_for(controller='share', action='path', path=os.path.split(current)[:1])
    
    %>

    <h1>${current}</h1>
    <ul class="popup-list path-list">
        <li><a class="up" onclick="path.get('${up_link}');return false;" title="${_('Parent Folder')}" href="#">...</a>
        
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
                            <a class="folder" onclick="path.get('${link}'); return false;" title="${_('List this Folder')}" href="#">
                                ${f}
                            </a>
                            
                            <a class="add" title="${_('Copy this Path to the Textbox')}" onclick="path.add('${path}');return false;" href="#">
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

<%def name="select_user_group()">
    <%
    
    user_list()
    group_list()
    
    %>
</%def>
    
<%def name="user_list()">
    <% users = h.get_user_list() %>
    
    <h1>${_('User List')}</h1>
    <ul class="popup-list user-list">
        % for g in users:
            <li>
                <span>${g}</span>
                <a title="${_('Add this User/Group to the List')}" onclick="userGroup.add('${g}', 'u');return false;" href="#">
                    <img class="add" src="/default/images/icons/plus-small.png" />
                </a>
            </li>
        % endfor
    </ul>
</%def>

<%def name="group_list()">
    <% groups = h.get_group_list() %>
    
    <h1>${_('Group List')}</h1>
    <ul class="popup-list group-list">
        % for g in groups:
            <li>
                <span>${g.gr_name}</span>
                <a title="${_('Add this User/Group to the List')}" onclick="userGroup.add('${g.gr_name}', 'g');return false;" href="#"><img class="add" src="/default/images/icons/plus-small.png" /></a>
            </li>
        % endfor
    </ul>
</%def>