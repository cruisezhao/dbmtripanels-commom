from django.conf.urls import url

from . import views, crud_views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(template_name='login.html'), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    #crud urls
    url(r'^$', crud_views.ClientListView.as_view(), name='client_list'),
    # url(r'^add/$', views.ClientEditView.as_view(), name='client_add'),
    # url(r'^import/$', views.ClientBulkImportView.as_view(), name='client_import'),
    # url(r'^edit/$', views.ClientBulkEditView.as_view(), name='client_bulk_edit'),
    # url(r'^delete/$', views.ClientBulkDeleteView.as_view(), name='client_bulk_delete'),
    # url(r'^(?P<uuid>[a-z\d]{32})/$', views.ClientView.as_view(), name='client'),
    # url(r'^(?P<uuid>[a-z\d]{32})/edit/$', views.ClientEditView.as_view(), name='client_edit'),
    # url(r'^(?P<uuid>[a-z\d]{32})/delete/$', views.ClientDeleteView.as_view(), name='client_delete'),
]
