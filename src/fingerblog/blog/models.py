#!/usr/bin/env python
# *_* encoding=utf-8 *_*

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from datetime import datetime

from fingerblog.blog.managers import EntryPublishManager
from fingerblog.tagging.fields import TagField
from fingerblog.tagging.models import Tag, TaggedItem


class Archive(models.Model):
    monthyear = models.CharField(max_length=20)
    year = models.CharField(max_length=8)
    month = models.CharField(max_length=4)
    entrycount = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    
    class META:
        ordering=('date',)
        
    def __unicode__(self):
        return self.monthyear
    
    def get_absolute_url(self):
        return '/archives/%s/%s' % (self.year, self.month)
    

class Blog(models.Model):
    title = models.CharField(max_length=100,default="FingerBlog")
    subtitle = models.CharField(max_length=100,default="this a simple single blog")
    theme_name = models.CharField(max_length=30,default='default')
    author = models.CharField(max_length=20,default='admin')
    email = models.EmailField(default='finger.zhou@gmail.com')
    notice = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    site_keywords = models.CharField(max_length=100,null=True, blank=True)
    site_description = models.CharField(max_length=200,null=True, blank=True)
    
    @staticmethod
    def get():
        blog = None
        try:
            blog = Blog.objects.all()[0]
        except:
            pass
        if not blog:
            blog = Blog()
            blog.save()
        return blog
    
    def __unicode__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    
    @property
    def count(self):
        return Entry.objects.get_posts().filter(category=self).count()
       
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
    
    
class Entry(models.Model):
    ENTRY_TYPE_CHOICES = (('page','page'),('post','post'))
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User)
    excerpt = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)
    entrytype = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES,default='post')
    tags = TagField()
    category = models.ForeignKey(Category)
    
    readtimes = models.IntegerField(default=0)
    slug = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    monthyear = models.CharField(max_length=20, null=True, blank=True)
    
    allow_comment = models.BooleanField()
    allow_pingback = models.BooleanField()
    menu_order = models.IntegerField(default=0)
    
    sticky = models.BooleanField(default=False)
    date = models.DateTimeField()
    objects = EntryPublishManager()
    
    class Meta:
        ordering = ['-id']
        
    def get_absolute_url(self):
        if self.link:
            return self.link
        else:
            return '/archive/%s.html' % (str(self.id))
    
    def __unicode__(self):
        return self.title
    
    @property
    def excerpt_content(self):
        if(len(self.excerpt) <= 0):
            return self.content[:200]+'...'
        else:
            return self.excerpt
        
    def prev(self):
        prev = Entry.objects.filter(published=True, entrytype='post', date__lt=self.date).order_by('-date')
        if len(prev) > 0:
            return prev[0]
        else:
            return None
    
    def next(self):
        next = Entry.objects.filter(published=True, entrytype='post', date__gt=self.date).order_by('date')
        if len(next) > 0:
            return next[0]
        else:
            return None
        
    def get_tags(self):
        return Tag.objects.get_for_object(self)
    
    def get_full_url(self):
        return "http://%s/%s" %(Site.objects.get_current().domain,self.link)
    
    def update_readtimes(self):
        self.readtimes += 1
        super(Entry,self).save()
    
    def relate_posts(self):
        posts = []
        for tag in self.get_tags():
            entrys = TaggedItem.objects.get_by_model(self, tag).order_by('-date')
            posts.extend(entrys)
            
        if self in posts:
            posts.remove(self)
        
        posts = set(posts)
        return list(posts)[:5]
    
    def __update_link(self):
        vals = {'year':self.date.year, 'month':str(self.date.month).zfill(2), 'day':self.date.day,\
                'postname':'self.slug', 'id':self.id}
        permalink_format = OptionSet.get('permalink_format', 'archive/%(id)s.html')
        
        if self.entrytype == 'post':
            if not self.slug:
                vals.update({'postname':self.id})
            if permalink_format == 'custom':
                permalink_structure = OptionSet.get('permalink_structure','%(year)s/%(month)s/%(day)s/%(postname)s')
                self.link = permalink_structure.strip()% vals
            else:
                self.link = permalink_format.strip() % vals
        
        else:
            if self.slug:
                self.link = self.slug
            else:
                self.link = str(self.id)
                
    def save(self, pub=False):
        if not self.date:
            self.date = datetime.now()
        else:
            self.date = datetime.strptime(str(self.date)[0:19],"%Y-%m-%d %H:%M:%S")
#        old_pub = self.published
        if pub:
            super(Entry,self).save()
            self.__update_link()
        
#        self.published = pub
        super(Entry,self).save()
        self.update_archive(1)
#        
#        if old_pub and not pub:
#            self.update_archive(-1)
#        
#        if not old_pub and pub:
#            self.update_archive(1)
        
    def delete(self):
        if self.published:
            self.update_archive(-1)
        super(Entry, self).delete()
        
    def update_archive(self, cnt=1):
        my = self.date.strftime('%B %Y')
        sy = self.date.strftime('%Y')
        sm = self.date.strftime('%m')
        
        if self.entrytype == 'post':
            try:
                archive = Archive.objects.get(monthyear=my)
                if not archive:
                    archive = Archive(monthyear=my, year=sy, month=sm, entrycount=1)
                    self.monthyear = my
                    archive.save()
                else:
                    archive.entrycount += cnt
                    if archive.entrycount <= 0:
                        archive.entrycount = 0
                    archive.save()
            except:
                archive = Archive(monthyear=my, year=sy, month=sm, entrycount=1)
                archive.save()

class Link(models.Model):
    text = models.CharField(max_length=20)
    href = models.URLField()
    create_date = models.DateTimeField(auto_now_add=True)      
    
    def __unicode__(self):
        return self.text
    

class OptionSet(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()
    
    @classmethod
    def set(cls, k, v):
        os, created = OptionSet.objects.get_or_create(key=k)
        os.value = v
        os.save()
        return os
    
    @classmethod
    def get(cls, k, v=''):
        try:
            option = OptionSet.objects.get(key=k)
        except:
            option = OptionSet.set(k, v)
        return option.value

    @classmethod
    def delete(cls, k):
        return OptionSet.object.get(key=k).delete()
    
    
    
    
    
     
    
    

