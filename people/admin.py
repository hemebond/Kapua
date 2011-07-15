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

from django.contrib import admin
from kapua.people.models import Person, Relationship, Residence
import inspect

class RelationshipInline(admin.StackedInline):
	model = Relationship
	fk_name = 'person'
	extra = 1
	exclude = ['reciprocal']

class PersonAdmin(admin.ModelAdmin):
	fieldsets = [
		(
			'Name', {
				'fields' : ['legal_first_name', 'middle_names', 'legal_last_name']
			}
		),
		(
			'Preferred Name', {
				'fields' : ['preferred_first_name', 'preferred_last_name'],
				'classes' : ['collapse']
			}
		),
		(
			None, {
				'fields' : ['photo', 'birth_date', 'gender', 'email', 'phone', 'privacy_indicator', 'residence', 'citizenship', 'ethnicity', 'iwi']
			}
		)
	]
	inlines = [RelationshipInline]
	filter_horizontal = ['ethnicity', 'iwi']

class ResidenceAdmin(admin.ModelAdmin):
	model = Residence

admin.site.register(Person, PersonAdmin)
admin.site.register(Residence, ResidenceAdmin)
