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
from kapua.students.views import StudentList, StudentAdd, StudentDetail, StudentEdit

urlpatterns = patterns('kapua.students.views',
	url(r'^$', StudentList.as_view(), name="kapua_student_list"),
	url(r'^add/$', StudentAdd.as_view(), name="kapua_student_add"),
	url(r'^(?P<pk>\d+)/$', StudentDetail.as_view(), name="kapua_student_detail"),
	url(r'^(?P<pk>\d+)/edit/$', StudentEdit.as_view(), name="kapua_student_edit"),
)
