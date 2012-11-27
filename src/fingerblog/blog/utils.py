#!/usr/bin/env python
# *_* encoding=utf-8 *_*

from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template
from fingerblog.blog.models import Blog
import urllib

def render_response(request, *args, **kwds):
    kwds['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwds)
    
def render(request,theme_file,template_ctx):
    blog=Blog.get()
    theme = blog.theme_name
    tpl_file='themes/'+theme+'/'+theme_file
    return render_response(request,tpl_file,template_ctx)

def load_tempalte(theme_file):
    blog=Blog.get()
    theme = blog.theme_name
    tpl_file='themes/'+theme+'/'+theme_file
    return get_template(tpl_file)
    
def urldecode(value):
    return  urllib.unquote(urllib.unquote(value)).decode('utf8')

def urlencode(value):
    return urllib.quote(value.encode('utf8'))

def paginator(object_list,per_page,pagenum):
    paginator = Paginator(object_list, per_page)
    return paginator.page(pagenum)





