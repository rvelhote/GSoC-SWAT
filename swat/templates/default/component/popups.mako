<%def name="select_path(current='/')">
    <% import os %>

    <ul>
        <li><a title="${_('Parent Folder')}" href="${h.url_for(controller = 'share', action = 'path', path = os.path.split(current)[:1])}">..</a>
        
        % try:
            <%
        
            folders = os.listdir(current)
            has_dirs = False %>
            
            % if len(folders) > 0:
                % for f in folders:
                    <% path = os.path.join(current, f) %>
                    
                    % if os.path.isdir(path):
                        <li>
                            <a title="${_('List this Folder')}" href="${h.url_for(controller = 'share', action = 'path', path = path)}">${f}</a>
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
