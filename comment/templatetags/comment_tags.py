from django import template
from ..models import Comment
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm


register = template.Library()

@register.simple_tag
def get_comment_num(obj):
	ct = ContentType.objects.get_for_model(obj)
	comment_num = Comment.objects.filter(content_type=ct,object_id=obj.pk).count()
	return  comment_num

@register.simple_tag
def get_comment_form(obj):
	ct = ContentType.objects.get_for_model(obj)
	form = CommentForm(initial={'content_type':ct.model,'object_id':obj.id,"reply_comment_id":0})
	return form

@register.simple_tag
def get_comment(obj):
	ct = ContentType.objects.get_for_model(obj)
	comment=Comment.objects.filter(content_type=ct,object_id=obj.id,parant=None)
	return comment.order_by('-comment_time')


