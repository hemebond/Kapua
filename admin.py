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
from mptt.admin import MPTTModelAdmin
from kapua.models import TreeNode
from django import forms

class TreeNodeAdmin(MPTTModelAdmin):
    def get_urls(self):
        urls = super(TreeNodeAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(?P<node_id>\d+)/move/$', self.admin_site.admin_view(self.move))
        )
        return my_urls + urls

    def move(self, request, node_id):
        print "Running move on node %s" % node_id
        # custom view which should return an HttpResponse
        if request.method == 'POST':
            target_id = request.POST.get('target_id')
            position = request.POST.get('position')
            print "moving to %s" % position
            node = TreeNode.objects.get(id=node_id)
            target = TreeNode.objects.get(id=target_id)
            node.move_to(target, position)
            return HttpResponse(status=200)
        else:
            raise Http404
        
admin.site.register(TreeNode, TreeNodeAdmin)