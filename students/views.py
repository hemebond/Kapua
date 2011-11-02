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

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from kapua.students.models import Student

#if "django.contrib.comments" in settings.INSTALLED_APPS:
#	print "Comments are enabled"

def index(request):
	student_list = Student.objects.all()
	return render_to_response('students/index.html', {
			'student_list': student_list
		},
		context_instance=RequestContext(request)
	)

def detail(request, student_id):
	s = get_object_or_404(Student, pk=student_id)
	return render_to_response('students/detail.html', {
			'student':s,
		},
		context_instance=RequestContext(request)
	)
