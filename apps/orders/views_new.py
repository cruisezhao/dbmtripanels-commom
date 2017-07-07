'''
Created on Jun 30, 2017

@author: ben
'''
from common.utilities.views import ObjectListView
from .models import Orders
from . import filters
from . import tables
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class OrderListView(ObjectListView):
    
    queryset = Orders.objects.all()
    filter = filters.OrderFilter
    #filter_form = filter.form
    table = tables.OrderTable
    template_name = 'orders/order_list.html'