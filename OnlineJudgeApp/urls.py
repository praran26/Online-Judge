from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$',auth_views.login,{'template_name': 'OnlineJudgeApp/login.htm'},name='login'),
	url(r'^dashboard/$',views.dashboard,name='dashboard'),
	url(r'^contests/$',views.contests,name='contests'),
	url(r'^problemset/$',views.problemset,name='problemset'),
	url(r'^settings/$',views.settings,name='settings'),
	url(r'^logout/$',auth_views.logout,{'next_page': '/'},name='logout'),
	url(r'^contests/(?P<pk>\d+)/standings/',views.standings,name='standings'),
	url(r'^contests/(?P<pk>\d+)/problems/',views.problems,name='problems'),
	url(r'^add/blog/$',views.add_blog,name='add_blog'),
	url(r'^add/problem/$',views.add_problem,name='add_problem'),
	url(r'^add/contest/$',views.add_contest,name='add_contest'),
	url(r'^user/(?P<user_id>\w+)/',views.user,name='user'),
	url(r'^blog/(?P<blog_id>\d+)/',views.blog,name='blog'),
	url(r'^post_blog/$',views.post_blog,name='post_blog'),
	url(r'^post_problem/$',views.post_problem,name='post_problem'),
	url(r'^post_contest/$',views.post_contest,name='post_contest'),
	
]