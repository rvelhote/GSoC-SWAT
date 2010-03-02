<%doc>
#
# Base Mako Template file for SWAT
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
		
		% if h.SwatMessages.any():
		    ${messages.write(h.SwatMessages.get())}
		    <% h.SwatMessages.clean() %>
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
    ${_('Samba Web Administration Tool')}
</%def>

<%doc>
Head Tags
</%doc>
<%def name="head_tags()">
    <link rel="shortcut icon" href="/default/images/favicon.ico" />
    
    ${h.javascript_link(h.url_for('/default/js/mootools-core-nc.js'))}
    ${h.javascript_link(h.url_for('/default/js/mootools-more-nc.js'))}
    ${h.javascript_link(h.url_for('/default/js/swat-default.js'))}

    ${h.stylesheet_link(h.url_for('/default/css/reset-fonts-yui.css'))}
    ${h.stylesheet_link(h.url_for('/default/css/swat-default.css'))}
    
    ${h.stylesheet_link(h.url_for('/default/css/smoothbox.css'))}
    ${h.javascript_link(h.url_for('/default/js/smoothbox.js'))}
    
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</%def>

<%doc>
Base Page Footer
</%doc>
<%def name="footer()">
    <div id="swat-footer">
	<p>${_('Samba Web Administration Tool')}</p>
	<p>${_('Only Tested in Firefox for now')} | <a title="${_('Icons used in SWAT')}" href="http://www.pinvoke.com">${_('Fugue Icons')}</a> | <a href="http://www.samba.org">${_('Samba')}</a></p>
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
	
	<div class="clear-both"></div>
    </div>
</%def>

<%doc>Samba Logo</%doc>
<%def name="samba_logo(with_link=True)">
    % if with_link:
	<a href="${h.url_for(controller = 'dashboard', action='index')}">
    % endif
    
    <img class="samba-logo samba-logo-interior" src="/default/images/samba-logo.png" alt="${_('Samba Logo')}" title="${_('Samba - Opening Windows to a Wider World')}" />
    
    % if with_link:
	</a>
    % endif
</%def>

<%doc>Server Name + Server Status Icon</%doc>
<%def name="server_name()"><%
    name = c.samba_lp.get("server name") or ""
    status = h.get_samba_server_status() or "down"
    
    if status == "down":
	h.swat_messages.add(_('Samba is down!'), "critical") %>
    
    <h1 class="server-name title-icon ${status}">
	% if len(name) > 0:
	    ${name}
	% else:
            <% from samba import version %>
	    Samba ${version}
	% endif
    </h1>
</%def>

<%def name="action_title(text)">
    <h2 class="module-title">${text}</h2>
</%def>