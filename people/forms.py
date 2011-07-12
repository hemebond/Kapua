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
from django.forms import ModelForm, RadioSelect
from kapua.forms import FormMixin
from django.shortcuts import HttpResponseRedirect
from kapua.people.models import Person, Address, Relationship

class PersonForm(ModelForm):
	class Meta:
		model = Person

class PersonEditForm(FormMixin, ModelForm):
	class Meta:
		model = Person
		fields = ('legal_last_name', 'legal_first_name', 'gender', 'birth_date', 'ethnicity', 'iwi', 'citizenship', 'privacy_indicator', 'middle_names', 'preferred_first_name', 'preferred_last_name', 'residence',)

