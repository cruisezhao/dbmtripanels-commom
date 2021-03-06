'''
Created on Jun 13, 2017

@author: ben
'''


from django.conf.urls import url
from django.contrib.auth import views
from . import forms


admin_urlpatterns = [
     url('^login/$',views.login, {'template_name': 'users/login.html',
                                  'authentication_form':forms.AuthenticationFormWithAdminGroupOkay}, name='login'),
     url('^logout/$',views.logout, name='logout'),
]

staff_urlpatterns = [
     url('^login/$',views.login, {'template_name': 'users/login.html',
                                  'authentication_form':forms.AuthenticationFormWithStaffGroupOkay}, name='login'),
     url('^logout/$',views.logout, name='logout'),
]