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
from django.views.generic import ListView, DetailView
from kapua.courses.views import *
from kapua.courses.models import Course, SubjectGroup

urlpatterns = patterns('kapua.courses.views',
#	url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Course, template_name="courses/course_detail.html"), name='course_detail'),
	(r'^$', 'course_list'),
	(r'^add/$', 'course_edit', {}, 'course_add'),
	(r'^(?P<course_pk>\d+)/$', 'course_detail'),
	(r'^(?P<course_pk>\d+)/edit/$', 'course_edit', {}, 'course_edit'),
	(r'^(?P<course_pk>\d+)/add/$', 'page_edit', {}, 'page_add'),
	(r'^pages/(?P<page_pk>\d+)/$', 'page_detail'),
	(r'^pages/(?P<page_pk>\d+)/edit/$', 'page_edit'),
	(r'^pages/(?P<page_pk>\d+)/move/$', 'page_move'),
#	(r'^by_subject/(?P<subject_group>[-\w]+)/(?P<subject>[-\w]+)/$', CourseListView.as_view()),
	url(r'^(?P<subjectgroup>[-\w]+)/(?P<subject>\d+)/$', CourseListView.as_view(), name="course_list"),
	url(r'^(?P<slug>[-\w]+)/$', DetailView.as_view(model=SubjectGroup, template_name="courses/subjectgroup_detail.html"), name="subjectgroup_detail"),
#	(r'^$', ListView.as_view(model=Course)),
#	(r'^add/$', "add"),
)
