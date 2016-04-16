from django.conf.urls import patterns, url
from store import views

urlpatterns = [
        url(r'^$', views.get_index, name='get_index'),
        url(r'^buy/$', views.buy_item, name='buy_item'),
        url(r'^get_catalogue/$', views.get_catalogue, name='get_catalogue'),
        url(r'^item/(?P<item_id>[0-9]+)$', views.get_item, name='get_item'),
]
