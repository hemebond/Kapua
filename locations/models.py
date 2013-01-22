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
from mptt.models import MPTTModel, TreeForeignKey


class LocationType(models.Model):
	name = models.CharField(max_length=255)
	level = models.IntegerField()

	def __unicode__(self):
		return self.name


class Location(MPTTModel):
	name = models.CharField(max_length=255)
	type = models.ForeignKey(LocationType, null=True)

	# Use by MPTT
	parent = TreeForeignKey(
		'self',
		null=True,
		blank=True,
		related_name='children'
	)

	def __unicode__(self):
		return u"%s" % self.name

	# def save(self, *args, **kwargs):
	# 	return super(Location, self).save(*args, **kwargs)


class Country(Location):
	code_alpha2 = models.CharField(max_length=2)
	code_alpha3 = models.CharField(max_length=3)
	code_numeric = models.IntegerField()

	class Meta:
		verbose_name_plural = _("countries")

	def save(self, *args, **kwargs):
		self.type = LocationType.objects.get(name="Country")
		return super(Country, self).save(*args, **kwargs)
