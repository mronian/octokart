from django.conf.urls import patterns, url
from store import views

urlpatterns = [
        url(r'^index/$', views.get_index, name='get_index'),
        url(r'^item/(?P<item_id>[0-9]+)$', views.get_item, name='get_item'),
]
