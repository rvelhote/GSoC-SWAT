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
        var clickedTabContent = null;

        tabContainers.each(function(el) {
            children = el.getChildren("li");
            
            if(children) {         
                children.each(function(c) {
                    clickedTabContent = $("content-" + c.getProperty("id"));
                    
                    if(clickedTabContent && Cookie.read(getCurrentUri() + "-tab")) {
                        if(Cookie.read(getCurrentUri() + "-tab") == c.getProperty("id")) {
                            c.addClass("active");
                            clickedTabContent.addClass("active");
                        } else {
                            c.removeClass("active");
                            clickedTabContent.removeClass("active");
                        }
                    }
                    
                    c.addEvent("click", function(event) {
                        event = new Event(event).preventDefault()
                        tabs.activateTab(this.getProperty("id"));
                    });
                });
            }
        });
    },
    
    activateTab: function(tabId) {
        var clickedTab = $(tabId);
        
        if(clickedTab) {
            var clickedTabContent = $("content-" + clickedTab.getProperty("id"));
            
            if(clickedTab && clickedTabContent) {
                clickedTab.addClass("active");
                clickedTabContent.addClass("active");
                
                Cookie.write(getCurrentUri() + "-tab", clickedTab.getProperty("id"), {duration: 1});
        
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
//var PathSelector = new Class({
//    Implements: [Options, Events],
//    
//    options: {
//        request: null,
//        element: '',
//        copyTo: ''
//    },
//    
//    initialize: function(options) {
//        this.setOptions(options);
//        this.request = new Request.HTML({
//            update: this.options.element,
//            onComplete: this.bindEvents
//        });
//    },
//    
//    bindEvents: function() {
//        console.log("get to the binding man!");
//    },
//    
//    get: function(url) {
//        this.request.get(url);
//    },
//    
//    add: function(path) {
//        $(this.options.copyTo).value = path;
//    },
//    
//    remove: function() {
//        $(this.options.copyTo).value = "";
//    }
//});

var ItemList = new Class({
    Implements: [Options, Events],
    
    options: {
        //request: null,
        /*element: '',*/
        copyTo: ''
    },
    
    initialize: function(options) {
        this.setOptions(options);
        //this.addRemoveEvent();
       /* this.request = new Request.HTML({
            update: this.options.element
        });*/
    },
    
    /*addRemoveEvent: function() {
        elements = $$("a.delete-link");
        
        if(elements) {
            elements.each(function(a, i) {
                a.addEvent('click', function(ev) {
                    event = new Event(ev).stop();
                    this.options.copyTo = ev.target.getParent().getParent();
                    this.remove(ev.target);
                }.bind(this));
            }.bind(this));
        }
    },*/
    
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
    //
    //get: function(url) {
    //    this.request.get(url);
    //},
    
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
        
        var numElements = this.options.copyTo.getChildren().length;
        var newElementId = 'delete-' + this.options.copyTo.getProperty("id") + '-' + (numElements + 1);
        
        var newLi = new Element('li');
        var newAnchor = new Element('a', {text:name, class:"delete-link", id:newElementId, title:"Remove this item from the list", href:"#"});

        newAnchor.addEvent('click', function(ev) {
            event = new Event(ev).preventDefault();
            this.options.copyTo = ev.target.getParent().getParent();
            this.remove(ev.target);
        }.bind(this));
        
        newAnchor.injectInside(newLi);
        newLi.injectInside(this.options.copyTo);
        
        this.effect(newElementId, "add");
        this.updateHiddenList("add");
    },
    
   /* addManual: function(from, to) {
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
            
            from.value = "";
        }
    },*/
    
    remove: function(id, forReal) {
        var element = $(id);
        
        if(element) {
            this.effect(id, "remove");
            element.getParent().dispose();
            this.updateHiddenList("rem")
        }
    },
    
    exists: function(name) {
        var elements = this.options.copyTo.getChildren();
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
    },
    
    updateHiddenList: function(operation) {
        var area = $(this.options.copyTo.getProperty("id") + "-textbox");
        var list = this.options.copyTo;
        var elements = null;

        if(area && list) {
            links = list.getElements("li a");
            area.setProperty("value", "");

            links.each(function(link, i) {
                area.setProperty("value", area.getProperty("value") + "," + link.get("text"));
            });

            area.setProperty("value", area.getProperty("value").substring(1));
        }
    }
});

function getCurrentUri() {
    var uri = new URI(window.location);
    return uri.toRelative();
}

function selectShareRow(checkbox) {
    var rowId = "";
    
    if(checkbox) {
        rowId = checkbox.id.substring(6);
        if(checkbox.checked) {
            $(rowId).addClass("selected-row");
        } else {
            $(rowId).removeClass("selected-row");
        }
    }
}

function clickableRow(url) {
    window.location = url;
}

function calcPermissions(base, copyTo) {
    var owner = $(base + "-owner");
    var group = $(base + "-group");
    var world = $(base + "-world");
    var target = $(copyTo);
    
    if(owner && group && world && copyTo) {
        target.setProperty("value", "0" +
                                owner.getProperty("value") +
                                group.getProperty("value") +
                                world.getProperty("value") + "L");
    }
}

function checkAllRows(parent, base) {
    var checkboxes = $$("input[id^=" + base + "]");
    var op = parent.checked ? "check" : "uncheck";
    
    if(checkboxes) {
        checkboxes.each(function(c) {
            if(op == "check") {
                c.checked = true;
            } else {
                c.checked = false;
            }
            
            selectShareRow(c);
        });
    }
}

var Popup = new Class({
    Implements: [Options, Events],
    
    options: {
        title: "",
        window: ""
    },
    
    isActive: false,
    htmlRequest: null,
    
    initialize: function(options) {
        this.setOptions(options);
        this.setup();
    },
    
    setup: function() {
        /**
         *
         */
        var mainWindow = new Element('div', {opacity: 0, id: this.options.window, class:'popup-main-window round-2px'});
        mainWindow.injectInside(document.body);
        
        var titleBar = new Element('div', {'id': this.options.window + "-title-bar", 'class': 'popup-main-window-title-bar'});
        titleBar.injectInside(mainWindow);
        
        var titleBarTitle = new Element('span', {'id': this.options.window + "-title", class:'popup-main-window-title'});
        var titleBarClose = new Element('a', {'text': 'close', 'id': this.options.window + "-close", class:'popup-main-window-close'});
        
        titleBarTitle.injectInside(titleBar);
        titleBarClose.injectInside(titleBar);

        var mainWindowContent = new Element('div', {'id': this.options.window + "-content", class:'popup-main-window-content'});
        mainWindowContent.injectInside(mainWindow);
        
        /**
         *
         */
        titleBarTitle.set("text", this.options.title);
        titleBarClose.addEvent('click', this.hide.bind(this));
        mainWindow.makeDraggable({handle: titleBar.getProperty("id")});

        this.options.window = mainWindow;
        this.position();
    },
    
    show: function() {
        if(!this.isActive) {
            this.position();
            
            this.options.window.set('tween', {duration: 150});
            this.options.window.fade("in");
            
            this.isActive = true;
        }
    },
    
    makeRequest: function(url) {
        this.htmlRequest.get(url);
    },
    
    hide: function(ev) {
        new Event(ev).preventDefault();
        
        if(this.isActive) {
            this.options.window.set('tween', {duration: 150});
            this.options.window.fade("out");
            
            this.isActive = false;
        }
    },
    
    position: function() {
        this.options.window.setStyle("left", (window.getScrollLeft() + (window.getWidth() - this.options.window.getStyle("width").toInt()) / 2) + 'px');
	this.options.window.setStyle("top", (window.getScrollTop() + (window.getHeight() - this.options.window.getStyle("height").toInt()) / 2) + 'px');
    },
    
    parseUrl: function(href) {
        var queryString = href.match(/\?(.+)/)[1];
        var params = queryString.parseQueryString();
    
        var element = $(params['copyto']);
        return element ? element : null;
    }
});

var UserGroupSelector = new Class({
    Extends: Popup,
    list: null,
    /*copyTo: null,*/
    
    initialize: function(id, element) {
        var href = element.getProperty("href");
        element.setProperty("id", id);
        
        this.parent({window: id + "-window", title: element.getProperty("title")});
        
        this.htmlRequest = new Request.HTML({   method: 'get',
                                                update: this.options.window.getProperty("id") + "-content",
                                                onComplete: function() {
                                                    this.show();
                                                    this.bind();
                                                }.bind(this)
                                            
                                            });
        
        element.addEvent("click", function(e) {
            new Event(e).preventDefault();
            this.makeRequest(href);
        }.bind(this));
        
        this.list = new ItemList({copyTo: this.parseUrl(href)});
    },
    
    bind: function() {
        var lists = this.options.window.getElements("ul");
        
        if(lists) {
            lists.each(function(l) {
                var elements = l.getChildren("li");
                elements.each(function(element) {
                    link = element.getElement("a");
                    
                    link.addEvent('click', function(e, el) {
                        new Event(e).preventDefault();
                        
                        value = el.getElement("span").get("text");
                        this.list.add(value, "g");
                    }.bindWithEvent(this, element));
                }.bind(this));
            }.bind(this));
        }
    }
});

var PathSelector = new Class({
    Extends: Popup,

    copyTo: null,
    
    initialize: function(id, element) {
        var href = element.getProperty("href");
        element.setProperty("id", id);
        
        this.parent({window: id + "-window", title: element.getProperty("title")});
        this.copyTo = this.parseUrl(href);

        this.htmlRequest = new Request.HTML({   method: 'get',
                                                update: this.options.window.getProperty("id") + "-content",
                                                onComplete: function() {
                                                    this.show();
                                                    this.bind();
                                                }.bind(this)
                                            
                                            });
        
        element.addEvent("click", function(e) {
            new Event(e).preventDefault();
            this.makeRequest(href);
        }.bind(this));
    },
    
    bind: function() {
        var pathList = this.options.window.getElement("ul");
        var paths = null;
        var addLink = null;

        if(pathList) {
            paths = pathList.getChildren("li");

            if(paths) {
                paths.each(function(f) {
                    addLink = f.getElement("a.add");
                    gotoLink = f.getElement("a.folder, a.up");
                    
                    if(addLink) {
                        addValue = f.getElement("input[type=hidden]").getProperty("value");
                        addLink.addEvent('click', function(e, value) {
                            new Event(e).preventDefault();
                            this.add(value);
                        }.bindWithEvent(this, addValue));
                    }
                    
                    if(gotoLink) {
                        gotoValue = gotoLink.getProperty("href");
                        gotoLink.addEvent('click', function(e, path) {
                            new Event(e).preventDefault();
                            this.makeRequest(path);
                        }.bindWithEvent(this, gotoValue));
                    }
                }.bind(this));
            }
        }
    },

    add: function(path) {
        if(this.copyTo) {
            this.copyTo.setProperty("value", path);
        }
    },
    
    remove: function() {
        if(this.copyTo) {
            this.copyTo.setProperty("value") = "";
        }
    }
});    
