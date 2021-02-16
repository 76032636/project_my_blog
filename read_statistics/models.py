from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


# Create your models here.
class Read_Number(models.Model):
	"""docstring for read_number"""
	read_number = models.IntegerField(default=0)
	
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpand():
	def read_num(self):
		try:
			ct = ContentType.objects.get_for_model(self)
			readnum = Read_Number.objects.get(content_type=ct,object_id=self.pk)
			return readnum.read_number
		except exceptions.ObjectDoesNotExist:
			return 0

class ReadDetail(models.Model):
	"""docstring for ReadDetail"""
	date = models.DateField(default=timezone.now)
	read_number = models.IntegerField(default=0)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')


