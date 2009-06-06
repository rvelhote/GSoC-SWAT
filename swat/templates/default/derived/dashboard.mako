<%inherit file="/default/base/base.mako" />

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
	
	<div class="dashboard-row col2">
	    <div class="widget round-2px">                    
		<div class="title-bar">
		    <h2 class="title-icon" style="background-image:url('default/images/icons/folders.png');"><a href="shares.html" title="Go to the Share Management Area">Share Management</a></h2>
		
		    <ul>                                
			<li><a href="shares.html" title="Go to the Share Management Area"><img src="default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>                                
		    </ul>
		</div>
		<div class="content">
		    <ul class="widget-task-list">
			<li>
			    <a href="create_share.html" title="Add a Share" class="item-icon-link">
				<img src="default/images/icons/folder-plus.png" alt="Add Share Icon" />
				<span>add share</span>
			    </a>
			</li>
			
			<li>
			    <a href="create_share.html" title="Add a Share using the Assistant" class="item-icon-link">
				<img src="default/images/icons/wand.png" alt="Add Share Assistant Icon" />
				<span>add share assistant</span>
			    </a>
			</li>                     
						    
			<li>
			    <a href="shares.html" title="List All Users" class="item-icon-link">
				<img src="default/images/icons/folders-stack.png" alt="List Shares Icon" />
				<span>list shares</span>
			    </a>
			</li>                           
		    </ul>
		    
		    <div class="clear-both"></div>
		</div>
	    </div>                
			     
	    <div class="widget round-2px">                    
		<div class="title-bar">
		    <h2 class="title-icon" style="background-image:url('default/images/icons/users.png');"><a href="#" title="Go to the Account Management Area">Account Management</a></h2>
					
		    <ul>                                
			<li><a href="#" title="Go to the Account Management Area"><img src="default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>                                
		    </ul>
		</div>
		
		<div class="content">
		    <ul class="widget-task-list">
			<li>
			    <a href="#" title="Add a User" class="item-icon-link">
				<img src="default/images/icons/user-plus.png" alt="Add User Icon" />
				<span>add user</span>
			    </a>
			</li>
						    
			<li>
			    <a href="#" title="List All Users" class="item-icon-link">
				<img src="default/images/icons/user-silhouette.png" alt="List Users Icon" />
				<span>list users</span>
			    </a>
			</li>							
		    </ul>
		    
		    <div class="clear-both"></div>
		</div>
	    </div>
	    
	    <div class="clear-both"></div>
	</div>
	
	<div class="dashboard-row col2">
	    <div class="widget round-2px">
		<div class="title-bar">
		    <h2 class="title-icon" style="background-image:url('default/images/icons/printer.png');"><a href="#" title="Go to the Printer Management Area">Printer Management</a></h2>

		    <ul>
			<li><a href="#" title="Go to the Help Area"><img src="default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>
		    </ul>
		</div>                                            
		
		<div class="content">
		    <div class="clear-both"></div>
		</div>
	    </div>                                    
	    
	    <div class="widget round-2px">                    
		<div class="title-bar">
		    <h2 class="title-icon" style="background-image:url('default/images/icons/question.png');"><a href="#" title="Get Help">Help</a></h2>
					    
		    <ul>                                
			<li><a href="#" title="Go to the Help Area"><img src="default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>                                
		    </ul>                            
		</div>

		<div class="content">
		    <ul class="widget-task-list">
			<li>
			    <a href="#" title="Go Through the Samba Checklist" class="item-icon-link">
				<img src="default/images/icons/ui-check-box.png" alt="Checklist Icon" />
				<span>troubleshoot checklist</span>
			    </a>
			</li>
						    
			<li>
			    <a href="#" title="Help for Samba" class="item-icon-link">
				<img src="default/images/icons/user-silhouette.png" alt="List Users Icon" />
				<span>samba</span>
			    </a>
			</li>
			
			<li>
			    <a href="#" title="Help for SWAT" class="item-icon-link">
				<img src="default/images/icons/user-silhouette.png" alt="List Users Icon" />
				<span>swat</span>
			    </a>
			</li>                            
		    </ul>                        
		    
		    <div class="clear-both"></div>
		</div>
	    </div>
	    
	    <div class="clear-both"></div>
	</div>
    
	<div class="dashboard-row col1">
	    <div class="widget round-2px">                    
		<div class="title-bar">
		    <h2 class="title-icon" style="background-image:url('default/images/icons/blueprint.png');"><a href="#" title="Go to the Administration Area">Administration</a></h2>
		    
		    <ul>                                
			<li><a href="#" title="Go to the Administration Area"><img src="default/images/icons/arrow-000-small.png" alt="Right Arrow Icon" /></a></li>                                
		    </ul>                              
		</div>
		
		<div class="content">
		    <ul class="widget-task-list">
			
			<li>
			    <a href="configuration_assistant.html" title="Run the Samba4 Configuration Assistant" class="item-icon-link">
				<img src="default/images/icons/wand.png" alt="Configuration Assistant Icon" />
				<span>configuration assistant</span>
			    </a>
			</li>                                
			
			<li>
			    <a href="#" title="Manage Samba and SWAT Logs" class="item-icon-link">
				<img src="default/images/icons/document-text.png" alt="Logs Icon" />
				<span>logs</span>
			    </a>
			</li>
			
			<li>
			    <a href="#" title="Security" class="item-icon-link">
				<img src="default/images/icons/shield.png" alt="Security Icon" />
				<span>security settings</span>
			    </a>
			</li>
			
			<li>
			    <a href="#" title="Monitor Samba4 Status" class="item-icon-link">
				<img src="default/images/icons/application-monitor.png" alt="Status Monitor Icon" />
				<span>server status</span>
			    </a>
			</li>                             
		    </ul>
		    
		    <div class="clear-both"></div>
		</div>
	    </div>
	</div>
    </div>
    
    <div class="clear-both"></div>            
</div>

<%def name="title()">
    ${parent.title()} :: Dashboard
</%def>