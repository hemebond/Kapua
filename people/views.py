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
from kapua.people.models import Person

def index(request):
	people_list = Person.objects.all().order_by('last_name', 'first_name')
	return render_to_response('people/index.html', {'people_list': people_list})

def detail(request, person_id):
	p = get_object_or_404(Person, pk=person_id)
	return render_to_response('people/detail.html', {'person': p})

