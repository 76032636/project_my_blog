from django.urls import path
from . import views

urlpatterns = [
	path('logout/',views.logout,name='logout'),
    path('login/',views.login,name='login'),
    path('loginModel/',views.loginModel,name='loginModel'),
    path('register/',views.register,name='register'),
    path('user_info/',views.user_info,name='user_info'),
    path('change_nick_name',views.change_nick_name,name='change_nick_name'),
    path('bind_email',views.bind_email,name='bind_email'),
    path('send_verification_code',views.send_verification_code,name='send_verification_code'),
    path('change_password',views.change_password,name='change_password'),
    path('forget_password',views.forget_password,name='forget_password'),

]