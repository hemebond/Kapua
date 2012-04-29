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

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, CreateView, UpdateView, DetailView, TemplateView

from kapua.students.models import Student
from kapua.students.forms import StudentForm, StudentPersonForm
from kapua.people.models import Person


class StudentList(ListView):
	model = Student


class StudentAdd(TemplateView):
	template_name = "students/student_edit.html"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(StudentAdd, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		student_form = StudentForm(self.request.POST, self.request.FILES, prefix="student")

		# A person query string parameter can pre-fill the person form
		person_pk = self.request.GET.get("person", None)
		if person_pk:
			person = get_object_or_404(Person, pk=person_pk)
		else:
			person = None

		person_form = StudentPersonForm(self.request.POST, self.request.FILES, instance=person, prefix="person")

		if student_form.is_valid() and person_form.is_valid():
			person = person_form.save()

			# Add the person to the student record
			student = student_form.save(commit=False)
			student.person = person
			student.save()
			return HttpResponseRedirect(student.get_absolute_url())
		else:
			return self.render_to_response(self.get_context_data(student_form=student_form, person_form=person_form))

	def get_context_data(self, **kwargs):
		context = super(StudentAdd, self).get_context_data(**kwargs)

		# A person query string parameter can pre-fill the person form
		person_pk = self.request.GET.get("person", None)

		if not context.get('student_form', False):
			context['student_form'] = StudentForm(prefix="student")

		if "person_form" not in context:
			if person_pk:
				person = get_object_or_404(Person, pk=person_pk)
			else:
				person = None

			context['person_form'] = StudentPersonForm(instance=person, prefix="person")

		return context


class StudentDetail(DetailView):
	model = Student
	context_object_name = "student"


class StudentEdit(TemplateView):
 	template_name = "students/student_edit.html"

	def post(self, request, *args, **kwargs):
		student_pk = self.kwargs.get('pk', None)
		student = get_object_or_404(Student, pk=student_pk)
		student_form = StudentForm(self.request.POST, self.request.FILES, instance=student, prefix="student")

		# A person query string parameter can pre-fill the person form
		person_pk = student.person_id
		if person_pk:
			person = get_object_or_404(Person, pk=person_pk)
		else:
			person = None

		person_form = StudentPersonForm(self.request.POST, self.request.FILES, instance=person, prefix="person")

		if student_form.is_valid() and person_form.is_valid():
			person = person_form.save()
			student = student_form.save()
			return HttpResponseRedirect(student.get_absolute_url())
		else:
			return self.render_to_response(self.get_context_data(student_form=student_form, person_form=person_form))

	def get_context_data(self, **kwargs):
		context = super(StudentEdit, self).get_context_data(**kwargs)

		student_pk = self.kwargs.get('pk', None)
		student = get_object_or_404(Student, pk=student_pk)

		person_pk = student.person_id

		if not context.get('student_form', False):
			context['student_form'] = StudentForm(instance=student, prefix="student")

		if "person_form" not in context:
			if person_pk:
				person = get_object_or_404(Person, pk=person_pk)
			else:
				person = None

			context['person_form'] = StudentPersonForm(instance=person, prefix="person")

		return context