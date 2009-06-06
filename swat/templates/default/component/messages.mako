<%def name="write(messages)">
    % if messages is not None and len(messages) > 0:
	% for message in messages:
	    <div class="messages ${message['type']} round-2px">
		<p>${message['text']}</p>
	    </div>
	% endfor
    % endif
</%def>