from __future__ import unicode_literals

from markdown import markdown

from django import template
from django.utils.safestring import mark_safe
from itertools import chain
from collections import namedtuple

register = template.Library()

Field = namedtuple('Field', 'name verbose_name')

#
# Filters
#

@register.filter()
def oneline(value):
    """
    Replace each line break with a single space
    """
    return value.replace('\n', ' ')


@register.filter()
def getlist(value, arg):
    """
    Return all values of a QueryDict key
    """
    return value.getlist(arg)


@register.filter
def getkey(value, key):
    """
    Return a dictionary item specified by key
    """
    return value[key]


@register.filter(is_safe=True)
def gfm(value):
    """
    Render text as GitHub-Flavored Markdown
    """
    html = markdown(value, extensions=['mdx_gfm'])
    return mark_safe(html)


@register.filter()
def contains(value, arg):
    """
    Test whether a value contains any of a given set of strings. `arg` should be a comma-separated list of strings.
    """
    return any(s in value for s in arg.split(','))


@register.filter()
def bettertitle(value):
    """
    Alternative to the builtin title(); uppercases words without replacing letters that are already uppercase.
    """
    return ' '.join([w[0].upper() + w[1:] for w in value.split()])


@register.filter()
def example_choices(value, arg=3):
    """
    Returns a number (default: 3) of example choices for a ChoiceFiled (useful for CSV import forms).
    """
    choices = []
    for id, label in value:
        if len(choices) == arg:
            choices.append('etc.')
            break
        if not id:
            continue
        choices.append(label)
    return ', '.join(choices) or 'None'


#
# Tags
#

@register.simple_tag()
def querystring(request, **kwargs):
    """
    Append or update the page number in a querystring.
    """
    querydict = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            querydict[k] = v
        elif k in querydict:
            querydict.pop(k)
    querystring = querydict.urlencode()
    if querystring:
        return '?' + querystring
    else:
        return ''


@register.inclusion_tag('utilities/templatetags/utilization_graph.html')
def utilization_graph(utilization, warning_threshold=75, danger_threshold=90):
    """
    Display a horizontal bar graph indicating a percentage of utilization.
    """
    return {
        'utilization': utilization,
        'warning_threshold': warning_threshold,
        'danger_threshold': danger_threshold,
    }
    

@register.assignment_tag
def concat_string(a, b, *args):
    res = str(a) + str(b)
    for i in args:
        res = res + str(i)
    return res

@register.filter
def get_field(instance, field_name):
    """
    Returns field object for a model instance
    """
    return instance._meta.get_field(field_name)

@register.filter
def get_related_absolute_url(instance, field_name):
    """
    Returns field object for a model instance
    """
    if hasattr(instance, field_name) and getattr(instance, field_name):
        
        return get_absolute_url(getattr(instance, field_name))
    else:
        return ""

@register.filter
def get_absolute_url(instance):
    """
    Returns field object for a model instance
    """
    if hasattr(instance, 'get_absolute_url') and getattr(instance, 'get_absolute_url'):
        
        return instance.get_absolute_url()
    else:
        return ""

    
@register.filter
def get_related_objs(instance, field_name):
    """
    Returns field object for a model instance
    """
    if hasattr(instance, field_name) and getattr(instance, field_name):
        
        return getattr(instance, field_name).all()
    else:
        return ""
    
@register.filter
def get_value(obj, field):
    try:
        return getattr(obj, 'get_%s_display' % field)()
    except:
        return getattr(obj, field)
        
@register.filter
def get_model_fields(obj, detail_exclude=None):
    model = obj.__class__
    excludes = ['pk']

    property_fields = []
    for name in dir(model):
        if name not in excludes and isinstance(
            getattr(model, name, None), property
        ):
            property_fields.append(Field(name=name, verbose_name=name))
    fields = chain(obj._meta.fields, property_fields)

    if detail_exclude:
        fields = [field for field in fields if field.name not in detail_exclude]
    return fields


@register.filter
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    fields = [field.name for field in instance._meta.fields]
    if field_name in fields:
        return instance._meta.get_field(field_name).verbose_name.title()
    else:
        return field_name.title()
    
@register.inclusion_tag('inc/object_field.html')
def render_object_field(obj, field_name):
    """
    render the object field to a row of a table
    """
    return {
        'object': obj,
        'field_name': field_name,
    }
    
@register.filter
def get_model_name(instance):
    return instance.__class__.__name__