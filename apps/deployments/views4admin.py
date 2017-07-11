from django.views.generic import View
from django.shortcuts import get_object_or_404,render
from .models import SystemOptions
from . import tables
from . import forms
from .filters import SysOptionFilterForm
from common.utilities.views import (ObjectListView,ObjectEditView,
                                    ObjectDeleteView)

class SystemOptionListView(ObjectListView):
    queryset = SystemOptions.objects.all()
    filter = SysOptionFilterForm
    filter_form = forms.SysOptionFilterForm
    table = tables.SysOptionTable
    template_name = "deployments/sys_option_list.html"


class SystemOptionView(View):
    def get(self, request, uuid):
        sys_option = get_object_or_404(SystemOptions,uuid = uuid)
        return render(request, "deployments/sys_option.html",
                      {'object':sys_option})

class SystemOptionEditView(ObjectEditView):
    """product edit"""
    model = SystemOptions
    form_class = forms.SystemOptionForm
    template_name = 'deployments/sys_option_edit.html'
    default_return_url = 'deployments:sys_option_list'


class SystemOptionDeleteView(ObjectDeleteView):
    model = SystemOptions
    default_return_url = "deployments:sys_option_list"
