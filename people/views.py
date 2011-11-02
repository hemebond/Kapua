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

#from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from kapua.people.models import Person, Relationship
from kapua.people.forms import PersonForm, PersonEditForm
from operator import attrgetter

def index(request):
	people_list = sorted(Person.objects.all(), key=attrgetter('last_name', 'first_name'))
	return render_to_response('people/index.html', {
			'people_list':people_list
		},
		context_instance=RequestContext(request)
	)

def detail(request, person_id):
	p = get_object_or_404(Person, pk=person_id)
	change_url = urlresolvers.reverse('admin:people_person_change', args=(p.id,))
	return render_to_response('people/detail.html', {
			'person':p,
			'change_url':change_url,
		},
		context_instance=RequestContext(request)
	)

def edit(request, person_id):
	person = get_object_or_404(Person, pk=person_id)
	if request.method == 'POST':
		person_form = PersonEditForm(request.POST, instance=person, prefix="person")

		if person_form.is_valid():
			return HttpResponseRedirect(reverse('kapua.people.views.detail', args=(person.id,)))
	else:
		person_form = PersonEditForm(instance=person, prefix="person")

	return render_to_response('people/edit.html', {'form': person_form}, context_instance=RequestContext(request))

def add(request):
	form = PersonForm
	if request.method == 'POST':
		print "Got your POST, thanks."
		return HttpResponseRedirect(reverse('kapua.people.views.detail', args=(p.id,)))

	return render_to_response('people/add.html', {'form': form}, context_instance=RequestContext(request))

