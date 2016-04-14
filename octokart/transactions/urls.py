from django.conf.urls import patterns, url
from transactions import views

urlpatterns = [
        url(r'^connections_manager/$', views.connections_manager, name='connections_manager'),
        url(r'^connections_manager/add_connection/$', views.add_connection, name='add_connection'),
        url(r'^connections_manager/receive_connection/$', views.receive_connection, name='receive_connection'),
        url(r'^connections_manager/check_connection/$', views.check_connection, name='check_connection'),
        url(r'^connections_manager/delete_connections/$', views.delete_connections, name='delete_connections'),
        url(r'^perform_transaction/$', views.perform_transaction, name='perform_transaction'),
        url(r'^prepare/$', views.prepare_for_commit, name='prepare'),
        url(r'^commit/$', views.commit, name='commit'),
        ]