from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Packages
from django.http.response import JsonResponse
from common.utilities.views import ObjectListView, ObjectEditView
from . import filters,tables
from django.views.generic import View
from .forms import PackageForm
from django.utils.decorators import method_decorator


# Create your views here.
@login_required
def list_user_products(request, template_name='packages/product_list.html'):
    if request.method == 'GET':
        pkgs = Packages.objects.filter(client__pk=request.user.pk)
        return render(request, template_name, {'pkg_list': pkgs})
    else:
        name = request.POST.get('packagename', '').strip()
        if  name != '':
            pkg = get_object_or_404(Packages, uuid=request.POST.get('packageid'))
            pkg.package_name = name
            pkg.save()
            return JsonResponse({'retcode':0, 'desc':'update successfully'})
        return JsonResponse({'retcode':1, 'desc':'updating fails'})
    
@login_required    
def product_details(request, pid, template_name='packages/product_detail.html'):
    #pkg = Packages.objects.filter(user__pk=request.user.pk).get(id=pid)
    
    pkg = get_object_or_404(Packages, client__pk=request.user.pk, uuid=pid, status='Active')
    return render(request, template_name, {'pkg': pkg})

@method_decorator(login_required, name='dispatch')
class PackageListView(ObjectListView):
    '''Package list view'''
    queryset = Packages.objects.all()
    filter = filters.PackageFilter
    #filter_form = filter.form
    table = tables.PackageTable
    template_name = 'packages/package_list.html'
    
@method_decorator(login_required, name='dispatch')    
class PackageView(View):
    """Package object view"""
    def get(self,request,uuid):
        pkg = get_object_or_404(Packages,uuid=uuid)
        return render(request, "packages/package.html", {'pkg':pkg})
    
@method_decorator(login_required, name='dispatch')
class PackageEditView(ObjectEditView):
    """package edit view"""
    model = Packages
    form_class = PackageForm
    template_name = 'packages/product_update_staff.html'
    default_return_url = 'packages:list'