from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.login,name='login'),
	url(r'^dashboard/$',views.dashboard,name='dashboard'),
	url(r'^contests/$',views.contests,name='contests'),
	url(r'^problemset/$',views.problemset,name='problemset'),
	url(r'^settings/$',views.settings,name='settings'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^contests/(?P<pk>\d+)/standings/',views.standings,name='standings'),
	url(r'^contests/(?P<pk>\d+)/problems/',views.problems,name='problems'),
]