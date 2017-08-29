from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^dashboard/$',views.dashboard,name='dashboard'),
	url(r'^contests/$',views.contests,name='contests'),
	url(r'^problemset/$',views.problemset,name='problemset'),
	url(r'^settings/$',views.settings,name='settings'),
]