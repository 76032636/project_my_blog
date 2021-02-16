from django import template
from ..models import LikeCount,LikeUserBlog
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def get_like_num(obj):
	ct = ContentType.objects.get_for_model(obj)
	like_counts,create = LikeCount.objects.get_or_create(content_type=ct, object_id=obj.pk)
	return like_counts.like_counts


@register.simple_tag(takes_context=True)
def is_liked(context,obj):
	ct = ContentType.objects.get_for_model(obj)
	user = context['user']
	if not user.is_authenticated:
		return ''
	else:
		if LikeUserBlog.objects.filter(content_type=ct,object_id=obj.pk,user=user).exists():
			return "active"
		else:
			return ''


@register.simple_tag
def get_model_str(obj):
	ct = ContentType.objects.get_for_model(obj)
	return ct.model


