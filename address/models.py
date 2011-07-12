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

class Address(models.Model):
	"""Model to store addresses for residences and businesses"""
	number = models.CharField(max_length=32, verbose_name=_('Unit and house number')) # [96] ADDRESS1
	street = models.CharField(max_length=32, verbose_name=_('Street name')) # [96] ADDRESS1
	suburb = models.CharField(max_length=32, verbose_name=_('Suburb or Rural Delivery number')) # [97] ADDRESS2
	city = models.CharField(max_length=32, verbose_name=_('Town or city')) # [98] ADDRESS3
	country = models.ForeignKey(Country, default='NZ')
	postcode = models.IntegerField(max_length=4, blank=True, null=True) # [99] ADDRESS4

	def __unicode__(self):			
		return "%s, %s, %s, %s" % (self.city, self.suburb, self.street, str(self.number))

	@models.permalink
	def get_absolute_url(self):
		return ('kapua.address.views.detail', [str(self.id)])

	class Meta:
		verbose_name_plural = _('Addresses')
		unique_together = ('number', 'street', 'suburb', 'city', 'country')
		ordering = ['country', 'city', 'suburb', 'street', 'number']
