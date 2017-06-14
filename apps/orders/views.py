from django.shortcuts import render

from common.apps.orders.form import OrderCreateForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, get_list_or_404
from common.apps.products.models import Products, Plans
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


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
    template_name = 'order_submit_success.html'


class OrderNotallowView(TemplateView):
    template_name = 'notallow.html'


class OrderCreateView(FormView):
    success_url = reverse_lazy('orders:success')
    template_name = '/order_form.html'
    form_class = OrderCreateForm

    @method_decorator(login_required(login_url='accounts:login'))
    def dispatch(self, request, *args, **kwargs):
        #if not allowed_order(request):
            #return HttpResponseRedirect("/orders/notallow/")
        return super(OrderCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        if 'pro' in self.kwargs and self.kwargs['pro']:
            prouuid = self.kwargs['pro']
            product = get_object_or_404(Products, uuid=prouuid)
        else:
            return HttpResponseRedirect("error.html")

        plan_list = get_list_or_404(Plans, product=product)
        context['product'] = product
        context['plan_list'] = plan_list
        return context

    def form_valid(self, form):
        form.save(self.request.user)
        return super(OrderCreateView, self).form_valid(form)

