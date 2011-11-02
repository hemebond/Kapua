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

class Country(models.Model):
	"""Model for countries"""
	iso_code = models.CharField(max_length=2, primary_key=True)
	ministry_code = models.CharField(max_length=3, blank=True, null=True)
	name = models.CharField(max_length=45)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('Country')
		verbose_name_plural = _('Countries')
		ordering = ["name", "iso_code"]

class Ethnicity(models.Model):
	ministry_code = models.IntegerField(default=999, primary_key=True)
	description = models.CharField(max_length=64)

	def __unicode__(self):
		return self.description

	class Meta:
		ordering = ['description']

class Iwi(models.Model):
	ministry_code = models.CharField(max_length=4, primary_key=True)
	description = models.CharField(max_length=64)

	def __unicode__(self):
		return self.description

	class Meta:
		verbose_name_plural = "Iwi"
		ordering = ['description']

class Residence(models.Model):
	"""Model to store residence information"""
	number = models.CharField(max_length=32, verbose_name=_('Unit and house number')) # [96] ADDRESS1
	street = models.CharField(max_length=32, verbose_name=_('Street name')) # [96] ADDRESS1
	suburb = models.CharField(max_length=32, verbose_name=_('Suburb or Rural Delivery number')) # [97] ADDRESS2
	city = models.CharField(max_length=32, verbose_name=_('Town or city')) # [98] ADDRESS3
	country = models.ForeignKey(Country, default='NZ')
	postcode = models.IntegerField(max_length=4, blank=True, null=True) # [99] ADDRESS4
	phone = models.CharField(max_length=32, blank=True, null=True)

	def __unicode__(self):
		return "%s, %s, %s, %s" % (self.city, self.suburb, self.street, str(self.number))

#	@models.permalink
#	def get_absolute_url(self):
#		return ('kapua.people.views.residence_detail', [str(self.id)])

	class Meta:
		verbose_name_plural = _('Residences')
		unique_together = ('number', 'street', 'suburb', 'city', 'country')
		ordering = ['country', 'city', 'suburb', 'street', 'number']

#class PersonManager(models.Manager):
#	def get_query_set(self):
#		return super(PersonManager, self).get_query_set().extra(select={'first_name': "CASE WHEN LENGTH(preferred_first_name) > 0 THEN preferred_first_name ELSE legal_first_name END", 'last_name': "CASE WHEN LENGTH(preferred_last_name) > 0 THEN preferred_last_name ELSE legal_last_name END"})

class Person(models.Model):
	GENDER_CHOICES = (
		(1, _('male')),
		(2, _('female')),
	)

	legal_last_name = models.CharField(max_length=32, verbose_name=_('last_name')) # [4] Surname
	legal_first_name = models.CharField(max_length=32, verbose_name=_('first_name')) # [5] First Name
	gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, default=1) # [6] Gender
	birth_date = models.DateField(_('Date of Birth'), help_text="Use the format YYYY-MM-DD", blank=True, null=True) # [7] Date of birth
	ethnicity = models.ManyToManyField(Ethnicity, blank=True, null=True) # [10,11,12] Ethnicity (Ethnic 1, 2 and 3)
	iwi = models.ManyToManyField(Iwi, blank=True, null=True) # [13,14,15] Iwi affiliation (Iwi 1, 2 & 3)
	citizenship = models.ForeignKey(Country, blank=True, null=True) # [21] Country of Citizenship
	privacy_indicator = models.BooleanField(_('Hide address information')) # [105] Privacy Indicator
	middle_names = models.CharField(max_length=32, blank=True, null=True) # [106] MiddleName(S)
	preferred_first_name = models.CharField(max_length=32, blank=True, null=True) # [107] Preferred First Name
	preferred_last_name = models.CharField(max_length=32, blank=True, null=True) # [108] Preferred Surname

	residence = models.ForeignKey(Residence, blank=True, null=True)
	phone = models.CharField(max_length=32, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)

	photo = models.ImageField(upload_to="people", blank=True, null=True)

	user = models.OneToOneField(User, verbose_name='SIS Account', blank=True, null=True)

	#objects = PersonManager()

	first_name = models.CharField(max_length=32, blank=True, null=True)
#	@property
#	def first_name(self):
#		return "%s" % (self.preferred_first_name or self.legal_first_name)

	last_name = models.CharField(max_length=32, blank=True, null=True)
#	@property
#	def last_name(self):
#		return "%s" % (self.preferred_last_name or self.legal_last_name)

	def __unicode__(self):
		return "%s, %s %s" % (self.last_name, self.first_name, self.middle_names)

	@property
	def age(self):
		TODAY = datetime.date.today()
		return u'%s' % dateutil.relativedelta(TODAY, self.birth_date).years

	@models.permalink
	def get_absolute_url(self):
		return ('kapua.people.views.detail', [str(self.id)])

	class Meta:
		verbose_name = _('Person')
		verbose_name_plural = _('People')

	def save(self, *args, **kwargs):
		self.first_name = (self.preferred_first_name or self.legal_first_name)
		self.last_name = (self.preferred_last_name or self.legal_last_name)
		super(Person, self).save(*args, **kwargs)

class RelationshipType(models.Model):
	description = models.CharField(max_length=32)
	reciprocal = models.ForeignKey('self')

	def __unicode__(self):
		return "%s" % (self.description)

class Relationship(models.Model):
	person = models.ForeignKey(Person, related_name='related_people', verbose_name=_('Person'))
	related_person = models.ForeignKey(Person, related_name='+', verbose_name=_('Person'))
	relationship_type = models.ForeignKey(RelationshipType, verbose_name="Type of relationship")
	reciprocal = models.ForeignKey('self', related_name="+", null=True, blank=True)

	class Meta:
		unique_together = (('person', 'related_person', 'relationship_type'),)

	def __unicode__(self):
		return '%s is %s to %s' % (str(self.related_person), str(self.relationship_type), str(self.person))

	def save(self, is_reciprocal=False, *args, **kwargs):
		if not is_reciprocal:
			if not self.reciprocal == None:
				self.reciprocal.relationship_type = self.relationship_type.reciprocal
				self.reciprocal.save(is_reciprocal=True)
			else:
				super(Relationship, self).save(*args, **kwargs)
				r = Relationship(person=self.related_person, related_person=self.person, relationship_type=self.relationship_type.reciprocal, reciprocal=self)
				r.save(is_reciprocal=True)
				self.reciprocal = r
		super(Relationship, self).save(*args, **kwargs)
