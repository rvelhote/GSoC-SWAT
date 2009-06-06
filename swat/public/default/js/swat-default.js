window.addEvent("domready", function() {
    /**
     *  Add the Tab Feature
     */
    var tabList = $$("li[id^=tab]");
    var numTabs = tabList.length;
    
    if(numTabs > 0) {    
        for(var i = 0; i < numTabs; i++) {
            tabList[i].addEvent("click", function(event) {
                event = new Event(event).stop();
                activateTab(this);
            });
        }
    }
    
    /**
     *  Delete Confirmation Popup Mockup
     */
    var deleteButtonsList = $$("a[id^=delete-]");
    var numButtons = deleteButtonsList.length;
    
    if(numButtons > 0) {    
        for(var i = 0; i < numButtons; i++) {
            deleteButtonsList[i].addEvent("click", function(event) {
                event = new Event(event).stop();
                confirm("Are you sure you want to delete this User/Group?");
            });          
        }
    }    
});

function activateTab(clickedTab) {
    if(clickedTab) {
        var clickedTabContent = $("content-" + clickedTab.getProperty("id"));
        
        if(clickedTab && clickedTabContent) {
            clickedTab.addClass("active");
            clickedTabContent.addClass("active");
    
            var tabList = clickedTab.getParent().getChildren();
            var numTabs = tabList.length;
            var otherTab = null;
            
            for(var i = 0; i < numTabs; i++) {
                if(tabList[i] && tabList[i].getProperty("id") != clickedTab.getProperty("id")) {
                    tabList[i].removeClass("active");
                    otherTab = $("content-" + tabList[i].getProperty("id"));
                    
                    if(otherTab) {
                        otherTab.removeClass("active");
                    }
                }
            }
        }
    }
}