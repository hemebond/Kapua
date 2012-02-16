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

from django.forms import Form, ModelForm, Textarea

class FormMixin(object):
	def as_div(self):
		"Returns this form rendered as HTML <div>s."
		return self._html_output(
			normal_row = u'<div%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</div>',
			error_row = u'<p>%s</p>',
			row_ender = '</div>',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = False)

	def __unicode__(self):
		return self.as_div()

	class Meta:
		abstract = True

class HTMLEditorWidget(Textarea):
	class Media:
		js = (
			'wymeditor/jquery/jquery.js',
			'wymeditor/jquery/jquery-ui-1.8.11.custom.min.js',
			'wymeditor/wymeditor/jquery.wymeditor.js',
			'wymeditor/wymeditor/plugins/hovertools/jquery.wymeditor.hovertools.js',
			'wymeditor/wymeditor/plugins/resizable/jquery.wymeditor.resizable.js',
			'wymeditor/settings.js',
			'wymeditor/init.js',
		)
		css = {
			'screen': (
				'wymeditor/jquery/jquery.ui.resizable.css',
			)
		}