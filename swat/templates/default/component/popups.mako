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
    <%
    #
    # FIXME Just temporary
    #
    from swat.controllers.account import SAMPipeManager
    from samba.dcerpc import samr, security, lsa
    from samba import credentials, param
    
    samba_lp = param.LoadParm()
    samba_lp.load_default()
    
    manager = SAMPipeManager(c.samba_lp)
    
    domains = manager.fetch_and_get_domain_names()
    manager.set_current_domain(0)
    manager.fetch_users_and_groups()
    
    %>
    
    <h1>${_('User List')}</h1>
    <ul class="popup-list usr-list">
        % for g in manager.user_list:
            <%
            
            selected = ""
            operation = "add"
            
            if g.username in already_selected:
                selected = "selected"
                operation = "remove"
            
            %>
            <li class="${selected}">
                <span class="name" title="${g.description}">${g.username}</span>
                <span class="operation ${operation}"></span>
            </li>
        % endfor
    </ul>
</%def>

<%def name="group_list(already_selected)">
    <%
    #
    # FIXME Just temporary
    #
    from swat.controllers.account import SAMPipeManager
    from samba.dcerpc import samr, security, lsa
    from samba import credentials, param
    
    samba_lp = param.LoadParm()
    samba_lp.load_default()
    
    manager = SAMPipeManager(c.samba_lp)
    
    domains = manager.fetch_and_get_domain_names()
    manager.set_current_domain(0)
    manager.fetch_users_and_groups()

    
    %>
    
    <h1>${_('Group List')}</h1>
    <ul class="popup-list grp-list">
        % for g in manager.group_list:
            <%
            
            selected = ""
            operation = "add"
            
            if "@" + g.name in already_selected:
                selected = "selected"
                operation = "remove"
            
            %>
            <li class="${selected}">
                <span class="name" title="${g.description}">${g.name}</span>
                <span class="operation ${operation}"></span>
            </li>
        % endfor
    </ul>
</%def>