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

from django import forms
from django.forms.models import inlineformset_factory
from kapua.people.models import Person, Relationship


class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ('legal_first_name', 'middle_names', 'legal_last_name', 'gender')


class PersonEditForm(forms.ModelForm):
	class Meta:
		model = Person
		exclude = ("first_name", "last_name")


RelationshipFormSet = inlineformset_factory(
	Person,
	Relationship,
	fk_name="person",
	fields=(
		'related_person',
		'relationship_type',
	)
)
