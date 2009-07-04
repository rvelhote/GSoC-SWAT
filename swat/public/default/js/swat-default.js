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

/**
 *  Path Selection
 */
var PathSelector = new Class({
    Implements: [Options, Events],
    
    options: {
        request: null,
        element: '',
        copyTo: ''
    },
    
    initialize: function(options) {
        this.setOptions(options);        
        this.request = new Request.HTML({
            update: this.options.element
        });
    },
    
    get: function(url) {
        this.request.get(url);
    },
    
    add: function(path) {
        $(this.options.copyTo).value = path;
    },
    
    remove: function() {
        $(this.options.copyTo).value = "";
    }
});

function add(name, type) {
    
}

var UserGroupSelector = new Class({
    Implements: [Options, Events],
    
    options: {
        request: null,
        element: '',
        copyTo: '',
        addFrom: ''
    },
    
    initialize: function(options) {
        this.setOptions(options);        
        this.request = new Request.HTML({
            update: this.options.element
        });
    },
    
    get: function(url) {
        this.request.get(url);
    },
    
    add: function(name, type) {
        if(name.length == 0) {
            return;
        }
        
        if(type == "g") {
            name = "@" + name;
        }        
        
        if(this.exists(name)) {
            alert("Already Exists!");
            return;
        }
        
        var numElements = $(this.options.copyTo).getChildren().length;
        var newElementId = 'delete-read-list-' + (numElements + 1);
        
        var newLi = new Element('li');
        var newAnchor = new Element('a', {class:"delete-link", id:newElementId, title:"Remove this User/Group", href:"#"});

        newAnchor.addEvent('click', function(ev) {
            event = new Event(ev).stop();
            this.remove(ev.target);
        }.bind(this));
        
        var newSpan = new Element('span', {text:name});
        newSpan.injectInside(newAnchor);
        
        newAnchor.injectInside(newLi);
        newLi.injectInside($(this.options.copyTo));
    },
    
    remove: function(id) {
        if($(this.options.copyTo).hasChild(id)) {
            $(id).getParent().dispose();
        }
    },
    
    addManual: function(type) {
        this.add($(addFrom).value, type);
        $(addFrom).value = "";
    },
    
    exists: function(name) {
        var elements = $(this.options.copyTo).getChildren();
        var n = elements.length;
        var span = null;
        
        var exists = false;
        
        for(var i = 0; i < n; i++) {
            span = elements[i].getElement("span");
            
            if(span.get('text') == name) {
                exists = true;
                break;
            }
        }
        
        return exists;
    }
});