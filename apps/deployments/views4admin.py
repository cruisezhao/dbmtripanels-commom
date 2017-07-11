from .models import SystemOptions
from . import tables
from . import forms
from .filters import SysOptionFilterForm
from common.utilities.views import ObjectListView

class SystemOptionListView(ObjectListView):
    queryset = SystemOptions.objects.all()
    filter = SysOptionFilterForm
    filter_form = forms.SysOptionFilterForm
    table = tables.SysOptionTable
    template_name = "deployments/sys_option_list.html"
