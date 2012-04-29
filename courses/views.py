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


from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, CreateView
from django.http import HttpResponseRedirect

from mptt.exceptions import InvalidMove
from kapua.models import TreeNode
from kapua.forms import MoveNodeForm
from kapua.courses.models import *
from kapua.courses.forms import *


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
	
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CourseDetail, self).get_context_data(**kwargs)

		# Add the tree nodes for pages
		object_type = ContentType.objects.get_for_model(self.object)
		treenode = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=self.object.id)

		context['treenode'] = treenode
		context['prev'] = treenode.previous()
		context['next'] = treenode.next()
		
		return context


class CourseEdit(UpdateView):
	template_name = "courses/course_edit.html"
	form_class = CourseForm
	model = Course
	context_object_name = "course"
	
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CourseEdit, self).get_context_data(**kwargs)

		object_type = ContentType.objects.get_for_model(self.object)
		treenode = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=self.object.pk)

		context['treenode'] = treenode
		
		return context


class PageAdd(CreateView):
	template_name = "courses/page_edit.html"
	form_class = PageForm

	def get_course_treenode(self, course_pk):
		"""
		Returns the treenode that points to the course
		"""
		object_type = ContentType.objects.get_for_model(Course)
		return TreeNode.objects.get(content_type__pk=object_type.pk, object_id=course_pk)

	# Have to override this method because PageForm requires the "root" argument
	def get_form_kwargs(self):
		"""
		Returns the keyword arguments for instanciating the form.
		"""
		kwargs = super(PageAdd, self).get_form_kwargs()

		course_pk = self.kwargs.get('pk')
		kwargs.update({'root': self.get_course_treenode(course_pk)})
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None

		course_pk = kwargs.get("pk")
		course = get_object_or_404(Course, pk=course_pk)
		course_treenode = self.get_course_treenode(course_pk)

		form = PageForm(data=self.request.POST, root=course_treenode)

		if form.is_valid():
			self.object = form.save(commit=False)
			self.object.course_id = course_pk
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		self.object = form.save()

		course_treenode = self.get_course_treenode(self.object.course_id)
		node = TreeNode(content_object=self.object, parent=course_treenode)

		position = form.cleaned_data.get('position', None)
		target = form.cleaned_data.get('target', None)
		if not position or not target:
			position = 'last-child'
			target = course_treenode

		node.insert_at(target=target, position=position, save=True)

		return super(PageAdd, self).form_valid(form)


class PageDetail(DetailView):
	template_name = "courses/page_detail.html"
	context_object_name = "page"
	model = Page
	
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(PageDetail, self).get_context_data(**kwargs)
		
		# Add the tree nodes for adjacent pages
		object_type = ContentType.objects.get_for_model(self.object)
		treenode = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=self.object.id)

		context['treenode'] = treenode
		context['prev'] = treenode.previous()
		context['next'] = treenode.next()
		
		return context


class PageEdit(UpdateView):
	template_name = "courses/page_edit.html"
	form_class = PageForm
	model = Page

	# Have to override this method because PageForm requires the "root" and "node" arguments
	def get_form_kwargs(self):
		"""
		Returns the keyword arguments for instanciating the form.
		"""
		kwargs = super(PageEdit, self).get_form_kwargs()

		page_pk = self.kwargs.get('pk')
		node = self.get_page_treenode(page_pk)
		kwargs.update({'root': node.get_root(), 'node': node})

		return kwargs

	def get_page_treenode(self, page_pk):
		"""
		Returns the treenode that points to this page
		"""
		object_type = ContentType.objects.get_for_model(Page)
		return TreeNode.objects.get(content_type__pk=object_type.pk, object_id=page_pk)

	def form_valid(self, form):
		self.object = form.save()

		position = form.cleaned_data.get('position', None)
		if position:
			node = self.get_page_treenode(self.object.pk)
			target = form.cleaned_data.get('target')
			node.move_to(target=target, position=position)

		return super(PageEdit, self).form_valid(form)


class PageMove(UpdateView):
	template_name = "courses/page_move.html"
	model = TreeNode
	form_class = MoveNodeForm

	def get_object(self, queryset=None):
		# Use a custom queryset if provided; this is required for subclasses
		# like DateDetailView
		if queryset is None:
			queryset = self.get_queryset()

		pk = self.kwargs.get(self.pk_url_kwarg, None)
		page = get_object_or_404(Page, pk=pk)
		object_type = ContentType.objects.get_for_model(page)
		treenode = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=pk)

		return treenode
