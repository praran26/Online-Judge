from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import Http404  
from datetime import datetime,timedelta
from django.contrib.auth import logout
from django.core.files.base import ContentFile
from django.conf import settings as settingsFile
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
import random,os,shutil,subprocess,resource,functools,hashlib
from django.contrib.auth import authenticate, login as login_user
from django.core.exceptions import PermissionDenied
from base64 import b64encode,b64decode
# Create your views here.
@login_required
def dashboard(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT a.blog_id,a.title,a.content,b.username,a.timestamp FROM OnlineJudgeApp_blog a,auth_user b WHERE a.isImportant=1 AND b.id=a.user_id")
		temp=dict()
		temp['importantBlogs']=[dict(zip(["blog_id","title","content","username","timestamp"],i)) for i in cursor.fetchall()]
		cursor.execute("SELECT a.blog_id,a.title,b.username FROM OnlineJudgeApp_blog a,auth_user b WHERE b.id=a.user_id ORDER BY a.timestamp DESC LIMIT 10")
		temp['recentBlogs']=[dict(zip(["blog_id","title","username"],i)) for i in cursor.fetchall()]
		cursor.execute("SELECT a.username,b.rating FROM auth_user a, OnlineJudgeApp_profile b WHERE a.id=b.user_id ORDER BY b.rating desc LIMIT 5")
		temp['topRated']=[dict(zip(["username","rating"],i)) for i in cursor.fetchall()]
	return render(request, 'OnlineJudgeApp/dashboard.htm',temp)

@login_required
def contests(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM OnlineJudgeApp_contest ORDER BY start_time")
		res=cursor.fetchall()
		temp=dict()
		temp['pastContests']=[dict(zip(["contest_id","start_time","duration"],i)) for i in res if i[1]+timedelta(microseconds=i[2])<datetime.now()]
		temp['presentContests']=[dict(zip(["contest_id","start_time","duration"],i)) for i in res if i[1]+timedelta(microseconds=i[2])>=datetime.now() and i[1]<=datetime.now()]
		temp['futureContests']=[dict(zip(["contest_id","start_time","duration"],i)) for i in res if i[1]>datetime.now()]
		for i in temp['pastContests']:
			i["duration"]=str(timedelta(microseconds=i["duration"]))
		for i in temp['presentContests']:
			i["duration"]=str(timedelta(microseconds=i["duration"]))
		for i in temp['futureContests']:
			i["duration"]=str(timedelta(microseconds=i["duration"]))
		
		return render(request, 'OnlineJudgeApp/contests.htm',temp)

@login_required
def problemset(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT prob_id,name,user_solved FROM OnlineJudgeApp_problem WHERE addedToPractice='1'")
		probs=cursor.fetchall()
		headers=["id","name","user_solved"]
		temp=[dict(zip(headers,i)) for i in probs]
		for idx,prob in enumerate(temp):
			cursor.execute("SELECT * FROM OnlineJudgeApp_probcontest WHERE problem_id=%d;"%(int(prob["id"])))
			record=cursor.fetchone()
			temp[idx]["idx"]=record[1]
			temp[idx]["contest_id"]=record[2]
			cursor.execute("SELECT tag_id FROM OnlineJudgeApp_probtag WHERE prob_id=%d;"%(int(prob["id"])))
			records=cursor.fetchall()
			tags=[i[0] for i in records]
			if tags:
				temp[idx]["tags"]=", ".join(tags)
			else:
				temp[idx]["tags"]=""
		return render(request, 'OnlineJudgeApp/problemset.htm',{'prob_list':temp})

@login_required
def settings(request):
	return render(request, 'OnlineJudgeApp/settings.htm',{})

@login_required
def logout(request):
	return HttpResponseRedirect(reverse('login'))

@login_required
def standings(request,contest_id):
	return render(request, 'OnlineJudgeApp/standings.htm',{})

@login_required
def problems(request,contest_id,problem_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT start_time FROM OnlineJudgeApp_contest WHERE contest_id=%d;"%(int(contest_id)))
		res=cursor.fetchone()
		if res[0]>datetime.now():
			raise Http404
	with connection.cursor() as cursor:
		cursor.execute("SELECT problem_id FROM OnlineJudgeApp_probcontest WHERE contest_id=%d AND idx='%s'"%(int(contest_id),problem_id))
		res=cursor.fetchone()[0]
		cursor.execute("SELECT name,content,time_limit,mem_limit FROM OnlineJudgeApp_problem WHERE prob_id=%d;"%(int(res)))
		headers=["name","content","time_limit","mem_limit"]
		temp=dict(zip(headers,cursor.fetchone()))
		temp["idx"]=problem_id
		temp["contest_id"]=contest_id
		cursor.execute("SELECT a.sub_id,a.timestamp,a.verdict FROM OnlineJudgeApp_submission a WHERE a.user_id=%d AND a.prob_id_id=%d;"%(int(request.user.id),int(res)))
		temp["submissions"]=[dict(zip(["sub_id","timestamp","verdict"],i)) for i in cursor.fetchall()]
		return render(request, 'OnlineJudgeApp/problems.htm',temp)
@login_required
def contest(request,contest_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT start_time FROM OnlineJudgeApp_contest WHERE contest_id=%d;"%(int(contest_id)))
		res=cursor.fetchone()
		if res[0]>datetime.now():
			raise Http404
	with connection.cursor() as cursor:
		cursor.execute("SELECT problem_id,idx FROM OnlineJudgeApp_probcontest WHERE contest_id=%d ORDER BY idx;"%(int(contest_id)))
		probs=cursor.fetchall()
		temp=[]
		for i in probs:
			cursor.execute("SELECT name FROM OnlineJudgeApp_problem WHERE prob_id=%d;"%(int(i[0])))
			cur=[("idx",i[1]),("name",cursor.fetchone()[0])]
			temp.append(dict(cur))
		vals=dict()
		vals["prob_list"]=temp
		vals["contest_id"]=contest_id
		return render(request, 'OnlineJudgeApp/contest.htm',vals)
@login_required
def add_blog(request):
	return render(request, 'OnlineJudgeApp/add_blog.htm',{})

@login_required
def add_problem(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM OnlineJudgeApp_tag ORDER BY tag")
		return render(request, 'OnlineJudgeApp/add_problem.htm',{"tags":list(i[0] for i in cursor.fetchall())})

@login_required
def add_contest(request):
	with connection.cursor() as cursor:
		cur_user=request.user.id
		cursor.execute("SELECT prob_id, name FROM OnlineJudgeApp_problem WHERE addedToPractice=0 AND setter_id=%d"%(cur_user))
		res=cursor.fetchall()
		return render(request, 'OnlineJudgeApp/add_contest.htm',{'prob_list':res})

@login_required
def user(request,user_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT b.id,b.username,a.rating,b.email,b.first_name,b.last_name,b.date_joined,b.is_active,b.is_superuser FROM OnlineJudgeApp_profile a,auth_user b WHERE a.user_id=b.id AND b.username='%s'"%(user_id))
		res=cursor.fetchone()
		headers=["id","username","rating","email","first_name","last_name","date_joined","is_active","is_superuser"]
		temp=dict(zip(headers,res))
		cursor.execute("SELECT blog_id,title FROM OnlineJudgeApp_blog WHERE user_id=%d;"%(int(temp["id"])))
		temp["blogs"]=[dict(zip(["blog_id","title"],i)) for i in cursor.fetchall()]
		return render(request, 'OnlineJudgeApp/user.htm',temp)

@login_required
def ban_user(request,user_id):
	if request.user.is_superuser:
		with connection.cursor() as cursor:
			cursor.execute("UPDATE auth_user SET is_active=0 WHERE username='%s';"%(user_id))
		return HttpResponseRedirect(reverse('user',kwargs={'user_id':user_id}))

@login_required
def unban_user(request,user_id):
	if request.user.is_superuser:
		with connection.cursor() as cursor:
			cursor.execute("UPDATE auth_user SET is_active=1 WHERE username='%s';"%(user_id))
		return HttpResponseRedirect(reverse('user',kwargs={'user_id':user_id}))

@login_required
def blog(request,blog_id):
	res=()
	column=()
	comments=[]
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM OnlineJudgeApp_blog WHERE blog_id=%d;"%(int(blog_id)))
		res=cursor.fetchone()
		columns=[col[0] for col in cursor.description]
		cursor.execute("SELECT * FROM OnlineJudgeApp_comment WHERE blog_id=%d;"%(int(blog_id)))
		comments=cursor.fetchall()
	comments=map(list,comments)
	if res:
		temp=dict(zip(columns,res))
		with connection.cursor() as cursor:
			cursor.execute("SELECT username FROM auth_user WHERE id=%d;"%(int(temp['user_id'])))
			temp['user_id']=str(cursor.fetchone()[0])
			for idx,comment in enumerate(comments):
				cursor.execute("SELECT username FROM auth_user WHERE id=%d;"%(int(comment[-1])))
				comments[idx][-1]=str(cursor.fetchone()[0])
			cursor.execute("SELECT a.blog_id,a.title,b.username FROM OnlineJudgeApp_blog a,auth_user b WHERE b.id=a.user_id ORDER BY a.timestamp DESC LIMIT 10")
			temp['recentBlogs']=[dict(zip(["blog_id","title","username"],i)) for i in cursor.fetchall()]
			cursor.execute("SELECT a.username,b.rating FROM auth_user a, OnlineJudgeApp_profile b WHERE a.id=b.user_id ORDER BY b.rating desc LIMIT 5")
			temp['topRated']=[dict(zip(["username","rating"],i)) for i in cursor.fetchall()]
		comments=map(tuple,comments)
		headers=["id","content","timestamp","blog","author"]
		comments=[dict(zip(headers,comment)) for comment in comments]
		temp["comments"]=comments
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
		problem_tags=request.POST.getlist('problem-tags')
		setter=str(request.user.id)
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO OnlineJudgeApp_problem (name,content,time_limit,mem_limit,addedToPractice,user_solved,checker,setter_id) VALUES ('%s','%s',%d,%d,'%s',%d,'%s','%s')"%(problem_title,problem_legend,int(problem_tl),int(problem_ml),0,0,problem_checker,setter))
			cursor.execute("SELECT LAST_INSERT_ID()")
			idx=cursor.fetchone()[0]
			for tag in problem_tags:
				cursor.execute("INSERT INTO OnlineJudgeApp_probtag (prob_id,tag_id) VALUES (%d,'%s')"%(int(idx),tag))
			return HttpResponseRedirect(reverse('add_tests',kwargs={'problem_id':idx}))

@login_required
def add_tests(request,problem_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT setter_id FROM OnlineJudgeApp_problem WHERE prob_id='%s'"%(problem_id))
		x=cursor.fetchone()
		if not x or x[0]!=request.user.id:
			raise PermissionDenied
		return render(request,'OnlineJudgeApp/add_tests.htm',{'problem_id':problem_id})

def post_tests(request):
	if request.POST:
		problem=request.POST['problem_id']
		test_case=request.FILES['test_case'].read()
		test_case=b64encode(test_case)
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO OnlineJudgeApp_test (data,problem_id) VALUES ('%s',%d)"%(test_case,int(problem)))
		return HttpResponseRedirect(reverse('add_tests',kwargs={'problem_id':problem}))

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

@login_required
def post_comment(request,blog_id):
	if request.POST:
		user=request.user.id
		content=request.POST['comment_content'].replace('\\','\\\\')
		timestamp=str(datetime.now())
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO OnlineJudgeApp_comment (content,timestamp,blog_id,user_id) VALUES ('%s','%s',%d,%d)"%(content,timestamp,int(blog_id),int(user)))
	return HttpResponseRedirect(reverse('blog',kwargs={'blog_id':blog_id}))

@login_required
def update_profile(request):
	if request.POST:
		oldpass=request.POST['old_pass']
		newpass=request.POST['new_pass']
		confirmpass=request.POST['confirm_pass']
		request.user.set_password(newpass)
		request.user.save()
		logout(request)
	return HttpResponseRedirect(reverse('dashboard'))

@login_required
def make_important(request,blog_id):
	with connection.cursor() as cursor:
		cursor.execute("UPDATE OnlineJudgeApp_blog SET isImportant=1 WHERE blog_id=%d;"%(int(blog_id)))
	return HttpResponseRedirect(reverse('blog',kwargs={'blog_id':blog_id}))

@login_required
def remove_important(request,blog_id):
	with connection.cursor() as cursor:
		cursor.execute("UPDATE OnlineJudgeApp_blog SET isImportant=0 WHERE blog_id=%d;"%(int(blog_id)))
	return HttpResponseRedirect(reverse('blog',kwargs={'blog_id':blog_id}))

def check(folder,code_name,checker_name,mem,time):
	p=subprocess.Popen(["g++",code_name,"-O2","-o","code","-std=c++14"],cwd=folder)
	ret_code=p.wait()
	if ret_code<0:
		return 1
	p=subprocess.Popen(["./code"],cwd=folder,stdout=open(folder+"/output.txt","w+"),stdin=open(folder+"/input.txt","r"),shell=True)
	ret_code=p.wait()
	if ret_code<0:
		return 1
	p=subprocess.Popen(["g++", "-O2",checker_name,"-o","checker","-std=c++14"],cwd=folder)
	ret_code=p.wait()
	if ret_code<0:
		return 1
	p=subprocess.Popen("./checker",cwd=folder)
	ret_code=p.wait()
	if ret_code<0:
		return 1
	return 0
@login_required
def submit(request,contest_id,problem_id):
	if request.POST:
		folder=""
		for i in range(30):
			folder+=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvqxyz')
		filename=request.FILES['submit_code_file'].name
		filename=filename.replace('/','_')
		BASE_PATH=settingsFile.MEDIA_ROOT
		try:
			os.makedirs(os.path.join(BASE_PATH,folder))
		except:
			pass
		files_path=os.path.join(BASE_PATH,folder)
		full_filename=os.path.join(files_path,filename)
		fout=open(full_filename,'wb+')
		file_content=ContentFile(request.FILES['submit_code_file'].read())
		try:
			for chunk in file_content.chunks():
				fout.write(chunk)
			fout.close()
		except:
			assert False
		checker=""
		prob_id=0
		TL=0
		ML=0
		with connection.cursor() as cursor:
			cursor.execute("SELECT a.checker,a.prob_id,a.time_limit,a.mem_limit FROM OnlineJudgeApp_problem a,OnlineJudgeApp_probcontest b WHERE b.idx='%s' AND b.contest_id=%d AND a.prob_id=b.problem_id;"%(problem_id,int(contest_id)))
			checker,prob_id,TL,ML=cursor.fetchone()
		prob_id=int(prob_id)
		full_checker=os.path.join(files_path,"checker_"+os.path.splitext(filename)[0]+".cpp")
		fout=open(full_checker,"w+")
		try:
			fout.write(checker)
			fout.close()
		except:
			pass
		bad=0
		with connection.cursor() as cursor:
			cursor.execute("SELECT a.data FROM OnlineJudgeApp_test a, OnlineJudgeApp_probcontest b WHERE b.idx='%s' AND b.contest_id=%d AND a.problem_id=b.problem_id;"%(problem_id,int(contest_id)))
			tests=cursor.fetchall()
			for test in tests:
				with open(os.path.join(files_path,"input.txt"),"w+") as f:
					f.write(b64decode(test[0]))
				bad|=check(files_path,filename,"checker_"+os.path.splitext(filename)[0]+".cpp",int(ML),int(TL))
				os.remove(os.path.join(BASE_PATH,folder,"input.txt"))
			cursor.execute("INSERT INTO OnlineJudgeApp_submission (timestamp,verdict,prob_id_id,user_id) VALUES ('%s','%s',%d,%d);"%(str(datetime.now()),"AC" if not bad else "RJ",prob_id,int(request.user.id)))
		if os.path.isdir(os.path.join(BASE_PATH,folder)):
			shutil.rmtree(os.path.join(BASE_PATH,folder))
		return HttpResponseRedirect(reverse('problems',kwargs={'contest_id':contest_id,'problem_id':problem_id}))
def home(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		return HttpResponseRedirect(reverse('login'))
def register(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		return render(request,'OnlineJudgeApp/register.htm')
def login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		return render(request,'OnlineJudgeApp/login.htm')
def registration_post(request):
	if request.POST:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM auth_user x WHERE x.email='%s' AND NOT EXISTS (SELECT * FROM OnlineJudgeApp_regnconfirm y WHERE x.id=y.user_id)"%(request.POST["email"]))
			if cursor.fetchall():
				messages.add_message(request,messages.ERROR,"There is already an account associated with email. Please try login instead.")
				return HttpResponseRedirect(reverse('login'))
			cursor.execute("SELECT * FROM auth_user x WHERE x.username='%s'"%(request.POST["username"]))
			if cursor.fetchall():
				messages.add_message(request,messages.ERROR,"There is already an account associated with handle. Please try another handle.")
				return HttpResponseRedirect(reverse('registration'))
			User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'],first_name=request.POST['first'],last_name=request.POST['last'])
			cursor.execute("SELECT * FROM auth_user WHERE id=(SELECT LAST_INSERT_ID());")
			user=cursor.fetchone()
			mystr=str(user[1])+str(user[4])+str(user[10])
			hashval=hashlib.sha512(mystr).hexdigest()
			cursor.execute("INSERT INTO OnlineJudgeApp_regnconfirm (user_id,hashval) VALUES (%d,'%s');"%(int(user[0]),hashval))
			subject,from_email,to='Verify Online Judge email address','admin@onlinejudge.org',request.POST['email']
			text_content='Please verify your email address. Ignore if not registered on the Online Judge.'
			html_content='<a href="%s">Verify!</a>'%(request.build_absolute_uri(reverse(verify_email,kwargs={'hash_val':hashval})))
			msg=EmailMultiAlternatives(subject,text_content,from_email,[to])
			msg.attach_alternative(html_content,"text/html")
			msg.send()
		return render(request,'OnlineJudgeApp/registration_post.htm')
def login_post(request):
	if request.POST:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM auth_user x WHERE x.username='%s' AND EXISTS (SELECT * FROM OnlineJudgeApp_regnconfirm y WHERE x.id=y.user_id)"%(request.POST["username"]))
			if cursor.fetchall():
				messages.add_message(request,messages.ERROR,"Please verify your email.")
				return HttpResponseRedirect(reverse('login'))
			cursor.execute("SELECT * FROM auth_user x WHERE x.username='%s'"%(request.POST["username"]))
			a=cursor.fetchone()
			if not a:
				messages.add_message(request,messages.ERROR,"Handle does not exist. Please try again.")
				return HttpResponseRedirect(reverse('login'))
			if a[9]==0:
				messages.add_message(request,messages.ERROR,"You have been banned by admin.")
				return HttpResponseRedirect(reverse('login'))
			user=authenticate(username=request.POST['username'],password=request.POST['password'])
			if user is not None:
				login_user(request,user)
				return HttpResponseRedirect(reverse('dashboard'))
			else:
				messages.add_message(request,messages.ERROR,"Invalid password. Please try again.")
				return HttpResponseRedirect(reverse('login'))
def verify_email(request,hash_val):
	with connection.cursor() as cursor:
		cursor.execute("SELECT user_id FROM OnlineJudgeApp_regnconfirm WHERE hashval='%s';"%(hash_val));
		a=cursor.fetchall()
		if not a:
			raise Http404
		else:
			cursor.execute("DELETE FROM OnlineJudgeApp_regnconfirm WHERE user_id=%d;"%(int(a[0][0])));
			messages.add_message(request,messages.SUCCESS,"Your email has been successfully verified. You may login now.")
			return HttpResponseRedirect(reverse('home'))

@login_required
def delete_blog(request,blog_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT user_id FROM OnlineJudgeApp_blog WHERE blog_id=%d;"%(int(blog_id)))
		if request.user.is_superuser or cursor.fetchone()[0]==request.user.id:
			cursor.execute("DELETE FROM OnlineJudgeApp_blog WHERE blog_id=%d;"%(int(blog_id)))
			return HttpResponseRedirect(reverse('dashboard'))
		else:
			raise PermissionDenied

@login_required
def edit_blog(request,blog_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT user_id FROM OnlineJudgeApp_blog WHERE blog_id=%d;"%(int(blog_id)))
		if request.user.is_superuser or cursor.fetchone()[0]==request.user.id:
			cursor.execute("SELECT * FROM OnlineJudgeApp_blog WHERE blog_id=%d;"%(int(blog_id)))
			headers=["blog_id","title","content","timestamp","isImportant","user_id"]
			res=dict(zip(headers,cursor.fetchone()))
			return render(request,"OnlineJudgeApp/edit_blog.htm",res)
		else:
			raise PermissionDenied

@login_required
def edit_problem(request,problem_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT setter_id FROM OnlineJudgeApp_problem WHERE prob_id=%d;"%(int(problem_id)))
		if request.user.is_superuser or cursor.fetchone()[0]==request.user.id:
			cursor.execute("SELECT * FROM OnlineJudgeApp_problem WHERE prob_id=%d;"%(int(problem_id)))
			headers=["prob_id","name","content","time_limit","mem_limit","addedToPractice","user_solved","checker","setter_id"]
			res=dict(zip(headers,cursor.fetchone()))
			cursor.execute("SELECT * FROM OnlineJudgeApp_tag ORDER BY tag")
			res["tags"]=list(i[0] for i in cursor.fetchall())
			return render(request,"OnlineJudgeApp/edit_problem.htm",res)
		else:
			raise PermissionDenied
@login_required
def update_problem(request,problem_id):
	if request.POST:
		with connection.cursor() as cursor:
			cursor.execute("UPDATE OnlineJudgeApp_problem SET name='%s', content='%s', time_limit=%d, mem_limit=%d,checker='%s' WHERE prob_id=%d;"%(
				request.POST['problem-name'],
				request.POST['problem-legend'],
				int(request.POST['problem-tl']),
				int(request.POST['problem-ml']),
				request.POST['problem-checker'],
				int(problem_id)
				))
		return HttpResponseRedirect(reverse('unused_problems'))
@login_required
def update_blog(request,blog_id):
	if request.POST:
		with connection.cursor() as cursor:
			cursor.execute("UPDATE OnlineJudgeApp_blog SET content='%s' WHERE blog_id=%d;"%(request.POST['blog-content'].replace('\\','\\\\'),int(blog_id)))
		return HttpResponseRedirect(reverse('blog',kwargs={'blog_id':blog_id}))

@login_required
def delete_comment(request,comment_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT user_id,blog_id FROM OnlineJudgeApp_comment WHERE comment_id=%d;"%(int(comment_id)))
		res=cursor.fetchone()
		if request.user.is_superuser or res[0]==request.user.id:
			cursor.execute("DELETE FROM OnlineJudgeApp_comment WHERE comment_id=%d;"%(int(comment_id)))
			return HttpResponseRedirect(reverse('blog',kwargs={'blog_id':res[1]}))
		else:
			raise PermissionDenied
@login_required
def unused_problems(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM OnlineJudgeApp_problem WHERE setter_id=%d;"%(int(request.user.id)))
		headers=["prob_id","name","content","time_limit","mem_limit","addedToPractice","user_solved","checker","setter_id"]
		res=[dict(zip(headers,i)) for i in cursor.fetchall()]
		return render(request,"OnlineJudgeApp/unused_problems.htm",{"problems":res})

@login_required
def add_tag(request):
	if request.user.is_superuser:
		return render(request,"OnlineJudgeApp/add_tag.htm")
	else:
		raise PermissionDenied

@login_required
def post_tag(request):
	if request.POST:
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO OnlineJudgeApp_tag VALUES ('%s')"%(request.POST['tag-name']))
		return HttpResponseRedirect(reverse('add_problem'))

def checker_example(request):
	return HttpResponse(r"""
<title>Example checker</title>
<pre>
// Here is an example checker to check if program takes two integers as input and prints their sum
// Take input from input.txt
// Take ouput from output.txt
// If output is incorrect, return non-zero exit code

#include "bits/stdc++.h"

using namespace std;

int main(){
	ifstream f_input;
	ifstream f_output;
	f_input.open("input.txt",ios::in);
	int a,b;
	f_input>>a>>b;
	f_input.close();
	f_output.open("output.txt",ios::in);
	int c;
	f_output>>c;
	f_output.close();
	assert(a+b==c);
	return 0;
}
</pre>
	""")