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

from django.forms.models import modelformset_factory, inlineformset_factory

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import View, ListView, CreateView, UpdateView, DetailView, TemplateView
from kapua.people.models import Person, Relationship
from kapua.people.forms import PersonForm, PersonEditForm, RelationshipFormSet
from operator import attrgetter

class PersonList(ListView):
	model = Person


class PersonAdd(CreateView):
	template_name = "people/person_edit.html"
	form_class = PersonForm

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(PersonAdd, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		self.object = form.save()
		kwargs = self.get_form_kwargs()
		if "_continue" in kwargs.get("data"):
			return HttpResponseRedirect(reverse('kapua_person_edit', kwargs={"pk":self.object.pk}))

		return super(PersonAdd, self).form_valid(form)


class PersonDetail(DetailView):
	model = Person


class PersonEdit(TemplateView):
	template_name = "people/person_edit.html"
	form_class = PersonEditForm
	model = Person

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(PersonEdit, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		person_pk = self.kwargs.get('pk', None)
		person = get_object_or_404(Person, pk=person_pk)

		formset = RelationshipFormSet(self.request.POST, self.request.FILES, instance=person)
		form = PersonEditForm(self.request.POST, self.request.FILES, instance=person)

		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect(person.get_absolute_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, relationship_formset=formset))

	def get_context_data(self, **kwargs):
		context = super(PersonEdit, self).get_context_data(**kwargs)

		if not self.request.POST:
			person_pk = self.kwargs.get('pk', None)
			person = get_object_or_404(Person, pk=person_pk)
			context['form'] = PersonEditForm(instance=person)

			formset = RelationshipFormSet(instance=person)
			context['relationship_formset'] = formset

		return context