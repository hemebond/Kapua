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
from django.db import models
from django.contrib.auth.models import User
from kapua.people.models import Person

class School(models.Model):
	name = models.CharField(max_length=128)
	ministry_code = models.IntegerField(max_length=4, db_index=True)

	def __unicode__(self):
		return self.name

class StudentType(models.Model):
	ministry_code = models.CharField(max_length=8)
	description = models.CharField(max_length=256)

	def __unicode__(self):
		return self.description

class ZoningStatus(models.Model):
	ministry_code = models.CharField(max_length=4)
	description = models.CharField(max_length=256)

	def __unicode__(self):
		return self.description

class ExchangeScheme(models.Model):
	ministry_code = models.IntegerField(max_length=2)
	description = models.CharField(max_length=256)

	def __unicode__(self):
		return self.description

class EligibilityCriteria(models.Model):
	ministry_code = models.IntegerField(max_length=5, db_index=True)
	description = models.CharField(max_length=256)

	def __unicode__(self):
		return self.description

class ORS(models.Model):
	ministry_code = models.CharField(max_length=1, db_index=True)
	description = models.CharField(max_length=128)

	def __unicode__(self):
		return self.description

class Student(models.Model):
	person = models.OneToOneField(Person)
	ministry_id = models.IntegerField(unique=True, max_length=10) # [3] National Student Number
	ors = models.ForeignKey(ORS, verbose_name="ORS and Section 9", default="1") # [16] ORS and Section 9
	funding_year_level = models.IntegerField(max_length=2) # [17] Funding Year Level
	student_type = models.ForeignKey(StudentType, default="1") # [18] Type of Student
	zoning_status = models.ForeignKey(ZoningStatus, default="3") # [20] Zoning Status
	tuition_fee = models.IntegerField(max_length=8, blank=True, null=True) # [22] Tuition Fee Paid by International Students
	exchange_scheme = models.ForeignKey(ExchangeScheme, blank=True, null=True) # [94] Exchange Scheme or Agreement
	boarding_status = models.BooleanField(verbose_name='Student is a school boarder', default=False) # [95] Students Boarding Status
	eligibility_criteria = models.ForeignKey(EligibilityCriteria, null=True, default="23") # [100] Elegibility Criteria
	year_level = models.IntegerField(verbose_name=_('Year Level'), max_length=2) # [103] Current Year Level

	def __unicode__(self):
		return "%s" % self.person

class LeaveReason(models.Model):
	ministry_code = models.CharField(max_length=1)
	description = models.CharField(max_length=256)

class Enrolment(models.Model):
	school = models.ForeignKey(School)
	start = models.DateField()
	end = models.DateField(blank=True, null=True)
