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
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import Form, ModelForm

from kapua.students.models import Student
from kapua.people.models import Person
from kapua.people.forms import PersonEditForm


class StudentForm(ModelForm):
	class Meta:
		model = Student
		exclude = ('person',)

	def __init__(self, *args, **kwargs):
		super(StudentForm, self).__init__(*args, **kwargs)


class StudentPersonForm(PersonEditForm):
	def __init__(self, *args, **kwargs):
		super(StudentPersonForm, self).__init__(*args, **kwargs)

		self.fields['ethnicity'].required = True


class PersonSelectForm(Form):
	person = forms.ModelChoiceField(queryset=Person.objects.all(), empty_label=None)