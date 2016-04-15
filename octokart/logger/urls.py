from django.conf.urls import url

from . import views

urlpatterns = [
				url(r'^$', views.locallogs, name = 'locallogs'),
				url(r'^alllogs/', views.alllogs, name = 'alllogs'),
               ]