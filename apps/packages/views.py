from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Packages
from django.http.response import JsonResponse


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
    
    pkg = get_object_or_404(Packages, client__pk=request.user.pk, id=pid, status='Active')
    return render(request, template_name, {'pkg': pkg})
