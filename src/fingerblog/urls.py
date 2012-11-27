#!/usr/bin/env python
# *_* encoding=utf-8 *_*

from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from fingerblog import settings
from fingerblog.blog import views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^themes/(?P<path>.*)$','fingerblog.blog.ext_views.theme'),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    (r'^$', views.index),
    (r'^archive/(?P<id>\d+).html$',views.single),
    (r'^category/(?P<name>[-\w]+)$',views.category), 
    (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})$',views.archives),
    (r'^demo/$',views.demo),
    (r'^admin/', include(admin.site.urls)),
)
