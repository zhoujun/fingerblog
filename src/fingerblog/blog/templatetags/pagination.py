#!/usr/bin/env python
# *_* encoding=utf-8 *_*

from django import template
from django.core.paginator import Paginator, EmptyPage

register = template.Library()

def get_page_range(current, range):
    if range[-1] < 8:
        return xrange(1, range[-1] + 1)
    
    if range[-1] - current < 4:
        first = range[-1] - 7
    elif current > 4:
        first = current - 3
    else:
        first = 1
    
    if first + 7 < range[-1]:
        last = first + 8
    else:
        last = range[-1] + 1
        
    return xrange(first, last)
        
class PaginationNode(template.Node):
    def __init__(self, objects, page, page_size=8):
        self.object_var_name = objects
        self.page_size = int(page_size)
        self.objects_to_be_paginated = template.Variable(objects)
        self.current_page = template.Variable(page)
    
    def render(self, context):
        objects = self.objects_to_be_paginated.resolve(context)
        current = int(self.current_page.resolve(context))
        paginator = Paginator(objects, self.page_size)
        try:
            page = paginator.page(current)
        except EmptyPage:
            context[self.object_var_name] = None
            context['paginator_page'] = None
            context['paginator_current'] = current
            context['paginator_range'] = None
        else:
            context[self.object_var_name] = page.object_list
            context['paginator_page'] = page
            context['paginator_current'] = current
            context['paginator_range'] = get_page_range(current, paginator.page_range)
        return ''

@register.tag
def begin_pagination(parser, token):
    try:
        tag_name, objects, page, page_size = token.split_contents()
        return PaginationNode(objects, page, page_size)
    except:
        tag_name, objects, page = token.split_contents()
    
    return PaginationNode(objects, page)
        
@register.inclusion_tag('pagination.html', takes_context=True)
def end_pagination(context):
    if 'paginator_path' in context:
        paginator_path = context['paginator_path']
    else:
        paginator_path = ''
    
    return{
        'paginator_page':context['paginator_page'],
        'paginator_current':context['paginator_current'],
        'paginator_range':context['paginator_range'],
        'paginator_path':paginator_path
    }        
        
        
        