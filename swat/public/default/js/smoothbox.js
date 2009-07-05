/*
 * Smoothbox v20080623 by Boris Popoff (http://gueschla.com)
 * To be used with mootools 1.2
 *
 * Based on Cody Lindley's Thickbox, MIT License
 *
 * Licensed under the MIT License:
 *   http://www.opensource.org/licenses/mit-license.php
 */
window.addEvent('domready', TB_init);

var TB_isActive = false;
var TB_htmlRequest = null;

var TB_elementName = "TB_window";
var TB_contentElementName = "TB_ajaxContent";

function TB_init() {
    $$("a.popup-selector").each(function(el){
	el.addEvent("click", TB_bind);
    });
    
    document.addEvent("keyup", function(event){
	event = new Event(event);
	if (event.code == 27) {
	    TB_remove();
	}
    });
    
    TB_htmlRequest = new Request.HTML({method: 'get', update: TB_contentElementName, onComplete: handlerFunc})
}

function handlerFunc() {
    TB_position();
    TB_showWindow();
};

function TB_bind(e){
    new Event(e).preventDefault();    
    this.blur();

    var caption = this.getProperty("title") || this.getProperty("name") || "";
    var url = this.getProperty("href");

    TB_show(caption, url);
    
    var queryString = url.match(/\?(.+)/)[1];
    var params = queryString.parseQueryString();
    
    userGroup.options.copyTo = params['copyto'];
}

function TB_show(caption, url) {
    /**
     *	Only one Popup Window is Allowed at a time
     */
    if(TB_isActive) {
	return;
    }
    
    var tb = $(TB_elementName);
    TB_isActive = true;
    
    if (!tb) {
        new Element('div').setProperty('id', TB_elementName).injectInside(document.body);
	new Drag(TB_elementName, {handle:'TB_title'})
	
	tb = $(TB_elementName);
	
        tb.setOpacity(0);
	tb.addClass("round-2px");
	
	tb.innerHTML += "<div id='TB_title'><div id='TB_ajaxWindowTitle'></div><div id='TB_closeAjaxWindow'><a href='#' id='TB_closeWindowButton'>close</a></div></div><div id='TB_ajaxContent'></div>";
	$("TB_closeWindowButton").onclick = TB_remove;
    }
    
    $('TB_ajaxWindowTitle').set("text", caption);
    TB_htmlRequest.get(url);
}

function TB_showWindow() {
    var tb = $(TB_elementName);
    
    if(tb) {
	tb.set('tween', {duration: 250});
        tb.fade("in");
    }
}

function TB_remove() {
    var tb = $(TB_elementName);
    TB_isActive = false;
    
    if(tb) {
	tb.set('tween', {duration: 250});
	tb.fade("out");
    }
    
    return false;
}

function TB_position() {
    var tb = $(TB_elementName);
    
    if(tb) {
	tb.set('morph', {duration: 75});

	tb.morph({
	    left: (window.getScrollLeft() + (window.getWidth() - tb.getStyle("width").toInt()) / 2) + 'px',
	    top: (window.getScrollTop() + (window.getHeight() - tb.getStyle("height").toInt()) / 2) + 'px'
	});	
    }
}
