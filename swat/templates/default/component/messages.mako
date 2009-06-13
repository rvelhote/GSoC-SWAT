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