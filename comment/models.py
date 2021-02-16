import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string


class  SendMail(threading.Thread):
	"""docstring for  SendMail"""
	def __init__(self,subject,text,email,fail_silently='false'):
		self.subject=subject
		self.text=text
		self.email=email
		self.fail_silently=fail_silently
		threading.Thread.__init__(self)

	def run(self):

		send_mail(self.subject,
			'',
			'76032636@qq.com',
			[self.email],
			fail_silently=self.fail_silently,
			html_message=self.text
			)


class Comment(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	text = models.TextField()
	comment_time = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User,related_name="comment",on_delete=models.CASCADE)

	root = models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)
	parant = models.ForeignKey('self',related_name='parant_comment',null=True,on_delete=models.CASCADE)
	reply_to = models.ForeignKey(User,related_name="reply",null=True,on_delete=models.CASCADE)

	def send_email(self):
		if self.parant == None:
			email_title='有人对您的博客进行了评论'
			email=self.content_object.get_email()			
		else:
			email_title = '有人对您的回复进行了回复'
			email=self.get_email()	
		if email !='':
			content = {}
			content['comment_text']=self.text
			content['url'] = self.content_object.get_url()
			html_content = render_to_string('comment/email_template.html',content)
			send_mail=SendMail(email_title,html_content,email)
			send_mail.start()

	def get_email(self):
		return self.reply_to.email

	def __str__(self):
		return self.text
	

	class Meta:
		ordering = ['comment_time']

	


			
		