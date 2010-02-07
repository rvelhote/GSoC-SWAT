<%def name="paginate(what, per_page = 1, current_page = 1)">
    <% total_items = len(what.keys()) %>
    <% total_pages = int(round(float(total_items) / float(per_page), 0)) %>

    % if total_items > 0 and total_pages > 1:
        <ul class="pagination">
            % if total_pages:
                <li class="previous">
                    <a title="${_('Previous Page')}" href="#">
                        <img src="/default/images/icons/arrow-180-small.png" alt="${_('Arrow Previous Page Icon')}" />
                    </a>
                </li>
            % endif
            
            % for i in range(1, total_pages + 1):
                <li>
                    <a title="${_('List Page')} ${i}" href="#">${i}</a>
                </li>
                
                % if i % per_page == 0:
                    <% i = i + 1 %>
                % endif
            % endfor

            % if total_pages > 1:
                <li class="next">
                    <a title="${_('Next Page')}" href="#">
                        <img src="/default/images/icons/arrow-000-small.png" alt="${_('Arrow Next Page Icon')}" />
                    </a>
                </li>
            % endif                            
        </ul>
    % endif
</%def>