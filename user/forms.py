from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	"""docstring for ClassName"""
	username_or_email = forms.CharField(label='账户',
		widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名或邮箱'}))
	password_login = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))

	def clean(self):
		try:
			username_or_email = self.cleaned_data['username_or_email']
			password = self.cleaned_data['password_login']
			
		except Exception as e:
			raise forms.ValidationError('登录错误')	
		user = auth.authenticate(username=username_or_email, password=password)
		if user is None:
			if User.objects.filter(email=username_or_email).exists():
				print('邮箱存在')
				username=User.objects.get(email=username_or_email).username
				print('用户名是：')
				print(username)
				user = auth.authenticate(username=username, password=password)
				print(user)
				if not user is None:
					print('用户存在')
					self.cleaned_data['user'] = user
					return self.cleaned_data
			raise forms.ValidationError('用户名或密码不正确')	
		else:
			self.cleaned_data['user'] = user
		return self.cleaned_data

class RegisterFrom(forms.Form):
	"""docstring for ClassName"""
	username = forms.CharField(label='创建账户',
		max_length = 30,
		min_length = 3,
		widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
	password_register = forms.CharField(label='创建密码',
		min_length = 6,
		widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
	passwordagain = forms.CharField(label='再次输入密码',
		min_length = 6,
		widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再次输入密码'}))
	email = forms.EmailField(label='邮箱',
		widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))
	verification_code = forms.CharField(
		label='验证码',
		required=False,
		widget=forms.TextInput(attrs={'class':'form-control','placeholder':'点击"发送验证码"发送到邮箱'})
		)

	def __init__(self,*args,**kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(RegisterFrom,self).__init__(*args,**kwargs)

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('用户名已经存在')	
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('邮箱已经被使用')	
		return email

	def clean_passwordagain(self):
		password = self.cleaned_data['password_register']
		passwordagain = self.cleaned_data['passwordagain']
		if passwordagain != password:
			raise forms.ValidationError('两次输入密码不一致')
		return passwordagain

	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code','').strip()
		if verification_code == '' :
			raise forms.ValidationError('验证码不能为空')
		return verification_code

	def clean(self):
		code = self.request.session.get('register','')
		verification_code = self.cleaned_data.get('verification_code','') 
		if not (code != '' and code == verification_code) :
			raise forms.ValidationError('验证码不正确')

		return self.cleaned_data

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('邮箱已经存在')
		return email

class ChangeNickNameFrom(forms.Form):
	"""docstring for ChangeNickName"""
	nickname_new=forms.CharField(label='新昵称',
		max_length = 20,
		min_length = 3,
		widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入新的昵称'})
		)

	def clean_nickname_new(self):
		nickname_new=self.cleaned_data.get('nickname_new','').strip()
		if nickname_new == '':
			raise ValidationError('新的昵称不能为空')
		return nickname_new

	def __init__(self,*args,**kwargs):
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super(ChangeNickNameFrom,self).__init__(*args,**kwargs)
		

	def clean(self):
		if self.user.is_authenticated:
			self.cleaned_data['user'] =self.user
		else:
			raise forms.ValidationError('用户尚未登录')

		return self.cleaned_data
		
class BindEmailForm(forms.Form):
	"""docstring for Bind_Email"""
	email = forms.EmailField(
		label='邮箱',
		widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入正确的邮箱'})
		)
	verification_code = forms.CharField(
		label='验证码',
		required=False,
		widget=forms.TextInput(attrs={'class':'form-control','placeholder':'点击"发送验证码"发送到邮箱'})
		)

	def __init__(self,*args,**kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(BindEmailForm,self).__init__(*args,**kwargs)
		

	def clean(self):
		if self.request.user.is_authenticated:
			self.cleaned_data['user'] =self.request.user
		else:
			raise forms.ValidationError('用户尚未登录')

		if self.request.user.email !='':
			raise forms.ValidationError('已经绑定邮箱')

		code = self.request.session.get('bind_email','')
		verification_code = self.cleaned_data.get('verification_code','') 
		if not (code != '' and code == verification_code) :
			raise forms.ValidationError('验证码不正确')

		return self.cleaned_data
		
	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code','').strip()
		if verification_code == '' :
			raise forms.ValidationError('验证码不能为空')
		return verification_code


	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('邮箱已经存在')
		return email



class ChangePasswordForm(forms.Form):
	"""docstring for ClassName"""
	org_password = forms.CharField(label='原密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入原密码'}))
	new_password = forms.CharField(label='新密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'}))
	new_password_again = forms.CharField(label='再次输入新密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再次输入新密码'}))

	def __init__(self,*args,**kwargs):
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super(ChangePasswordForm,self).__init__(*args,**kwargs)

	def clean(self):
		if self.user.is_authenticated:
			self.cleaned_data['user'] =self.user
		else:
			raise forms.ValidationError('用户尚未登录')

		return self.cleaned_data
	#验证原密码是否正确
	def clean_old_password(self):
		old_password = self.cleaned_data.get('org_password','')
		if not self.user.check_password(old_password):
			raise ValidationError('原密码不正确')
		
		return old_password

	def clean_new_same_or_not(self):
		new_password = self.cleaned_data.get('new_password','')
		new_password_again = self.cleaned_data.get('new_password_again','')
		if new_password =='' or new_password != new_password_again:
			raise ValidationError('新密码设置错误')
		return self.cleaned_data


class ForgetPassword(forms.Form):
	"""docstring for ForgetPassword"""
	username = forms.CharField(
		label='用户名',
		widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入要找回密码的用户名'})
		)
	verification_code = forms.CharField(
		label='验证码',
		required=False,
		widget=forms.TextInput(attrs={'class':'form-control','placeholder':'点击"发送验证码"发送到邮箱'})
		)
	new_password = forms.CharField(label='新密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'}))
	new_password_again = forms.CharField(label='再次输入新密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再次输入新密码'}))


	def __init__(self,*args,**kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(ForgetPassword,self).__init__(*args,**kwargs)
		
	#检测用户名是否注册
	def clean_username(self):
		username = self.cleaned_data['username'].strip()
		if not User.objects.filter(username=username).exists():
			return ValidationError('用户名不存在')
		return username


	#验证是否为空及是否正确
	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code','').strip()
		if verification_code == '' :
			raise forms.ValidationError('验证码不能为空')
		code = self.request.session.get('forgetpassword','')
		verification_code = self.cleaned_data.get('verification_code','') 
		if not (code != '' and code == verification_code) :
			raise forms.ValidationError('验证码不正确')

		return verification_code

	#验证新旧密码是否一致
	def clean_passwordagain():
		new_password = self.cleaned_data['new_password']
		new_password_again = self.cleaned_data['new_password_again']
		if new_password != new_password_again:
			raise forms.ValidationError('两次输入密码不一致')
		return new_password