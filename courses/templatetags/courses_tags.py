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

from django import template
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from kapua.courses.models import Course
from kapua.models import TreeNode

register = template.Library()

@register.inclusion_tag('courses/moveable_page_list.html')
def display_moveable_page_list(course_id):
	course = get_object_or_404(Course, id=course_id)
	object_type = ContentType.objects.get_for_model(course)
	root_node = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=course.id)
	return {
		'course': course,
		'root_node': root_node,
	}
