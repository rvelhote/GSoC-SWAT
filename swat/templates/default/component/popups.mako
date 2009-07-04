<%doc>Should move the non-presentation code into a helper</%doc>
<%def name="select_path(current='/')">
    <% import os %>

    <ul class="popup-list path-list">
        <li><a style="float:left;display:block;height:16px;padding-left:20px;background-image:url('/default/images/icons/arrow-return-090.png');background-position:left center;background-repeat:no-repeat;" onclick="path.get('${h.url_for(controller = 'share', action = 'path', path = os.path.split(current)[:1])}');return false;" title="${_('Parent Folder')}" href="#">...</a>
        
        % try:
            <%
        
            folders = os.listdir(current)
            has_dirs = False %>
            
            % if len(folders) > 0:
                % for f in folders:
                    <% path = os.path.join(current, f) %>
                    
                    % if os.path.isdir(path):
                        <li>
                            <a style="float:left;display:block;height:16px;padding-left:20px;background-image:url('/default/images/icons/folders.png');background-position:left center;background-repeat:no-repeat;" id="path-selector" onclick="path.get('${h.url_for(controller = 'share', action = 'path', path = path)}'); return false;" title="${_('List this Folder')}" href="#">
                                ${f}
                            </a>
                            
                            <a title="${_('Copy this Path to the Textbox')}" onclick="path.add('${path}');return false;" href="#"><img alt="Add Icon" class="add" src="/default/images/icons/plus-small.png" /></a>
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

<%doc>Should move the non-presentation code into a helper</%doc>
<%def name="select_user_group()"><%
    import grp
    
    list = grp.getgrall()
    users = []

    for g in list:
        if len(g.gr_mem) > 0:
            users.extend(g.gr_mem)

    users = set(users) %>
    
    <h1 style="font-weight:bold;border-bottom:1px solid #484848;margin-bottom:10px;">${_('User List')}</h1>
    <ul class="popup-list group-list" style="margin-bottom:25px;">
        % for g in users:
            <li>
                <span style="float:left;display:block;height:16px;padding-left:20px;background-image:url('/default/images/icons/user.png');background-position:left center;background-repeat:no-repeat;">${g}</span>
                <a title="${_('Add this User/Group to the List')}" onclick="userGroup.add('${g}', 'u');return false;" href="#"><img class="add" src="/default/images/icons/plus-small.png" /></a>
            </li>
        % endfor
    </ul>

    <h1 style="font-weight:bold;border-bottom:1px solid #484848;margin-bottom:10px;">${_('Group List')}</h1>
    <ul class="popup-list group-list">
        % for g in list:
            <li>
                <span style="float:left;display:block;height:16px;padding-left:20px;background-image:url('/default/images/icons/users.png');background-position:left center;background-repeat:no-repeat;">${g.gr_name}</span>
                <a title="${_('Add this User/Group to the List')}" onclick="userGroup.add('${g.gr_name}', 'g');return false;" href="#"><img class="add" src="/default/images/icons/plus-small.png" /></a>
            </li>
        % endfor
    </ul>
</%def>