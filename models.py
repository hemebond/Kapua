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
# Generic relationship
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
# MPTT
from mptt.models import MPTTModel, TreeForeignKey

class TreeNode(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    # Generic relationship to link to courses, topics or activities
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return u"%s %s %s" % (self.lft, self.content_object, self.rght)
    
    def previous(self):
        try:
            node = TreeNode.objects.filter(rght__lt=self.lft, tree_id=self.tree_id).order_by("-lft")[0:1].get()
        except:
            if self.parent:
                node = self.parent
            else:
                node = None
        return node
    
    def next(self):
        try:
            node = TreeNode.objects.filter(lft__gt=self.lft, tree_id=self.tree_id).order_by("lft")[0:1].get()
        except:
            node = None
        return node
