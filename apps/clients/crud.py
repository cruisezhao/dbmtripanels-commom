"""the package used for crud"""

import operator
from crudbuilder.abstract import BaseCrudBuilder
from django.contrib.auth import get_user_model
User = get_user_model()

from functools import reduce
from django.db.models import Q

from crudbuilder.formset import BaseInlineFormset
#from common.apps.packages.models import OpenstackUser
from common.apps.clients.forms import UserForm

# class OpenstackUserInlineFormset(BaseInlineFormset):
#     inline_model = OpenstackUser
#     parent_model = User
#     exclude = ['password']

class UserCrud(BaseCrudBuilder):
    """user crud"""
    model = User
    custom_modelform = UserForm
    search_fields = ['first_name','last_name','email','is_active','date_joined','phone_number','last_login_ip',]
    tables2_fields = ('first_name','last_name','email','is_active','date_joined','phone_number','last_login_ip')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 5
    login_required=False
    permission_required=False
    #inlineformset = OpenstackUserInlineFormset
    detailview_excludes = ['password','picture']
    ordering = '-date_joined'

    custom_templates = {
        'list': 'crud/userlist.html',
        'create': 'yourtemplates/your_create_template.html',
        'detail': 'crud/userdetail.html',
        'update': 'crud/userupdate.html',
        'delete': 'yourtemplates/your_delete_template.html'
        }

    @classmethod
    def custom_queryset(cls, request, **kwargs):
        """custom queryset"""
        d = request.GET
        # d.pop('page',None)
        qset = search_user(d)
        return qset

    @classmethod
    def custom_context(cls, request, context, **kwargs):
        """add context of search"""
        context['search_fields'] = ['first_name','last_name','email','is_active','date_joined',
                                    'phone_number','last_login_ip',]
        return context


def search_user(d):
    """search user"""
    objects = User.objects.all()
    if ''.join([d[k] for k in d if k !='page' and k != 'sort']):
        q_list = [Q(
                    ("{}__icontains".format(k),d[k]))
                    for k in d if k!='page' and d[k]!='' and k != 'sort']
        objects = objects.filter(reduce(operator.or_, q_list))
    return objects.order_by('-date_joined')
