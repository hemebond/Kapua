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
from django.forms import ModelForm
from kapua.courses.models import Course, Page
from mptt.forms import TreeNodeChoiceField, TreeNodePositionField

class CourseForm(ModelForm):
	class Meta:
		model = Course


class PageForm(ModelForm):
	target = TreeNodeChoiceField(queryset=None, required=False)
	position = TreeNodePositionField(required=False)

	class Meta:
		model = Page
		fields = ('name', 'content', 'target', 'position')

	def __init__(self, root, node=None, *args, **kwargs):
		super(PageForm, self).__init__(*args, **kwargs)

		# Use some friendlier names
		position_choices = (
			('', ''),
			('first-child', _("Under")),
			('left', _("Before")),
			('right', _("After"))
		)

		if node:
			# Exclude the root node (the course) and the current page tree from the list of possible targets
			valid_targets = root.get_descendants().exclude(Q(lft__gte=node.lft) & Q(rght__lte=node.rght))
		else:
			# Exclude the root node (the course) from the list of possible targets
			valid_targets = root.get_descendants()

		print valid_targets

		self.fields['target'].queryset = valid_targets
		self.fields['position'].choices = position_choices
