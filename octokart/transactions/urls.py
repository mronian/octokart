from django.conf.urls import patterns, url
from transactions import views

urlpatterns = [
        url(r'^connections_manager/$', views.connections_manager, name='connections_manager'),
        ]