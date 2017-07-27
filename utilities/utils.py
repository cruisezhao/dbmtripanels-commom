import uuid
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.utils.functional import keep_lazy


def uuid_to_str():
    """convert uuid to str"""
    return uuid.uuid4().hex

@keep_lazy(list)
def gen_choices(cls, field_name, choices):
    """generate choice count for each choice value"""
    pt_d = {}
    ps = cls.objects.values(field_name).annotate(count=Count(field_name))
    for p in ps:
        value = pt_d.setdefault(p[field_name],0)
        pt_d[p[field_name]] = value + p['count']
    return [(t[0], mark_safe("{} <span class='badge pull-right'>{}</span>".format(t[1],pt_d.get(t[0],0)))) for t in choices ]
