<%inherit file="/default/base/base.mako" />
<%namespace name="widget" file="/default/component/widget.mako" />

${widget.paint(c.layout)}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: Dashboard
</%def>