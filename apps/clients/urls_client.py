from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(template_name='login.html'), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    #url(r'^avatar/$', views.avatar, kwargs={'template_name':'account_client.html'}, name="avatar"),
    url(r'^profilebasic/$', views.profile_basic, kwargs={'template_name':'clients/profile_basic.html'}, name="profile_basic"),
    url(r'^profilecontact/$', views.profile_contact, kwargs={'template_name':'clients/profile_contact.html'}, name="profile_contact"),
    url(r'^profilesocial/$', views.profile_social, kwargs={'template_name':'clients/profile_social.html'}, name="profile_social"),
    url(r'^passwordchange/$', views.PasswordChangeView.as_view(template_name='clients/passwordchange.html'), name='passwordchange'),
    #url(r'^all/$', views.account_page_view, kwargs={'template_name':'account_client.html'}, name="all"),
]
