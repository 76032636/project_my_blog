import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse

from .models import Profile
from .forms import LoginForm, RegisterFrom, ChangeNickNameFrom, BindEmailForm,ChangePasswordForm,ForgetPassword

def login(request):
	if request.method == 'POST':
		print('执行了post')
		login = LoginForm(request.POST)
		if login.is_valid():
			user = login.cleaned_data['user']
			auth.login(request, user)	
			return redirect(request.GET.get('from',reverse('home')))	
	else:
		login=LoginForm()
	
	content={}
	content['login_form'] = login
	return render(request,'user/login.html',content)

def loginModel(request):
	login = LoginForm(request.POST)
	date = {}
	if login.is_valid():
		
		user = login.cleaned_data['user']
		auth.login(request, user)	
		date['status'] = 'SUCCESS'
	else:
		print('不成功')
		date['status'] = 'ERROR'
	return JsonResponse(date)

def register(request):
	if request.method == 'POST':
		print('执行了post')
		register = RegisterFrom(request.POST,request=request)
		if register.is_valid():
			username = register.cleaned_data['username']
			password = register.cleaned_data['password_register']
			email = register.cleaned_data['email']
			user = User.objects.create_user(username,email,password)
			user.save()
			#删除用户侧保留的session中验证码部分
			del request.session['register']
			user = auth.authenticate(request, username=username, password=password)
			auth.login(request, user)	
			return redirect(request.GET.get('from',reverse('home')))
	else:
		register = RegisterFrom()
			
	content = {}
	content['register'] = register
	return render(request,'user/register.html',content)

def logout(request):
	auth.logout(request)
	return redirect(request.GET.get('from',reverse('home')))

def user_info(request):
	context={}
	return render(request,'user/user_info.html',context)

def change_nick_name(request):

	redirect_to = request.GET.get('from',reverse('home'))

	if request.method== 'POST' :
		form = ChangeNickNameFrom(request.POST,user=request.user)
		if form.is_valid():
			nick_name = form.cleaned_data['nickname_new']
			user_more_info,create = Profile.objects.get_or_create(user=request.user)
			user_more_info.nickname=nick_name
			user_more_info.save()
			return redirect(redirect_to)

	else:
		form = ChangeNickNameFrom()

	context = {}
	context['form'] = form
	context['page_title']="修改昵称"
	context['form_title']="修改昵称"
	context['submit_text'] ='修改'
	context['return_back_url']=redirect_to
	return render (request,'form.html',context)

def bind_email(request):
	redirect_to = request.GET.get('from',reverse('home'))

	if request.method== 'POST' :
					form = BindEmailForm(request.POST,request=request)
					if form.is_valid():
						email = form.cleaned_data['email']
						request.user.email = email
						request.user.save()
						return redirect(redirect_to)

	else:
		form = BindEmailForm()

	context = {}
	context['form'] = form
	context['page_title']="绑定邮箱"
	context['form_title']="绑定邮箱"
	context['submit_text'] ='绑定'
	context['return_back_url']=redirect_to
	return render (request,'user/bind_email.html',context)

def send_verification_code(request):
	date = {}
	email = request.GET.get('email','')
	if email =='':
		username = request.GET.get('username','')
		if username =='':
	
			date['message'] = '用户名不能为空'
		if User.objects.filter(username=username).exists():
			if User.objects.get(username=username).email != '':
				email = User.objects.get(username=username).email
			else:
				date['message'] = '用户未绑定邮箱'
		else:
		
			date['message'] = '用户名不存在'
			
	send_for = request.GET.get('send_for','')

	if  email !='':
		#生产验证码
		now = int(time.time())
		send_code_time = request.GET.get('send_code_time',0)

		if now - send_code_time <30:
			date['status'] = 'ERROR'
		else:
			code = ''.join(random.sample(string.ascii_letters + string.digits,4))
			request.session[send_for] = code
			request.session['send_code_time'] = now
			send_mail(
				'验证码',
				'验证码是：%s' % code,
				'76032636@qq.com',
				[email],
				fail_silently='false',
				)
			date['status'] = 'SUCCESS'
	else:
		date['status'] = 'ERROR'
	return JsonResponse(date)


def change_password(request):
	redirect_to =reverse('home')

	if request.method == 'POST' :
		form = ChangePasswordForm(request.POST,user=request.user)
		if form.is_valid():
			password = form.cleaned_data['new_password']
			request.user.set_password(password)
			request.user.save()
			auth.logout(request)
			return redirect(reverse('home'))

	else:
		form = ChangePasswordForm()

	context={}
	context['form']=form
	context['page_title']="修改密码"
	context['form_title']="修改密码"
	context['submit_text'] ='修改'
	context['return_back_url']=redirect_to
	return render(request,'user/ChangePassword.html',context)

def forget_password(request):
	if request.method == 'POST' :
		form = ForgetPassword(request.POST,request=request)
		if form.is_valid():
			password = form.cleaned_data['new_password']
			username = form.cleaned_data['username']
			user = User.objects.get(username=username)
			user.set_password(password)
			user.save()
			auth.logout(request)
			return redirect(reverse('home'))

	else:
		form = ForgetPassword()

	context={}
	context['form']=form
	context['page_title']="忘记密码"
	context['form_title']="忘记密码"
	context['submit_text'] ='修改'
	context['return_back_url']=reverse('home')
	return render(request,'user/forgetpassword.html',context)