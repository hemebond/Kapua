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

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from kapua.students.models import Student
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from attachments.models import Attachment
from kapua import settings
from kapua.models import TreeNode
from django.db.models.signals import post_save

def create_tree_node(sender, **kwargs):
		if kwargs.get('created', False) and not kwargs.get('raw', False):
			i = kwargs.get('instance')
			if hasattr(i, 'course'):
				object_type = ContentType.objects.get_for_model(i.course)
				o = TreeNode.objects.get(content_type__pk=object_type.pk, object_id=i.course_id)
				TreeNode.objects.create(content_object=i, parent=o)
			else:
				TreeNode.objects.create(content_object=i)

class SubjectGroup(models.Model):
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

# [34] Instructional year level (for subjects 1-15)
class InstructionalYearLevel(models.Model):
	ministry_code = models.CharField(max_length=4)
	description = models.CharField(max_length=32)

	def __unicode__(self):
		return self.description

	class Meta:
		verbose_name = _('Instructional Year Level')

class Assessment(models.Model):
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
	subject = models.ForeignKey(Subject, blank=True, null=True)
	instructional_year_level = models.ForeignKey(InstructionalYearLevel, blank=True, null=True)
	# Need a way to track the learning level of a course for primary school
	#level = models.Something()
	name = models.CharField(max_length=64)
	short_name = models.CharField(max_length=16)
	nodes = generic.GenericRelation(TreeNode)
	attachments = generic.GenericRelation(Attachment)
	assessments = generic.GenericRelation(Assessment)
	
	# change tracking
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

#	@models.permalink
#	def get_absolute_url(self):
#		return ('testnameview', (str(self.id)))
	@models.permalink
	def get_absolute_url(self):
		return ('kapua.courses.views.course_detail', [str(self.pk)])

	def __unicode__(self):
		return u"%s" % self.name

	class Meta:
		verbose_name = _('Course')

post_save.connect(create_tree_node, sender=Course)

# A course page is like a university "paper"; a small component grouped with other
# components to make up a course.
class Page(models.Model):
	course = models.ForeignKey(Course)
	name = models.CharField(max_length=64)
	content = models.TextField(_('Content'))
	nodes = generic.GenericRelation(TreeNode)
	assessments = generic.GenericRelation(Assessment)
	attachments = generic.GenericRelation(Attachment)

	# change tracking
	created = models.DateTimeField()
	last_modified = models.DateTimeField()
	
	def __unicode__(self):
		return self.name
	
	@models.permalink
	def get_absolute_url(self):
		return ('kapua.courses.views.page_detail', [str(self.id)])

post_save.connect(create_tree_node, sender=Page)

#	def save(self):
#		import bleach
#		self.content = bleach.clean(self.content, tags=settings.ALLOWED_TAGS, attributes=settings.ALLOWED_ATTRS)
#
#		return super(Fragment, self).save()
	
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
	assessment = models.ForeignKey(Assessment)
	student = models.ForeignKey(Student)
	score = models.DecimalField(max_digits=10, decimal_places=9, blank=True, null=True)

class Submission(models.Model):
	assessment = models.ForeignKey(Assessment)
	student = models.ForeignKey(Student)
	created = models.DateTimeField()

class Schedule(models.Model):
	name = models.CharField(max_length=32)
	course = models.ForeignKey(Course)
	
	# change tracking
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
	
	def __unicode__(self):
		return self.name

class Activity(models.Model):
	schedules = models.ManyToManyField(Schedule, related_name="activities")
	subject = models.CharField(max_length=64)
	track_attendance = models.BooleanField(default=True)
	assessments = generic.GenericRelation(Assessment)
	date_and_time = models.DateTimeField()

	# change tracking
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

	def __unicode__(self):
		return self.subject

	class Meta:
		verbose_name = _('Activity')
		verbose_name_plural = _('Activities')

class AttendanceCode(models.Model):
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
	activity = models.ForeignKey(Activity)
	student = models.ForeignKey(Student)
	code = models.ForeignKey(AttendanceCode)

class Enrolment(models.Model):
	student = models.ForeignKey(Student)
	schedule = models.ForeignKey(Schedule)
	start = models.DateField()
	end = models.DateField()
