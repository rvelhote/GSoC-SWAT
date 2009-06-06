<%inherit file="/default/base/base.mako" />
<%namespace name="widget" file="/default/component/widget.mako" />

${widget.get_all("dashboard")}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: Dashboard
</%def>