from django.shortcuts import render, redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse
from app_my_blog.models import Blog
from django.contrib.auth.models import User

# Create your views here.
def submit_comment (request):
	referer = request.META.get('HTTP_REFERER',reverse('home'))
	comment_form = CommentForm(request.POST,user = request.user)
	if comment_form.is_valid():
		comment = Comment()
		comment.text=comment_form.cleaned_data['comment']
		comment.user = comment_form.cleaned_data['user']
		comment.content_object=comment_form.cleaned_data['content_object']
		print('执行了')
		print(comment_form.cleaned_data['parant'])
		parant = comment_form.cleaned_data['parant']
		if not parant == None:
			comment.parant = parant
			comment.root =  parant.root if not parant.root is None else parant
			comment.reply_to = parant.user
		comment.save()
		comment.send_email()
			#判断回复的是博客还是评论，如果是回复博客的，则发一份邮件给作者，如果是回复回复的，则发一份邮件给用户
		#通过comment是否有parant来判断回复给谁
		

		data = {}
		data['status'] = 'SUCCESS'
		data['username'] = comment.user.get_nickname_or_username()
		data['comment'] = comment.text
		data['create_data']=comment.comment_time.timestamp()
		data['content_types']=ContentType.objects.get_for_model(comment).model
		if not parant == None:
			data['reply_to_comment'] = comment.reply_to.get_nickname_or_username()
		else:
			data['reply_to_comment'] = ''
		data['pk'] = comment.pk
		data['root_pk'] =comment.root.pk if not comment.root is None else ''	
	else:
		data = {}
		data['status'] = 'Error'
		data['message'] = list(comment_form.errors.values())[0][0]
	
	return JsonResponse(data)

