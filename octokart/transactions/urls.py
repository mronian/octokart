from django.conf.urls import patterns, url
from transactions import views

urlpatterns = [
        url(r'^connections_manager/$', views.connections_manager, name='connections_manager'),
        url(r'^connections_manager/add_connection/$', views.add_connection, name='add_connection'),
        url(r'^connections_manager/check_connection/$', views.check_connection, name='check_connection'),
        url(r'^connections_manager/delete_connections/$', views.delete_connections, name='delete_connections'),
        ]