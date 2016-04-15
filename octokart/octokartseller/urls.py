from django.conf.urls import url, include, patterns

from octokartseller import views

urlpatterns = [
    url(r'^$', views.mainpage, name = "mainpage"),
]