from django.shortcuts import render, render_to_response

from .form import OrderCreateForm, OrderSearchForm, OrderForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, get_list_or_404
from common.apps.products.models import Products, Plans, ProductApps
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import datetime
from .models import Orders
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from common.apps.packages.models import Packages


ORDERS_PER_PAGE = 10

@login_required
def list_orders(request, template_name='orders/orderlist_staff.html'):

    if request.method == 'POST':
        form = OrderSearchForm(request.POST)
        
    else:
        data = {
                'uuid':request.GET.get('uuid',''),
                'created_date':request.GET.get('created_date', ''),
                'status':request.GET.get('status','')
            }
        form = OrderSearchForm(data)
    kwargs = {}
    if form.is_valid():
                
        if form.cleaned_data['uuid']:
            kwargs['uuid__contains'] = form.cleaned_data['uuid']
        if form.cleaned_data['created_date']:
            kwargs['created_date__lte'] = datetime.datetime.now()
            kwargs['created_date__gte'] = datetime.datetime.now() - datetime.timedelta(days=int(form.cleaned_data['created_date']))
        if form.cleaned_data['status']:
            kwargs['status'] = form.cleaned_data['status']
        
    order_list = Orders.objects.filter(**kwargs).order_by('-created_date')
     
    #pkg_list = Packages.objects.filter()    
    paginator = Paginator(order_list, ORDERS_PER_PAGE) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)

    return render(request, template_name, {'order_list': orders, 'form':form})


@login_required
def detail_orders(request, id, template_name='orders/orderdetail_admin.html'):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            messages.success(request, _("save successfully"))
            # redirect to a new URL:
            #return HttpResponseRedirect(reverse('accounts:profile_social'))
    # if a GET (or any other method) we'll create a new form by user model from DB           
    else:
        data = OrderForm.gen_data(id)
        form = OrderForm(data)
        
    return render(request, template_name, {'form':form})


@login_required
def list_user_order(request, template_name='orders/orderlist_client.html'):
    orders = Orders.objects.filter(client__pk=request.user.pk)
    return render(request, template_name, {'orders': orders})

# def allowed_order(request):
#     user = request.user
#     pkg = Packages.objects.filter(user=user)
#     if pkg:
#         count = 0
#         for p in pkg:
#             if p.status in ('Pending', 'Active', 'Suspended', 'Invalid'):
#                 count += 1
#         if count:
#             return False
#     return True


class OrderSuccess(TemplateView):
    template_name = 'orders/order_submit_success.html'


class OrderNotallowView(TemplateView):
    template_name = 'orders/notallow.html'


class OrderCreateView(FormView):
    success_url = reverse_lazy('orders:success')
    template_name = 'orders/order_form.html'
    form_class = OrderCreateForm

    @method_decorator(login_required(login_url='clients:login'))
    def dispatch(self, request, *args, **kwargs):
        #if not allowed_order(request):
            #return HttpResponseRedirect("/orders/notallow/")
        return super(OrderCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        if 'pro' in self.kwargs and self.kwargs['pro']:
            prouuid = self.kwargs['pro']
            product = get_object_or_404(Products, uuid=prouuid)
            product_app = get_object_or_404(ProductApps, product=product)
        else:
            return render_to_response('orders/error.html', {'message':'Can not get product information.'})

        plan_list = product.plans.all()
        context['product_uuid']=prouuid
        context['product_app'] = product_app
        context['plan_list'] = plan_list
        return context

    def form_valid(self, form):
        form.save(self.request.user)
        return super(OrderCreateView, self).form_valid(form)

