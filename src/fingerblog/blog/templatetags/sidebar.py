#!/usr/bin/env python
# *_* encoding=utf-8 *_*
from django.template import Library
from fingerblog.blog.models import Entry, Category, Link, Archive
from fingerblog.settings import DATABASE_ENGINE

register = Library()

@register.inclusion_tag('sidebar/recent_posts.html', takes_context=True)
def get_recent_posts(context):
    posts = Entry.objects.get_posts()[:8]
    return {'recent_posts': posts}

@register.inclusion_tag('sidebar/hot_posts.html', takes_context=True)
def get_hot_posts(context):
    posts=Entry.objects.get_posts().order_by('-readtimes')[:8]
    return {'hot_posts': posts}

@register.inclusion_tag('sidebar/random_posts.html', takes_context=True)
def get_random_posts(context):
    if DATABASE_ENGINE == 'mysql':
        entrys = Entry.objects.raw("select * from blog_entry where published=1 and entrytype='post' order by rand() limit 8")
    else:
        entrys = Entry.objects.raw("select * from blog_entry where published=1 and entrytype='post' order by random() limit 8")
    return {'random_posts':entrys}

@register.inclusion_tag('sidebar/categories.html', takes_context=True)
def get_categories(context):
    categories = Category.objects.all()
    return {'categories':categories}

@register.inclusion_tag('sidebar/links.html', takes_context=True)
def get_links(context):
    links = Link.objects.all()
    return {'links':links}    

@register.inclusion_tag('sidebar/archives.html', takes_context=True)    
def get_archives(context):
    archives = Archive.objects.all().order_by('-date')[:10]    
    return {'archives':archives}
    
@register.inclusion_tag('menus.html', takes_context = True)
def get_menus(context):
    pages = Entry.objects.get_pages()
    current = 'current' in context and context['current']
    return {'menus':pages,'current': current}    
    