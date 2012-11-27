#!/usr/bin/env python
# *_* encoding=utf-8 *_*
from django.contrib.sites.models import Site
from fingerblog.blog.models import Blog

def side(request):
    blog = Blog.get()
    site = Site.objects.get_current()
    return locals()
