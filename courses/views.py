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

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from kapua.courses.models import *
from kapua.courses.forms import *
from django.views.generic import ListView, TemplateView, DetailView
from django.core.urlresolvers import reverse
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse

#def index(request):
#	courses = Course.objects.all()

#	s_ids = courses.values_list('subject', flat=True).distinct()
#	subjects = Subject.objects.filter(pk__in=s_ids)

#	g_ids = subjects.values_list('group', flat=True).distinct()
#	groups = SubjectGroup.objects.filter(pk__in=g_ids)

#	mylist = {}

#	for group in groups:
#		mylist[group.pk] = [group, {}]

#	for subject in subjects:
#		mylist[subject.group.pk][1][subject.pk] = [subject, []]

#	for course in courses:
#		mylist[course.subject.group.pk][1][course.subject.pk][1].append(course)

#	return render_to_response('courses/index.html', {
#			'mylist': mylist
#		},
#		context_instance=RequestContext(request)
#	)

class SubjectListView(ListView):
#	context_object_name = "list"
#	template_name = "books/books_by_publisher.html",

	def get_queryset(self):
		print self.kwargs['subjectgroup']
		group = get_object_or_404(SubjectGroup, slug__iexact=self.kwargs['subjectgroup'])
		return Subject.objects.filter(group=group)

class CourseListView(ListView):
	template_name = "courses/course_list.html"

	def get_queryset(self):
		qs = Course.objects.all()
		try:
#			subject = get_object_or_404(Subject, slug__iexact=self.kwargs['subject'])
			subject = get_object_or_404(Subject, pk=self.kwargs['subject'])
			qs = qs.filter(subject=subject)
		except:
			pass
		return qs

def course_list(request):
	courses = Course.objects.all()
	return render_to_response('courses/course_list.html', {
			'object_list': courses,
		},
		context_instance=RequestContext(request)
	)

def course_detail(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)
	object_type = ContentType.objects.get_for_model(course)
	o = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=course.id)
	return render_to_response('courses/course_detail.html', {
			'object': o,
			'prev': o.previous(),
			'next': o.next(),
		},
		context_instance=RequestContext(request)
	)

def course_edit(request, course_pk=None ):
	if course_pk:
		o = get_object_or_404(Course, pk=course_pk)
	else:
		o = Course()

	if request.method == 'POST':
		form = CourseForm(request.POST, instance=o, prefix="course")

		if form.is_valid():
			form.save()
			print "o.od: %s" % o.id
			if request.POST['_continue']:
				return HttpResponseRedirect(reverse('course_edit', args=(o.id,)))
			return HttpResponseRedirect(reverse('kapua.courses.views.course_detail', args=(o.id,)))
	else:
		form = CourseForm(instance=o, prefix="course")

	return render_to_response('courses/course_edit.html', {'form': form, 'object': o}, context_instance=RequestContext(request))

def page_detail(request, page_pk):
	page = get_object_or_404(Page, pk=page_pk)
	object_type = ContentType.objects.get_for_model(page)
	o = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=page.id)
	return render_to_response("courses/page_detail.html", {
			"object": o,
			'prev': o.previous(),
			'next': o.next(),
		},
		context_instance=RequestContext(request)
	)

def page_edit(request, course_pk=None, page_pk=None):
	if page_pk:
		o = get_object_or_404(Page, pk=page_pk)
	else:
		o = Page()
		if course_pk:
			o.course = Course.objects.get(pk=course_pk)
		
	if request.method == 'POST':
		form = PageForm(request.POST, instance=o, prefix="page")

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(o.get_absolute_url())
	else:
		form = PageForm(instance=o, prefix="page")

	return render_to_response('courses/page_edit.html', {'form': form, 'object': o}, context_instance=RequestContext(request))

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm
def page_move(request, page_pk):
	page = get_object_or_404(Page, pk=page_pk)
	object_type = ContentType.objects.get_for_model(page)
	o = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=page.id)

	if request.method == 'POST':
		form = MoveNodeForm(o, request.POST)
		if form.is_valid():
			try:
				o = form.save()
				return HttpResponseRedirect(o.get_absolute_url())
			except InvalidMove:
				pass
	else:
		form = MoveNodeForm(o)
	
	return render_to_response('courses/page_move.html', {
        'form': form,
        'page': o,
        'page_tree': TreeNode.tree.all(),
    }, context_instance=RequestContext(request))