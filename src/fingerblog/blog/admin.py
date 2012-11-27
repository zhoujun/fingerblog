#!/usr/bin/env python
# *_* encoding=utf-8 *_*

from django.contrib import admin
from fingerblog.blog.models import Archive, Category, Entry, OptionSet, Link, \
    Blog
from fingerblog.tagging.models import Tag, TaggedItem


class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('monthyear','year','month','entrycount','date')
   
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug','description')
    search_fields = ['name']

admin.site.register(Tag)
admin.site.register(TaggedItem)
admin.site.register(Blog)
admin.site.register(Archive,ArchiveAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Entry)
admin.site.register(OptionSet)
admin.site.register(Link)    