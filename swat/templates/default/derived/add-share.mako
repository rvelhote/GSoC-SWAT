<%inherit file="/default/base/base.mako" />
<%namespace name="toolbar" file="/default/component/toolbar.mako" />

${toolbar.write(request.environ['pylons.routes_dict']['controller'], 'add')}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: Dashboard
</%def>