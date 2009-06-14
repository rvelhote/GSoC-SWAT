#
# Test Cases for Authentication Controller
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
from swat.tests import *
from swat.lib.helpers import ControllerConfiguration, DashboardConfiguration, \
BreadcrumbTrail, SwatMessages

class TestLoginController(TestController):

    def test_login(self):
        response = self.app.get(url(controller='login', action='login'))
        # Test response...

    def test_logout(self):
        response = self.app.get(url(controller='login', action='logout'))
        # Test response...