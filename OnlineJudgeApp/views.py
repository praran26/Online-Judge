from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection
from datetime import datetime
# Create your views here.
@login_required
def dashboard(request):
	return render(request, 'OnlineJudgeApp/dashboard.htm',{})

@login_required
def contests(request):
	return render(request, 'OnlineJudgeApp/contests.htm',{})

@login_required
def problemset(request):
	return render(request, 'OnlineJudgeApp/problemset.htm',{})

@login_required
def settings(request):
	return render(request, 'OnlineJudgeApp/settings.htm',{})

def login(request):
	return render(request, 'OnlineJudgeApp/login.htm',{})

@login_required
def logout(request):
	return HttpResponseRedirect(reverse('login'))

@login_required
def standings(request,pk):
	return render(request, 'OnlineJudgeApp/standings.htm',{})

@login_required
def problems(request,pk):
	return render(request, 'OnlineJudgeApp/problems.htm',{})

@login_required
def add_blog(request):
	return render(request, 'OnlineJudgeApp/add_blog.htm',{})

@login_required
def add_problem(request):
	return render(request, 'OnlineJudgeApp/add_problem.htm',{})

@login_required
def add_contest(request):
	return render(request, 'OnlineJudgeApp/add_contest.htm',{})

@login_required
def user(request,user_id):
	return render(request, 'OnlineJudgeApp/user.htm',{})

@login_required
def blog(request,blog_id):
	return render(request, 'OnlineJudgeApp/blog.htm',{})

@login_required
def post_blog(request):
	if request.POST:
		blog_title=request.POST['blog_title']
		blog_content=request.POST['blog_content']
		cur_user=str(request.user.id)
		timestamp=str(datetime.now())
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO OnlineJudgeApp_blog (title,content,user_id,timestamp,isImportant) VALUES ('%s','%s','%s','%s','%s')"%(blog_title,blog_content,cur_user,timestamp,0))
	return HttpResponseRedirect(reverse('dashboard'))