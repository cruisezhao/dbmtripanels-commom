"""the file include views for sfaff project"""

from django.shortcuts import render
from .forms import SoftwareForm, SoftwareShowForm
from .models import Software
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import DetailView
from crudbuilder.mixins import BaseDetailViewMixin
from .models import Software, Product
from .tables import ProductTable


class SoftwareDetailViewMixin(BaseDetailViewMixin):
    """mixin add some context"""
    def get_context_data(self, **kwargs):
        context = super(SoftwareDetailViewMixin, self).get_context_data(**kwargs)
        products = Product.objects.filter(software = self.object)
        context['table'] = ProductTable(products)
        return context

class SoftwareDetailView(SoftwareDetailViewMixin, DetailView):
    """software detail view"""
    model = Software
    inlineformset = None
    permissions = False
    custom_postfix_url = None
    permission_required = False
    template_name = 'applications/detail.html'


def verify_software(request, id):
    """verify software in homepage or status"""
    try:
        soft = Software.objects.get(id=id)
    except Software.DoesNotExist:
        return HttpResponseRedirect(reverse('applications-softwares-list'))
    if request.method =="POST":
        form = SoftwareForm(data = request.POST, instance=soft)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('applications-softwares-list'))
        return HttpResponseRedirect(reverse('applications-softwares-list'))
    else:
        form = SoftwareForm(instance=soft)
        return render(request, "applications/verify.html", {'form':form,'id':id})


def show_software(request, id):
    """verify software in homepage or status"""
    try:
        soft = Software.objects.get(id=id)
    except Software.DoesNotExist:
        return HttpResponseRedirect(reverse('applications-softwares-list'))
    if request.method =="POST":
        form = SoftwareShowForm(data = request.POST, instance=soft)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('applications-softwares-list'))
        return HttpResponseRedirect(reverse('applications-softwares-list'))
    else:
        form = SoftwareShowForm(instance=soft)
        return render(request, "applications/show.html", {'form':form,'id':id})


class PlanDetailView(BaseDetailViewMixin,DetailView):
    """plan detail view"""
    from common.apps.orders.models import Plans
    model = Plans
    inlineformset = None
    permissions = False
    custom_postfix_url = None
    permission_required = False
    template_name = 'plans/detail.html'