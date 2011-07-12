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
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from kapua.address.models import Address, Country
from kapua.people.models import Person
from kapua.address.forms import AddressForm

def index(request):
	a = Address.objects.all().order_by('country', 'city', 'suburb', 'street', 'number')
	return render_to_response('address/index.html', {
			'addresses':a
		}
	)

def detail(request, address_id):
	a = get_object_or_404(Address, pk=address_id)
	r = Person.objects.filter(residence=a)
	return render_to_response('address/detail.html', {
			'address':a,
			'residents':r,
		},
		context_instance=RequestContext(request)
	)

def edit(request, address_id):
	address = get_object_or_404(Address, pk=address_id)
	if request.method == 'POST':
		print "User submitted new data"
		form = AddressForm(request.POST, instance=person)
		if form.is_valid():
			print "Form is valid"
			form.save()
			return HttpResponseRedirect(reverse('kapua.address.views.detail', args=(address.id,)))
		else:
			print "Form is not valid"
			print form.errors
			return render_to_response('address/edit.html', {'form': form}, context_instance=RequestContext(request))
	
	form = AddressForm(instance=address)
	return render_to_response('address/edit.html', {'form': form}, context_instance=RequestContext(request))

