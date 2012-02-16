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
from django.forms import ModelForm, RadioSelect, Textarea
from kapua.forms import FormMixin, HTMLEditorWidget
from django.shortcuts import HttpResponseRedirect
from kapua.courses.models import Course, Page

class CourseForm(ModelForm):
	class Meta:
		model = Course
	
	class Media:
		js = (
			'js/jquery/jquery-1.6.2.js',
			'js/jquery/ui/jquery.ui.core.js',
			'js/jquery/ui/jquery.ui.widget.js',
			'js/jquery/ui/jquery.ui.mouse.js',
			'js/jquery/ui/jquery.ui.sortable.js',
			'js/jquery.cookie.js',
			'js/jquery.ui.nestedSortable.js',
		)
		css = {
			'screen': (
				'admin/css/page_tree.css',
			)
		}

class PageForm(ModelForm):
	class Meta:
		model = Page
		widgets = {
				'content': HTMLEditorWidget(attrs={'class': 'wymeditor',}),
		}