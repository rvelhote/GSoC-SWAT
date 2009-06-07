<%inherit file="/default/base/base.mako" />
<%namespace name="toolbar" file="/default/component/toolbar.mako" />

% if hasattr(c, "friendly_action"):
    ${parent.action_title(c.friendly_action)}
% else:
    request.environ['pylons.routes_dict']['action']
% endif

${toolbar.write(request.environ['pylons.routes_dict']['controller'], request.environ['pylons.routes_dict']['action'])}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: Dashboard
</%def>

