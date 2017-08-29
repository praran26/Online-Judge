from django.shortcuts import render

# Create your views here.
def dashboard(request):
	return render(request, 'OnlineJudgeApp/dashboard.htm',{})
def contests(request):
	return render(request, 'OnlineJudgeApp/contests.htm',{})
def problemset(request):
	return render(request, 'OnlineJudgeApp/problemset.htm',{})
def settings(request):
	return render(request, 'OnlineJudgeApp/settings.htm',{})
