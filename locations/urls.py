# Copyright 2011 James O'Neill
#
# This file is part of Kapua.
#
# Kapua is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Kapua is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Kapua.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *
from kapua.locations.views import *
from django.views.generic import ListView
from kapua.locations.models import Location

urlpatterns = patterns('kapua.locations.views',
	url(r'^$', ListView.as_view(model=Location), name="kapua_location_list"),
	url(r'^add/$', LocationAdd.as_view(), name="kapua_location_add"),
)
