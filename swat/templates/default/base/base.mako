<%namespace name="menu" file="/default/component/menu.mako" />
<%namespace name="messages" file="/default/component/messages.mako" />
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>${self.page_title()}</title>
	${next.head_tags()}
    </head>
    
    <body>
	<div class="swat-content dashboard round-2px">
	    
	    ${self.header()}
	    
	    <div id="swat-main-area">   
		${menu.breadcrumb()}
		
		% if session.has_key("messages"):
		    ${messages.write(session['messages'].get())}
		    <% session['messages'].clean() %>
		% endif
		
		${self.body()}
	    </div>
	    
	    <div class="clear-both"></div>
	</div>
	
	${next.footer()}
    </body>
</html>

<%doc>
Base Page Title
</%doc>
<%def name="page_title()">
    Samba Web Administration Tool
</%def>

<%doc>
Head Tags
</%doc>
<%def name="head_tags()">
    <link rel="shortcut icon" href="/default/images/favicon.ico" />
    
    ${h.javascript_link(h.url_for('/default/js/mootools-core-nc.js'))}
    ${h.javascript_link(h.url_for('/default/js/swat-default.js'))}

    ${h.stylesheet_link(h.url_for('/default/css/reset-fonts-yui.css'))}
    ${h.stylesheet_link(h.url_for('/default/css/swat-default.css'))}
    
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</%def>

<%doc>
Base Page Footer
</%doc>
<%def name="footer()">
    <div id="swat-footer">
	<p>Samba Web Administration Tool :: GSoC</p>
	<p>Only Tested in Firefox for now! | <a title="Icons used in SWAT" href="http://www.pinvoke.com">Fugue Icons</a> | <a href="http://www.samba.org">Samba</a></p>
    </div>
</%def>

<%doc>
Header Part. Contains items that will be in all pages except login
</%doc>
<%def name="header()">
    <div id="swat-top">
	${self.samba_logo()}  
	${self.server_name()}
        ${menu.top()}
	${self.goto_box()}
	
	<div class="clear-both"></div>
    </div>
</%def>

<%doc>Samba Logo</%doc>
<%def name="samba_logo()">
    <a href="${h.url_for(controller = 'dashboard')}">
	<img class="samba-logo samba-logo-interior" src="/default/images/samba-logo.png" alt="Samba Logo" title="Samba - Opening Windows to a Wider World" />
    </a>
</%def>

<%doc>Server Name + Server Status Icon</%doc>
<%def name="server_name()"><%
    name = g.samba.get_conf().get_string("servername") or "" %>
    
    <h1 class="server-name title-icon ${h.get_samba_server_status()}">
	% if len(name) > 0:
	    ${name}
	% else:
	    Samba ${g.samba_version}
	% endif
    </h1>
</%def>

<%doc>
"Goto" box. Previously know as the filter box. I felt it wasn't very
useful to have a filterbox since most pages will not have many things to filter.
It was mainly an idea I got from CPanel. It will know be a filterbox that will
jump to a controller/action that the user types in
</%doc>
<%def name="goto_box()">

    ${h.form(h.url_for(controller='dashboard', action='goto'), method='get')}
	<div class="filter-items">
	    <label title="Go directly to" for="goto-items-textbox">Goto: </label>
	    ${h.text('where', '', id = 'goto-items-textbox')}
	</div>
    ${h.end_form()}
    
</%def>

<%def name="action_title(text)">
    <h2 class="module-title">${text}</h2>
</%def>