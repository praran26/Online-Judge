from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$',views.home,name="home"),
	url(r'^login/$',views.login,name='login'),
	url(r'^dashboard/$',views.dashboard,name='dashboard'),
	url(r'^contests/$',views.contests,name='contests'),
	url(r'^problemset/$',views.problemset,name='problemset'),
	url(r'^settings/$',views.settings,name='settings'),
	url(r'^logout/$',auth_views.logout,{'next_page': '/'},name='logout'),
	url(r'^contests/(?P<contest_id>\d+)/$',views.contest,name='contest'),
	url(r'^contests/(?P<contest_id>\d+)/standings/$',views.standings,name='standings'),
	url(r'^contests/(?P<contest_id>\d+)/problems/(?P<problem_id>\w)/$',views.problems,name='problems'),
	url(r'^add/blog/$',views.add_blog,name='add_blog'),
	url(r'^add/problem/$',views.add_problem,name='add_problem'),
	url(r'^add/contest/$',views.add_contest,name='add_contest'),
	url(r'^user/(?P<user_id>\w+)/$',views.user,name='user'),
	url(r'^blog/(?P<blog_id>\d+)/$',views.blog,name='blog'),
	url(r'^post_blog/$',views.post_blog,name='post_blog'),
	url(r'^post_problem/$',views.post_problem,name='post_problem'),
	url(r'^post_contest/$',views.post_contest,name='post_contest'),
	url(r'^post_comment/(?P<blog_id>\d+)/$',views.post_comment,name='post_comment'),
	url(r'^update_profile/$',views.update_profile,name='update_profile'),
	url(r'^make_important/(?P<blog_id>\d+)/$',views.make_important,name='makeImportant'),
	url(r'^remove_important/(?P<blog_id>\d+)/$',views.remove_important,name='removeImportant'),
	url(r'^contests/(?P<contest_id>\d+)/problems/(?P<problem_id>\w)/submit/$',views.submit,name='submit'),
	url(r'^register/$',views.register,name='registration'),
	url(r'^registration_post/$',views.registration_post,name='registration_post'),
	url(r'^verify_email/(?P<hash_val>\w+)/$',views.verify_email,name="verify_email"),
	url(r'^login_post/$',views.login_post,name='login_post')
]