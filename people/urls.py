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
from kapua.people.views import *

urlpatterns = patterns('kapua.people.views',
	url(r'^$', PersonList.as_view(), name="kapua_person_list"),
	url(r'^add/$', PersonAdd.as_view(), name="kapua_person_add"),
	url(r'^(?P<pk>\d+)/$', PersonDetail.as_view(), name="kapua_person_detail"),
	url(r'^(?P<pk>\d+)/edit/$', PersonEdit.as_view(), name="kapua_person_edit"),
)
