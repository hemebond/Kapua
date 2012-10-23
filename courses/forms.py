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

from mptt.forms import TreeNodeChoiceField, TreeNodePositionField

from .models import Course, Page


class CourseForm(forms.ModelForm):
	class Meta:
		model = Course


class PageForm(forms.ModelForm):
	POSITIONS = (
		('right', _("After")),
		('left', _("Before")),
		('first-child', _("Under")),
	)

	class Meta:
		model = Page
		exclude = ('course', 'parent', )

	def __init__(self, valid_targets=None, *args, **kwargs):
		super(PageForm, self).__init__(*args, **kwargs)

		instance = kwargs.get('instance')

		if instance:
			# Exclude the root node (the course) and the current page tree from
			# the list of possible targets
			valid_targets = instance.get_root().get_descendants().exclude(
				Q(lft__gte=instance.lft) & Q(rght__lte=instance.rght)
			)

		if valid_targets:
			self.fields['target'] = TreeNodeChoiceField(
				required=False,
				queryset=valid_targets,
			)
			self.fields['position'] = TreeNodePositionField(
				required=False,
				choices=self.POSITIONS,
			)
