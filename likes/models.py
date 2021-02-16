from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class LikeCount(models.Model):
	"""docstring for ClassName"""
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	like_counts = models.IntegerField(default = 0)

class LikeUserBlog(models.Model):
	"""docstring for like_user_blog"""
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	liked_data = models.DateTimeField(auto_now_add = True)