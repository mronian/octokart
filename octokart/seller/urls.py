from django.conf.urls import patterns, url
from seller import views

urlpatterns = [
        url(r'^get_catalogue/$', views.get_catalogue, name='get_catalogue'),
        url(r'^sync_catalogue/$', views.sync_catalogue, name='sync_catalogue'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', views.logout, name='logout'),
        ]