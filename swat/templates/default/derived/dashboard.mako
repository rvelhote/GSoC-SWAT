<%inherit file="/default/base/base.mako" />
<%namespace name="widget" file="/default/component/widget.mako" />
<div class="swat-content dashboard round-2px">
    
    ${parent.header()}
    
    <div id="swat-main-area">   
	<ul id="breadcrumb" class="breadcrumb-trail">
	    <li>&raquo;&nbsp;Dashboard</li>                    
	</ul>
	
	<div id="important-messages" class="messages cool round-2px">
	    <p>This area is for important messages for the user and may or may not show up...</p>
	</div>
	
	<div id="important-messages-2" class="messages critical round-2px">
	    <p>Samba4 is not configured. Configure it <a href="configuration_assistant.html">now</a>!</p>
	</div>
	
	${widget.get_all("dashboard")}
    </div>
    
    <div class="clear-both"></div>            
</div>

<%def name="title()">
    ${parent.title()} :: Dashboard
</%def>