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

import datetime

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db import models
#from django.contrib.auth.models import User
from kapua.students.models import Student
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from attachments.models import Attachment
from kapua.models import TreeNode


class SubjectGroup(models.Model):
	"""
		A group of subjects. Provided by the MoE.
	"""
	name = models.CharField(max_length=64)
	slug = models.SlugField()

	def __unicode__(self):
		return self.name

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		return super(SubjectGroup, self).save()

	class Meta:
		ordering = ['name']


class Subject(models.Model):
	"""
		Subject list. Provided by the MoE.
	"""
	ministry_code = models.CharField(max_length=4)
	name = models.CharField(max_length=64)
	slug = models.SlugField()
	group = models.ForeignKey(SubjectGroup)

	def __unicode__(self):
		return u"%s" % self.name

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		return super(Subject, self).save()

	class Meta:
		verbose_name = _('Subject')
		ordering = ['name']


class InstructionalYearLevel(models.Model):
	"""
		Describes the level of the course.
		For MoE returns.
		[34] Instructional year level (for subjects 1-15)
	"""
	ministry_code = models.CharField(max_length=4)
	description = models.CharField(max_length=32)

	def __unicode__(self):
		return self.description

	class Meta:
		verbose_name = _('Instructional Year Level')


class Assessment(models.Model):
	"""
		An assessment can be attached to anything and allow students to
		make submissions to it. There will be different types of submissions
		and some will allow online testing.
	"""
	name = models.CharField(max_length=32, blank=True, null=True)
	# Generic relationship to link to courses, topics or activities
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')

	class Meta:
		verbose_name = _('Assessment')

	def __unicode__(self):
		return self.name


class Course(models.Model):
	"""
		This is the main object that the others point to. It's a collection
		of activities, assessments and learning materials.
	"""
	subject = models.ForeignKey(Subject, blank=True, null=True)
	instructional_year_level = models.ForeignKey(InstructionalYearLevel, blank=True, null=True)
	# Need a way to track the learning level of a course for primary school
	#level = models.Something()
	name = models.CharField(max_length=64)
	short_name = models.CharField(max_length=16,
								  help_text="A short code-name for this course.",
								  blank=True,
								  null=True)
	content = models.TextField(_('Content'))

	treenode = generic.GenericRelation(TreeNode)
	attachments = generic.GenericRelation(Attachment)
	assessments = generic.GenericRelation(Assessment)

	# change tracking
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

	@models.permalink
	def get_absolute_url(self):
		return ('kapua_course_detail', [str(self.pk)])

	def __unicode__(self):
		return unicode(self.name)

	def save(self, *args, **kwargs):
		created = self.pk == None
		super(Course, self).save(*args, **kwargs)

		if created:
			TreeNode.objects.create(content_type=ContentType.objects.get_for_model(Course), object_id=self.id)

	class Meta:
		verbose_name = _('Course')


class Page(models.Model):
	"""
		A course page is like a university "paper"; a small component
		grouped with other components to make up a course.
	"""
	course = models.ForeignKey(Course)
	name = models.CharField(max_length=64)
	content = models.TextField(_('Content'))
	nodes = generic.GenericRelation(TreeNode)
	assessments = generic.GenericRelation(Assessment)
	attachments = generic.GenericRelation(Attachment)

	# change tracking
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('kapua_page_detail', [str(self.pk)])


#class GradeSystem(models.Model):
#	name = models.CharField(max_length=64)
#
#class GradeComponent(models.Model):
#	name = models.CharField(max_length=64)
##	type = models.
#
#class GradeComponentType(models.Model):
#	pass

class Grade(models.Model):
	"""
		This is the score for an assessment for a particular student.
	"""
	assessment = models.ForeignKey(Assessment)
	student = models.ForeignKey(Student)
	score = models.DecimalField(max_digits=10, decimal_places=9, blank=True, null=True)

class Submission(models.Model):
	"""
		Students make a submission for an assessment.
	"""
	assessment = models.ForeignKey(Assessment)
	student = models.ForeignKey(Student)
	created = models.DateTimeField()

class Schedule(models.Model):
	"""
		This is a calendar.
	"""
	name = models.CharField(max_length=32)
	course = models.ForeignKey(Course)

	# change tracking
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

	def __unicode__(self):
		return self.name

	def get_current_students(self):
		# ToDo
		return Enrolment.objects.filter(pk=self.pk) \
				.filter(start__lte=datetime.date.today()) \
				.filter(end__gte=datetime.date.today())

class Activity(models.Model):
	"""
		This is like a calendar event.
	"""
	schedules = models.ManyToManyField(Schedule, related_name="activities")
	subject = models.CharField(max_length=64)
	track_attendance = models.BooleanField(default=True)
	assessments = generic.GenericRelation(Assessment)
	start = models.DateTimeField()
	end = models.DateTimeField()

	# change tracking
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

	def __unicode__(self):
		return self.subject

	class Meta:
		verbose_name = _('Activity')
		verbose_name_plural = _('Activities')

class AttendanceCode(models.Model):
	"""
		Ministry-provided codes that the administrator uses to categorise
		the students absense.
	"""
	code = models.CharField(max_length=1, primary_key=True)
	in_class = models.BooleanField()
	reason = models.CharField(max_length=128)
	explanation = models.TextField()
	audit_code = models.CharField(max_length=1)
	truancy_code = models.CharField(max_length=1)
	half_day_calc = models.BooleanField()

	def __unicode__(self):
		return self.code

class Attendance(models.Model):
	"""
		Was the student at the activity?
	"""
	activity = models.ForeignKey(Activity)
	student = models.ForeignKey(Student)
	code = models.ForeignKey(AttendanceCode)

class Enrolment(models.Model):
	"""
		A student is enrolled in a course schedule for a length of time.
		Their calendar will collect activities, for this schedule, during the
		period they are enrolled.
	"""
	student = models.ForeignKey(Student)
	schedule = models.ForeignKey(Schedule)
	start = models.DateField()
	end = models.DateField()
