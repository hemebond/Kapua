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


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, \
                                 FormView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .models import Course, Page
from .forms import CourseForm, PageForm


class CourseList(ListView):
	model = Course


class CourseAdd(CreateView):
	template_name = "courses/course_edit.html"
	form_class = CourseForm
	context_object_name = "course"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(CourseAdd, self).dispatch(*args, **kwargs)


class CourseDetail(DetailView):
	template_name = "courses/course_detail.html"
	model = Course
	context_object_name = "course"

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()

		if self.object.pages.exists():
			return redirect('kapua-page-detail', self.object.pages.get(level=0).pk)

		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)


class CourseEdit(UpdateView):
	template_name = "courses/course_edit.html"
	form_class = CourseForm
	model = Course


class PageAdd(SingleObjectMixin, FormView):
	model = Course
	template_name = "courses/page_edit.html"
	form_class = PageForm

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(PageAdd, self).dispatch(*args, **kwargs)

	def get_form(self, form_class):
		self.object = self.get_object()
		return super(PageAdd, self).get_form(form_class)

	def get_form_kwargs(self):
		"""
		Returns the keyword arguments for instantiating the form.
		"""
		form_kwargs = super(PageAdd, self).get_form_kwargs()

		form_kwargs.update({
			'valid_targets': self.object.pages.filter(level__gt=0)
		})

		return form_kwargs

	def form_valid(self, form):
		position = form.cleaned_data.get('position', 'last-child')
		target = form.cleaned_data.get('target', None)
		course = self.object

		page = form.save(commit=False)
		page.course = course

		if not target:
			if course.pages.exists():
				target = course.pages.get(level=0)
				position = 'last-child'

		if target:
			page.insert_at(
				target=target,
				position=position,
				save=True,
			)
			self.success_url = page.get_absolute_url()
		else:
			page.save()
			self.success_url = course.get_absolute_url()

		return super(PageAdd, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(PageAdd, self).get_context_data(*args, **kwargs)

		if context['form'].errors:
			context['error_message'] = context['form'].errors

		return context


class PageDetail(DetailView):
	template_name = "courses/page_detail.html"
	context_object_name = "page"
	model = Page

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(PageDetail, self).get_context_data(**kwargs)
		context['course'] = self.object.course
		pages = context['course'].pages.all()

		for index, page in enumerate(pages):
			if page.pk == self.object.pk:
				if index > 0:
					context['previous_page'] = pages[index - 1]

				if index < (len(pages) - 1):
					context['next_page'] = pages[index + 1]

				break

		# Remove the root page
		context['pages'] = pages.filter(level__gt=0)

		# This gets the ancestors of the current page but exluces the
		# root page
		context['breadcrumbs'] = pages.filter(
			lft__lt=self.object.lft,
			rght__gt=self.object.rght
		).exclude(
			level=0
		)

		return context


class PageEdit(UpdateView):
	template_name = "courses/page_edit.html"
	form_class = PageForm
	model = Page

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(PageEdit, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		self.object = form.save()

		target = form.cleaned_data.get('target')
		if target:
			position = form.cleaned_data.get('position')
			self.object.move_to(
				target=target,
				position=position
			)

		return redirect('kapua-page-detail', self.object.pk)
