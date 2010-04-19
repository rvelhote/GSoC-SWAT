<%doc>
#
# Pagination Mako Template file for SWAT
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

<%doc>
    TODO if there are too many pages the page numbers will seem weird.
    Need to implement some elipses (...) in the middle of the count for this
    case and also, perhaps, a first and last button (must find suitable icon
    first.)
    
    TODO/FIX improve page links.
</%doc>
<%def name="paginate(what, per_page = 1, current_page = 1)">
    <%
    
    import math
    
    total_items = len(what)
    total_pages = math.ceil(float(total_items) / float(per_page))
    
    %>

    % if total_items > 0 and total_pages > 1:
        <ul class="pagination">
            % if total_pages > 1 and current_page > 1:
                <li class="previous">
                    <a title="${_('Previous Page')}" href="?page=${current_page - 1}&amp;per_page=${per_page}">
                        <img src="/default/images/icons/arrow-180-small.png" alt="${_('Arrow Previous Page Icon')}" />
                    </a>
                </li>
            % endif
            
            % for i in range(1, total_pages + 1):
                <% current_item_class = "" %>
                
                <%doc>FIXME if per_page is one all items will be highlighted</%doc>
                % if (i - 1) % per_page == 0:
                    <% current_item_class = " current-item " %>
                % endif
            
                <li>
                    <a class="${current_item_class}" title="${_('List Page')} ${i}" href="?page=${i}&amp;per_page=${per_page}">${i}</a>
                </li>
                
                % if i % per_page == 0:
                    <% i = i + 1 %>
                % endif
            % endfor

            % if total_pages > 1 and current_page < total_pages:
                <li class="next">
                    <a title="${_('Next Page')}" href="?page=${current_page + 1}&amp;per_page=${per_page}">
                        <img src="/default/images/icons/arrow-000-small.png" alt="${_('Arrow Next Page Icon')}" />
                    </a>
                </li>
            % endif                            
        </ul>
    % endif
</%def>