from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import Http404  
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
	with connection.cursor() as cursor:
		cur_user=request.user.id
		cursor.execute("SELECT prob_id, name FROM OnlineJudgeApp_problem WHERE addedToPractice=0 AND setter_id=%d"%(cur_user))
		res=cursor.fetchall()
		return render(request, 'OnlineJudgeApp/add_contest.htm',{'prob_list':res})

@login_required
def user(request,user_id):
	return render(request, 'OnlineJudgeApp/user.htm',{})

@login_required
def blog(request,blog_id):
	res=()
	column=()
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM OnlineJudgeApp_blog WHERE blog_id=%d;"%(int(blog_id)))
		res=cursor.fetchone()
		columns=[col[0] for col in cursor.description]
	if res:
		temp=dict(zip(columns,res))
		with connection.cursor() as cursor:
			cursor.execute("SELECT username FROM auth_user WHERE id=%d;"%(int(temp['user_id'])))
			temp['user_id']=str(cursor.fetchone()[0])
		return render(request, 'OnlineJudgeApp/blog.htm',temp)
	else:
		raise Http404
@login_required
def post_blog(request):
	if request.POST:
		blog_title=request.POST['blog-title']
		blog_content=request.POST['blog-content'].replace('\\','\\\\')
		cur_user=str(request.user.id)
		timestamp=str(datetime.now())
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO OnlineJudgeApp_blog (title,content,user_id,timestamp,isImportant) VALUES ('%s','%s','%s','%s','%s')"%(blog_title,blog_content,cur_user,timestamp,0))
	return HttpResponseRedirect(reverse('dashboard'))
@login_required
def post_problem(request):
	if request.POST:
		problem_title=request.POST['problem-name']
		problem_legend=request.POST['problem-legend'].replace('\\','\\\\')
		problem_tl=request.POST['problem-tl']
		problem_ml=request.POST['problem-ml']
		problem_checker=request.POST['problem-checker']
		setter=str(request.user.id)
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO OnlineJudgeApp_problem (name,content,time_limit,mem_limit,addedToPractice,user_solved,checker,setter_id) VALUES ('%s','%s',%d,%d,'%s',%d,'%s','%s')"%(problem_title,problem_legend,int(problem_tl),int(problem_ml),0,0,problem_checker,setter))
	return HttpResponseRedirect(reverse('dashboard'))
@login_required
def post_contest(request):
	if request.POST:
		duration=request.POST['contest-duration']
		start=request.POST['contest-start']
		selected_problems=request.POST.getlist('contest-problems')
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO OnlineJudgeApp_contest (start_time,duration) VALUES ('%s',%d)"%(start,int(duration)*60*1000000))
			cursor.execute("SELECT LAST_INSERT_ID()")
			contest_id=cursor.fetchone()[0]
			for idx,prob in enumerate(selected_problems):
				cursor.execute("INSERT INTO OnlineJudgeApp_probcontest (problem_id,contest_id,idx) VALUES ('%s','%s','%s')"%(prob,contest_id,chr(idx+ord('A'))))
				cursor.execute("UPDATE OnlineJudgeApp_problem SET setter_id=NULL WHERE prob_id=%d;"%(int(prob)))
				
	return HttpResponseRedirect(reverse('dashboard'))