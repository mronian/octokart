from django.conf.urls import patterns, url
from locks import views

urlpatterns = [
        url(r'^seller/request/$', views.seller_request, name='seller_request'),
        url(r'^seller/release/$', views.seller_release, name='seller_release'),
        url(r'^items/request/$', views.items_request, name='items_request'),
        url(r'^items/release/$', views.items_release, name='items_release'),
        url(r'^items/empty/$', views.items_empty, name='items_empty'),
        url(r'^seller/empty/$', views.seller_empty, name='seller_empty'),
        ]