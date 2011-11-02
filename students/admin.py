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

from kapua.students.models import Student, School
from django.contrib import admin

class StudentAdmin(admin.ModelAdmin):
	list_display = ('ministry_id', '__unicode__', 'year_level')
	list_filter = ('year_level', 'person__gender')
	search_fields = ['person__legal_first_name', 'person__legal_last_name', 'person__preferred_first_name', 'person__preferred_last_name']

admin.site.register(Student, StudentAdmin)

