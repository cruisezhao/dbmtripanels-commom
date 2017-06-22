from django import forms
from common.apps.products.models import Products, Plans, ProductApps
from common.apps.orders.models import Orders, ORDER_STATUS
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.db import transaction


SEARCH_DATE = (
    (None, 'ALL'),
    (1, 'in a Day'),
    (7, 'in a Week'),
    (30,'in a Month'),
)
SEARCH_STATUS = [
    (None, 'ALL'),
    
    ]
SEARCH_STATUS.extend(ORDER_STATUS)


                
class OrderSearchForm(forms.Form):
    uuid = forms.CharField(label=_("Order ID"), required=False)
    created_date = forms.ChoiceField(label=_("Order Date"), choices=SEARCH_DATE, required=False)
    status = forms.ChoiceField(label=_("Order Status"), choices=SEARCH_STATUS, required=False)

class OrderForm(forms.Form):
    uuid = forms.CharField(label=_("Order ID"))
    product_name = forms.CharField(label=_("Product Name"))
    user_name = forms.CharField(label=_("User Name"))
    status = forms.ChoiceField(label=_("Order Status"), choices=ORDER_STATUS)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    @transaction.atomic
    def save(self):
        order = Orders.objects.get(uuid = self.cleaned_data['uuid'])
        order.status = self.cleaned_data['status']
        order.comment = self.cleaned_data['comment']
        order.save()
        
#         planorder = PlanOrders.objects.get(package = order.package)
#         planorder.status = self.cleaned_data['status']
#         planorder.save()
    
    @classmethod
    def gen_data(cls, productorder_id):
        order = Orders.objects.get(uuid = productorder_id)
        return {'uuid':order.uuid, 
                'product_name':order.get_product_name(), 
                'user_name':order.get_user_email(), 
                'status': order.status,
                'comment': order.comment}




@transaction.atomic
def gen_orders(user, product, plan, notes):
    # pkg_status = 'Pending'
    # pkg_ins = Packages.objects.create(package_name=pkgname, user=user, status=pkg_status, runtime=plan.content, plan=plan)
    order_status = 'Pending'
    order_amount = plan.price
    Orders.objects.create(client=user, plan=plan, product=product, amount=order_amount, status=order_status, notes=notes)


class OrderCreateForm(forms.Form):
    product = forms.CharField(max_length=255)
    plan = forms.CharField(max_length=255)
    notes = forms.CharField(max_length=255, required=False)

    def save(self, user):
        product = self.cleaned_data['product']
        plan = self.cleaned_data['plan']
        notes = self.cleaned_data['notes']
        product_ins = get_object_or_404(Products, uuid=product)
        plan_ins = get_object_or_404(Plans, uuid=plan)

        gen_orders(user, product_ins, plan_ins, notes)
