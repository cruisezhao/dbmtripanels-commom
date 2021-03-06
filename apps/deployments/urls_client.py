'''
Created on Jul 12, 2017

@author: ben
'''


from django.conf.urls import url
from common.apps.deployments.views import DeployView
from django.urls import reverse_lazy

urlpatterns = [    
    url(r'^deploy/(?P<package_id>\w+)/$', DeployView.as_view(success_url = reverse_lazy('packages:productlist')), name='deploy'),
]