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

from django.db import models
from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory
from django.shortcuts import HttpResponseRedirect
from kapua.locations.models import Location, LocationType


class LocationForm(forms.Form):
	COUNTRIES = (
		(x.id, x.name) for x in Location.objects.filter(type__name="country")
	)
	country = forms.CharField(
		max_length=255,
		widget=forms.Select(choices=COUNTRIES)
	)


LocationFormSet = modelformset_factory(Location, fields=['type', 'name'])
