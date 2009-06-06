<%namespace name="menu" file="/default/component/menu.mako" />
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>${self.title()}</title>
	${next.head()}
    </head>
    
    <body>
	${self.body()}
	${next.footer()}
    </body>
</html>

<%doc>SWAT Title</%doc>
<%def name="title()">
    Samba Web Administration Tool
</%def>

<%def name="head()">
    <link rel="shortcut icon" href="default/images/favicon.ico" />
    
    ${h.javascript_link(h.url_for('/default/js/mootools-core-nc.js'))}
    ${h.javascript_link(h.url_for('/default/js/swat-default.js'))}

    ${h.stylesheet_link(h.url_for('/default/css/reset-fonts-yui.css'))}
    ${h.stylesheet_link(h.url_for('/default/css/swat-default.css'))}
    
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</%def>

<%def name="footer()">
    <div id="swat-footer">
	<p>Samba Web Administration Tool :: HTML Prototype v1</p>
	<p>Only Tested in Firefox for now! | <a title="Icons used in SWAT" href="http://www.pinvoke.com">Fugue Icons</a> | <a href="http://www.samba.org">Samba</a></p>
    </div>
</%def>

<%def name="header()">
    <div id="swat-top">
	${self.samba_logo()}  
	${self.server_name()}
        ${menu.top()}
	${self.goto_box()}
	
	<div class="clear-both"></div>
    </div>
</%def>
    
<%def name="samba_logo()">
    <a href="dashboard.html"><img class="samba-logo samba-logo-interior" src="default/images/samba-logo.png" alt="Samba Logo" title="Samba - Opening Windows to a Wider World" /></a>
</%def>

<%def name="server_name()">
    <h1 class="server-name title-icon ${h.get_samba_server_status()}">Vandelay Industries</h1>
</%def>

<%def name="goto_box()">
    <div class="filter-items">
	<label title="Filter Icons" for="filter-items-textbox">Filter: </label>
	<input id="filter-items-textbox" name="item_filter" type="text" />
    </div>
</%def>s