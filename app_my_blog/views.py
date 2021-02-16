from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import Blog,BlogType
from read_statistics.utils import Read_Statistics_Once_Read
from django.contrib.contenttypes.models import ContentType



# Create your views here.
def get_blog_list_common_data(request,blogs_all_list):
	paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUM)
	page_num = request.GET.get('page',1)#GET获取字典，get获取具体键
	page_of_blogs = paginator.get_page(page_num)
	current_page_num = page_of_blogs.number
	page_range = list(range(max(current_page_num-2,1),current_page_num,))+list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
	#加上省略页
	if page_range[0] -1 >= 2:
		page_range.insert(0,'...')
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append('...')
	#加上首位页
	if page_range[0] !=1:
		page_range.insert(0,1)
	if page_range[-1] !=paginator.num_pages:
		page_range.append(paginator.num_pages)

	#获取获客分类对于的数量

	'''blog_types = BlogType.objects.all()
	blog_types_list=[]
	for blog_type in blog_types:
		blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
		blog_types_list.append(blog_type)'''
	#获取日期归档对于的博客数量

	blog_dates_dict = {}
	blog_dates=Blog.objects.dates('creat_time','month','DESC')
	for blog_date in blog_dates:
		blog_count = Blog.objects.filter(creat_time__year=blog_date.year,
			                creat_time__month=blog_date.month).count()
		blog_dates_dict[blog_date] = blog_count


	content = {}
	content['list'] = page_of_blogs
	content['blogs']= page_of_blogs.object_list
	content['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))#实例化，且增加了blog_count属性
	content['page_range'] = page_range
	content['blog_dates'] = blog_dates_dict
	return content


def blog_list(request):
	blog_all = Blog.objects.all()
	content = {}
	content=get_blog_list_common_data(request,blog_all)
	return render(request,'blog/blog_list.html',content)
	

def blog_detail(request,blog_id):
	content = {}
	blog = get_object_or_404(Blog,id=blog_id)
	#获取浏览器中的cookie中的blog字段

	'''if not request.COOKIES.get('blog_%s_read'%blog_id):
		ct = ContentType.objects.get_for_model(Blog)
		
		if Read_Number.objects.filter(content_type=ct,object_id=blog.id) :
			readnum=Read_Number.objects.get(content_type=ct,object_id=blog.id)
		else:
			readnum = Read_Number(content_type =ct,object_id = blog.id)
		readnum.read_number += 1
		readnum.save()
	'''

	
	
	read_cookie_key = Read_Statistics_Once_Read(request,blog)
	previous_blog = Blog.objects.filter(creat_time__gt=blog.creat_time).last()
	next_blog = Blog.objects.filter(creat_time__lt=blog.creat_time).first()

	ct = ContentType.objects.get_for_model(blog)
	

	
	content['detail'] = get_object_or_404(Blog,id=blog_id)
	content['previous_blog']=previous_blog
	content['next_blog']=next_blog
	response=render(request,'blog/blog_detail.html',content)
	#返回cookie告诉某一篇博客已经看过
	response.set_cookie(read_cookie_key,'true',max_age=3600,)
	return response

def blog_with_type(request,blog_type_id):
	blog_type = get_object_or_404(BlogType,id=blog_type_id)
	blog_all = Blog.objects.filter(blog_type=blog_type)
	content = {}
	content = get_blog_list_common_data(request,blog_all)
	
	content['types']=blog_type
	return render(request,'blog/blog_with_type.html',content)

def blog_with_data(request,year,month):
	blog_all = Blog.objects.filter(creat_time__year=year,creat_time__month=month)
	content = {}
	content = get_blog_list_common_data(request,blog_all)
	content['blogs_with_date']='%s年%s月' %(year,month) 
	return render(request,'blog/blog_with_date.html',content)
	
