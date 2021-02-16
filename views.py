from django.shortcuts import render

def home(request):
	content ={}
	content['home']="这是博客的首页"
	return render(request,'home.html',content)