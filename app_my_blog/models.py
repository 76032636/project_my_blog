from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpand,ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse




# Create your models here.
class BlogType(models.Model):
	type_name = models.CharField(max_length=15)

	def __str__(self):
		return self.type_name

class Blog(models.Model,ReadNumExpand):
	"""为博文定义表"""
	title = models.CharField(max_length=30)
	content = RichTextUploadingField()
	blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE)
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	readdetail=GenericRelation(ReadDetail)
	creat_time = models.DateTimeField(auto_now_add=True)
	last_updated_time = models.DateTimeField(auto_now=True)

	def get_url(self):
		return reverse('blog_detail',kwargs={'blog_id':self.pk})

	def get_email(self):
		return self.author.email 

	def __str__(self):
		return self.title

	class Meta:
		"""docstring for Meta"""
		ordering=['-creat_time']
