<%doc>
#
# Edit Share Mako Template file for SWAT
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#   
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#   
# You should have received a copy of the GNU General Public License
# 
</%doc>
<%inherit file="/default/base/base.mako" />
<%namespace name="toolbar" file="/default/component/toolbar.mako" />
<%namespace name="share_form" file="/default/component/share-form.mako" />

${parent.action_title(c.controller_config.get_action_info('page_title'))}
${toolbar.write(c.controller_config.get_toolbar_items())}

${share_form.write(c.share_name)}

<%doc></%doc>
<%def name="page_title()">
    ${parent.page_title()} :: ${c.controller_config.get_action_info('page_title')}
</%def>
