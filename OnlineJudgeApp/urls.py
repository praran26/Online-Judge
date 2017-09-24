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
	url(r'^add/blog/$',views.add_blog,name='add_blog'),
	url(r'^add/problem/$',views.add_problem,name='add_problem'),
	url(r'^add/contest/$',views.add_contest,name='add_contest'),
]