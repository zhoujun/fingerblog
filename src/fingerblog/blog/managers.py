#!/usr/bin/env python
# *_* encoding=utf-8 *_*

from django.db import models

class EntryPublishManager(models.Manager):
    
    def get_posts(self):
        return super(EntryPublishManager, self).get_query_set().filter(published=True, entrytype='post')\
        .order_by('-sticky').order_by('-date')
        
    def get_pages(self):
        return self.get_query_set().filter(published=True, entrytype='page').order_by('menu_order')
    
    def get_post_by_date(self, year, month):
        return super(EntryPublishManager, self).get_query_set()\
        .filter(published=True,entrytype='post',date__year=int(year),date__month=int(month))
    
    def get_post_by_day(self, year, month, day):
        return super(EntryPublishManager, self).get_query_set()\
        .filter(published=True,entrytype='post',\
        date__year=int(year), date__month=int(month), date__day=int(day))












