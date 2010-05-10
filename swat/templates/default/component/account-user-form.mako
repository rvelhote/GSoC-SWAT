<%doc>
#
# User Account Editing Form Mako Template file for SWAT
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

<%namespace name="field" file="/default/component/form-fields.mako" />

<%def name="write()">
    ${h.form('', method="post", id="share-form", class_="share-configuration")}
        <ol class="tab-list">
            <li id="tab1" class="active">
                <h3><a title="${_('Basic User Configuration')}" class="title-icon basic-tab" href="#">${_('Basic')}</a></h3>                           
            </li>              
        </ol>
    
        <ul class="tab-list-items"> 
            <li id="content-tab1" class="active tab">
                <ol class="col-1">
                    <li>${field.put("username", "x")}</li>
                    <li>${field.put("fullname", "y")}</li>
                    <li>${field.put("description", "y")}</li>
                    <li>${field.put("password", "y")}</li>
                    <li>${field.put("confirmpassword", "y")}</li>
                </ol>
            </li>
        </ul>
    ${h.end_form()}
</%def>
