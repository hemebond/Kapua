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

class Citizenship(models.Model):
	ministry_code = models.CharField(max_length=3)
	iso_code = models.CharField(max_length=2)
	description = models.CharField(max_length=256)

	def __unicode__(self):
		return self.description

class Ethnicity(models.Model):
	ministry_code = models.IntegerField(default=999)
	description = models.CharField(max_length=64)
	
	def __unicode__(self):
		return self.description

class Iwi(models.Model):
	ministry_code = models.CharField(max_length=4)
	description = models.CharField(max_length=64)

	def __unicode__(self):
		return self.description

class Residence(models.Model):
	unit = models.CharField(max_length=3, blank=True, null=True) # [96] ADDRESS1
	number = models.IntegerField(verbose_name='House number') # [96] ADDRESS1
	street = models.CharField(max_length=32, verbose_name='Street name') # [96] ADDRESS1
	suburb = models.CharField(max_length=32, verbose_name='Suburb or Rural Delivery (RD) number', blank=True, null=True) # [97] ADDRESS2
	town = models.CharField(max_length=32, verbose_name='Town or City') # [98] ADDRESS3
	postcode = models.IntegerField(max_length=4, blank=True, null=True) # [99] ADDRESS4
	
	def __unicode__(self):
		rs = ""
		if self.unit:
			rs = str(self.unit) + "/"
			
		return rs + str(self.number) + " " + self.street + ", " + self.suburb + ", " + self.town

class Person(models.Model):
	GENDER_CHOICES = (
		(1, _('male')),
		(2, _('female')),
	)
	
	last_name = models.CharField(max_length=32, verbose_name=_('last_name')) # [4] Surname
	first_name = models.CharField(max_length=32, verbose_name=_('first_name')) # [5] First Name
	gender = models.IntegerField(max_length=1, choices=GENDER_CHOICES, default=2, verbose_name=_('gender')) # [6] Gender
	birthdate = models.DateField(help_text='Use the format YYYY-MM-DD', verbose_name=_('date_of_birth')) # [7] Date of birth
	ethnicity = models.ManyToManyField(Ethnicity) # [10,11,12] Ethnicity (Ethnic 1, 2 and 3)
	iwi = models.ManyToManyField(Iwi, blank=True, null=True) # [13,14,15] Iwi affiliation (Iwi 1, 2 & 3)
	citizenship = models.ForeignKey(Citizenship) # [21] Country of Citizenship
	privacy_indicator = models.BooleanField(verbose_name="Hide address information") # [105] Privacy Indicator
	middle_names = models.CharField(max_length=32, blank=True, null=True) # [106] MiddleName(S)
	preferred_first_name = models.CharField(max_length=32, blank=True, null=True) # [107] Preferred First Name
	preferred_last_name = models.CharField(max_length=32, blank=True, null=True) # [108] Preferred Surname
	
	relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')
	residence = models.ForeignKey(Residence)
	
	user = models.ForeignKey(User, blank=True, null=True)

	def name(self):
		return self.first_name + " " + self.last_name

	def __unicode__(self):
		return self.name()
	
	class Meta:
		verbose_name = _('person')
		verbose_name_plural = _('people')

class RelationshipType(models.Model):
	description = models.CharField(max_length=32)
	
	def __unicode__(self):
		return self.description

class Relationship(models.Model):
	from_person = models.ForeignKey(Person, related_name='from_people')
	to_person = models.ForeignKey(Person, related_name='to_people')
	relationship = models.ForeignKey(RelationshipType)
	
	def __unicode__(self):
		return str(self.from_person) + " is " + str(self.relationship) + " to " + str(self.to_person)
