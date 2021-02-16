from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from . models import LikeCount,LikeUserBlog
from django.db.models import ObjectDoesNotExist

# Create your views here.
def SuccessResponse(like_counts):
	data={}
	data['status'] = 'SUCCESS'
	data['is_like'] = 'True'
	data['like_counts']= like_counts
	return JsonResponse(data)

def ErrorResponse(code,message):
	data = {}
	data['status'] ='Error'
	data['code'] = code
	data['message']= message
	return JsonResponse(data)

	
def like_change(request):
	user = request.user
	if not user.is_authenticated:
		message = '你还未登录'
		return ErrorResponse(400,message)

	content_type = request.GET.get('content_type')
	object_id = int(request.GET.get('object_id'))

	try:
		content_type = ContentType.objects.get(model = content_type)
		model_class = content_type.model_class()
		model_obj = model_class.objects.get(pk = object_id)
	except ObjectDoesNotExist :
		message:'点赞对象不存在'
		return ErrorResponse(401,message)

	if request.GET.get('is_like') == "true" : #前台传过来的数据是这个用户没有对这篇文章点赞过，所以要点赞
		like_record, created = LikeUserBlog.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
		print('是否有点在记录是')
		print(created)
		if created == True:#发现后台记录确实没有这个用户对这篇文章的点赞记录#于是保存点在记录
			like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id) #同时获取或创建点赞数量
			like_count.like_counts +=1
			like_count.save()
			return SuccessResponse(like_count.like_counts)
		else:
			message = '已经点赞过！'
			return ErrorResponse(402,message)
	else: #前台过来的数据是要取消点在
		if LikeUserBlog.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():#判断一下如果确实有点赞记录
			like_record = LikeUserBlog.objects.get(content_type=content_type,object_id=object_id,user=user)#获取这条点赞记录
			like_record.delete()
			like_count, created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id) #同时对博客的点赞数量做操作
			if created == True:
				message ='没有点赞记录，不可取消点赞'
				return ErrorResponse(403,message)
			else:
				like_count.like_counts -=1
				like_count.save()
				return SuccessResponse(like_count.like_counts)
		else:#发现实际上没有点在记录，不可以再次取消点赞
			message ='没有点赞记录，不可取消点赞'
			return ErrorResponse(403,message)



	
	

