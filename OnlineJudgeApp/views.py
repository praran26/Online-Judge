from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.
def dashboard(request):
	return render(request, 'OnlineJudgeApp/dashboard.htm',{})
def contests(request):
	return render(request, 'OnlineJudgeApp/contests.htm',{})
def problemset(request):
	return render(request, 'OnlineJudgeApp/problemset.htm',{})
def settings(request):
	return render(request, 'OnlineJudgeApp/settings.htm',{})
def login(request):
	return render(request, 'OnlineJudgeApp/login.htm',{})
def logout(request):
	return HttpResponseRedirect(reverse('login'))
def standings(request,pk):
	return render(request, 'OnlineJudgeApp/standings.htm',{})
def problems(request,pk):
	return render(request, 'OnlineJudgeApp/problems.htm',{})
def add_blog(request):
	return render(request, 'OnlineJudgeApp/add_blog',{})
def add_problem(request):
	return render(request, 'OnlineJudgeApp/add_problem',{})
def add_contest(request):
	return render(request, 'OnlineJudgeApp/add_contest',{})