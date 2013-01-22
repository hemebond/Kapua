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
from django.views.generic import TemplateView

#from kapua.locations.models import Location
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from kapua.locations.models import Location, LocationType, Country
from kapua.locations.forms import LocationForm


class LocationAdd(TemplateView):
	template_name = "locations/location_add.html"

	def post(self, request, *args, **kwargs):
		LocationFormSet = self.get_formset()
		formset = LocationFormSet(**self.get_formset_kwargs())
		form = LocationForm(request.POST, request.FILES)

		if form.is_valid():
			country = Country.objects.get(pk=int(form.cleaned_data["country"]))
		else:
			country = None

		#print request.POST
		#print formset.has_changed()

		for f in formset.forms:
			#print f._changed_data
			if f.has_changed():
				print f.data
				print f.initial

		if country and formset.is_valid():
			#print "is valid"
			cur_loc = country
			for d in formset.cleaned_data:
				#print d
				try:
					location = Location.objects.get(name__iexact=d["name"], type=d["type"])
				except:
					location = Location(d)

				cur_loc = location

			print cur_loc

		return HttpResponseRedirect('')

	def get_formset_kwargs(self):
		kwargs = {'queryset': Location.objects.none(),
		          'initial': [{'name': '', 'type': LocationType.objects.get(name='City')},
		                      {'name': '', 'type': LocationType.objects.get(name='Suburb')}]}
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})
		return kwargs

	def get_formset(self):
		return modelformset_factory(Location, extra=3, fields=['name', 'type'])

	def get_context_data(self, **kwargs):
		context = super(LocationAdd, self).get_context_data(**kwargs)

		LocationFormSet = self.get_formset()
		context['formset'] = LocationFormSet(**self.get_formset_kwargs())
		#print dir(context['formset'])
		context['form'] = LocationForm()
		return context
