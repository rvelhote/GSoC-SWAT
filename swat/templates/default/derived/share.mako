<%inherit file="/default/base/base.mako" />
<%namespace name="toolbar" file="/default/component/toolbar.mako" />

${parent.action_title(c.controller_config.get_action_info('page_title'))}
${toolbar.write(c.controller_config.get_toolbar_items())}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: ${c.controller_config.get_action_info('page_title')}
</%def>