<%def name="select_path(current='/')">
    <% import os %>

    <ul class="path-list">
        <li><a onclick="path.get('${h.url_for(controller = 'share', action = 'path', path = os.path.split(current)[:1])}');return false;" title="${_('Parent Folder')}" href="#">..</a>
        
        % try:
            <%
        
            folders = os.listdir(current)
            has_dirs = False %>
            
            % if len(folders) > 0:
                % for f in folders:
                    <% path = os.path.join(current, f) %>
                    
                    % if os.path.isdir(path):
                        <li>
                            <a id="path-selector" onclick="path.get('${h.url_for(controller = 'share', action = 'path', path = path)}'); return false;" title="${_('List this Folder')}" href="#">
                                <img class="folder" src="/default/images/icons/folders.png" />
                                ${f}
                            </a>
                            
                            <a title="${_('Copy this Path to the Textbox')}" onclick="path.add('${path}');return false;" href="#"><img class="add" src="/default/images/icons/plus-small.png" /></a>
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
