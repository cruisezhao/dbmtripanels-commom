from django import forms
from common.apps.products.models import Products, Plans
from common.apps.orders.models import Orders
from common.apps.packages.models import Packages
from django.shortcuts import get_object_or_404
from django.db import transaction

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
