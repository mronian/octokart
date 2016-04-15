from django.conf.urls import patterns, url
from store import views

urlpatterns = [
        # url(r'^login/$', views.login, name='login'),
        # url(r'^register/$', views.register, name='register'),
        # url(r'^logout/$', views.logout, name='logout'),
        url(r'^$', views.display_store, name='display_store'),
        ]