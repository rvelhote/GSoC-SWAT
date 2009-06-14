<%doc>
#
# Messages Mako Template file for SWAT
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

<%def name="write(messages)">
    % if messages is not None and len(messages) > 0:
	% for message in messages:
	    <% write_one(message['text'], message['type']) %>
	% endfor
    % endif
</%def>

<%def name="write_one(text, type='info')">
    % if len(type) <= 0:
	<% type = 'info' %>
    % endif

    % if len(text) > 0:
	<div class="messages ${type} round-2px">
	    <p>${text}</p>
	</div>
    % endif
</%def>