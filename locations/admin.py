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

from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.contrib import admin
from django import forms

from mptt.admin import MPTTModelAdmin

from .models import *
from .forms import *

# class EventInlines(admin.StackedInline):
# 	model = Event

# class CourseAdmin(admin.ModelAdmin):
# 	inlines = [EventInlines]
# 	list_display = ('name', 'short_name', 'subject')
# 	list_filter = ('subject',)
# 	form = CourseForm

# 	def save_formset(self, request, form, formset, change):
# 		instances = formset.save(commit=False)
# 		for instance in instances:
# 			instance.creator = request.user
# 			instance.save()
# 		formset.save_m2m()

# class PageAdmin(admin.ModelAdmin):
# 	form = PageForm

# 	def save_formset(self, request, form, formset, change):
# 		instances = formset.save(commit=False)
# 		for instance in instances:
# 			instance.creator = request.user
# 			instance.save()
# 		formset.save_m2m()

# class SubjectGroupAdmin(admin.ModelAdmin):
# 	fields = ('name',)

# class EnrolmentAdmin(admin.ModelAdmin):
# 	list_display = ('course_and_schedule', 'student')
# 	list_filter = ('schedule__course', 'schedule', 'student')

# 	def course_and_schedule(self, obj):
# 		return "%s / %s" % (obj.schedule.course, obj.schedule)
# 	course_and_schedule.short_description = "Course and Schedule"


class CountryAdmin(admin.ModelAdmin):
	list_display = ('name', 'code_alpha2', 'code_alpha3', 'code_numeric')


class LocationAdmin(admin.ModelAdmin):
	list_display = ('name', 'type')


class LocationTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'level')

admin.site.register(Location, MPTTModelAdmin)
admin.site.register(LocationType, LocationTypeAdmin)
admin.site.register(Country, CountryAdmin)
