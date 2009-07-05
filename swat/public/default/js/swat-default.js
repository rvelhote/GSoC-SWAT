window.addEvent("domready", function() {    
});

var FormSubmit = new Class({
    Implements: [Options, Events],

    options: {
        formId: ''
    },
    
    initialize: function(options) {
        this.setOptions(options);
        
        var elements = $$('a.form-submit-button');
        
        elements.each(function(el) {
            el.addEvent("click", function(ev) {
                ev = new Event(ev).preventDefault();
                
                this.changeTask(el.getProperty("href"));
                this.submitForm();
            }.bind(this));
        }.bind(this));
    },
    
    changeTask: function(link) {
        $(this.options.formId).setProperty("action", link);
    },
    
    submitForm: function() {
        $(this.options.formId).submit();
    }
});

var TabGroup = new Class({
    Implements: [Options, Events],

    options: {
        tabGroupClass: 'tab-list'
    },
    
    initialize: function(options) {
        this.setOptions(options);
        
        var tabContainers = $$('.' + this.options.tabGroupClass);
        var children = null;

        tabContainers.each(function(el) {
            children = el.getChildren("li");
            
            children.each(function(c) {
                c.addEvent("click", function(event) {
                    event = new Event(event).preventDefault()
                    tabs.activateTab(this.getProperty("id"));
                });
            });
        });
    },
    
    activateTab: function(tabId) {
        var clickedTab = $(tabId);
        
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
});

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

var UserGroupSelector = new Class({
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
    
    effect: function(id, type) {
        var element = $(id);
        
        if(element) {
            element.set('tween', {duration: 100});
            
            if(type == "add") {
                element.tween('opacity', 0, 1);
            } else {
                element.tween('opacity', 1, 0);
            }
        }
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
        var newElementId = 'delete-' + this.options.copyTo + '-' + (numElements + 1);
        
        var newLi = new Element('li');
        var newAnchor = new Element('a', {text:name, class:"delete-link", id:newElementId, title:"Remove this User/Group", href:"#"});

        newAnchor.addEvent('click', function(ev) {
            event = new Event(ev).stop();
            this.remove(ev.target);
        }.bind(this));
        
        newAnchor.injectInside(newLi);
        newLi.injectInside($(this.options.copyTo));
        
        this.effect(newElementId, "add");
    },
    
    addManual: function(from, to) {
        var items = null;
        var numItems = 0;
        
        from = $(from);
        this.options.copyTo = to;
        
        if(from) {
            items = from.value.split(',');
            numItems = items.length;

            for(var i = 0; i < numItems; i++) {
                this.add(items[i].trim());
            }
        }
    },
    
    remove: function(id, forReal) {
        var element = $(id);
        
        if(element) {
            this.effect(id, "remove");
            element.getParent().dispose();
        }
    },
    
    exists: function(name) {
        var elements = $(this.options.copyTo).getChildren();
        var n = elements.length;
        var a = null;
        
        var exists = false;
        
        for(var i = 0; i < n; i++) {
            a = elements[i].getElement("a");
            
            if(a.get('text') == name) {
                exists = true;
                break;
            }
        }
        
        return exists;
    }
});