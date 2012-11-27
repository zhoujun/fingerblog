#!/usr/bin/env python
# *_* encoding=utf-8 *_*

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from fingerblog.blog.models import Entry, Category
from fingerblog.blog.utils import render


def demo(request):
    if request.method == 'POST':
        
        user = []
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username: user.append(username)
        if password: user.append(password)
        
        print "=============user:",user
        return HttpResponseRedirect('/');
    else:
        context = RequestContext(request,{})
        return render_to_response('demo.html',context)
        

def index(request):
    page = request.GET.get('page',1)
    posts = Entry.objects.get_posts()
    return render(request, 'index.html', {'entries':posts, 'page':page})

def single (request,id=None):
    try:
        entry = Entry.objects.get(id=id)
        entry.update_readtimes()
    except:
        return render_to_response('404.html')
    return render(request,"single.html",{'entry':entry})

def category(request,name):
    try:
        if name:
            cat = Category.objects.get(slug=name)
            page = request.GET.get('page',1)
            posts = Entry.objects.get_posts().filter(category=cat)
            return render(request,'category.html',{'entries':posts,'category':cat,'page':page})
    except:
        return HttpResponseRedirect('404.html')

def archives(request,year,month):
    page = request.GET.get('page',1)
    posts = Entry.objects.get_post_by_date(year,month)
    return render(request,'archives.html',{'entries':posts,'page':page,'year':year,'month':month})