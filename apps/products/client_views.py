"""views for client project"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product
from common.apps.orders.models import Packages
from django.core.paginator  import Paginator


@login_required
def get_user_product(request):
    """get client product"""
    if request.method == 'GET':
        u = request.user
        qset_package = Packages.objects.filter(user = u)
        #search filter
        search = request.GET.get('search',None)
        p_order_list = []
        for package in qset_package:
            p_order_list.extend(package.productorders_set.all())
        return render(request,  'applications/product_list.html', {
            'product_order_list':p_order_list,
        })