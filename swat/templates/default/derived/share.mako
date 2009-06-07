<%inherit file="/default/base/base.mako" />
<%namespace name="toolbar" file="/default/component/toolbar.mako" />

${parent.action_title('Share Management')}
${toolbar.write(request.environ['pylons.routes_dict']['controller'])}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: Dashboard
</%def>