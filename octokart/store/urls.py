from django.conf.urls import patterns, url
from store import views

urlpatterns = [
        url(r'^index/$', views.get_index, name='get_index'),
]
