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
from kapua.courses.views import *

urlpatterns = patterns('kapua.courses.views',
	url(r'^$', CourseList.as_view(), name="kapua_course_list"),
	url(r'^add/$', CourseAdd.as_view(), name="kapua_course_add"),
	url(r'^(?P<pk>\d+)/$', CourseDetail.as_view(), name="kapua_course_detail"),
	url(r'^(?P<pk>\d+)/edit/$', CourseEdit.as_view(), name="kapua_course_edit"),
	url(r'^(?P<pk>\d+)/add/$', PageAdd.as_view(), name="kapua_page_add"),
	url(r'^page/(?P<pk>\d+)/$', PageDetail.as_view(), name="kapua_page_detail"),
	url(r'^page/(?P<pk>\d+)/edit/$', PageEdit.as_view(), name="kapua_page_edit"),
)
