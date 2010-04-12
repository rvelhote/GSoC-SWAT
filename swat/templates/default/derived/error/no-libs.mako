<%namespace name="base" file="/default/base/base.mako" />
<%namespace name="messages" file="/default/component/messages.mako" />
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>${self.page_title()}</title>
	${base.head_tags()}
    </head>
    
    <body>        
	<div class="swat-content login round-2px">
            
            ${base.samba_logo(False)}
            <br />
            % if h.SwatMessages.any():
                ${messages.write(h.SwatMessages.get())}
                <% h.SwatMessages.clean() %>
            % endif
	</div>
</html>

<%def name="page_title()">
    ${_('Samba Web Administration Tool')}
</%def>