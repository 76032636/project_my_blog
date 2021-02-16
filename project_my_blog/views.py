import datetime
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from app_my_blog.models import Blog
from read_statistics.utils import Get_seven_days_read_date,today_hot_blog,yestoday_hot_blog




def get_seven_day_hot_blog():
	today = timezone.now().date()
	seven_day = timezone.now().date()-datetime.timedelta(days=7)
	read_detail = Blog.objects.filter(readdetail__date__lt=today,readdetail__date__gte=seven_day)\
							  .values('id','title')\
							  .annotate(blog_read_num_sum=Sum('readdetail__read_number'))\
							  .order_by('-readdetail__read_number')
	
	return read_detail[:7]

def home(request):
	blog_content_type=ContentType.objects.get_for_model(Blog)
	content ={}
	read_nume,dates = Get_seven_days_read_date(blog_content_type)
	today_hot_data = today_hot_blog(blog_content_type)
	yestoday_hot_data = yestoday_hot_blog(blog_content_type)
	seven_days_hot_blog = get_seven_day_hot_blog()
	content['seven_days']=read_nume
	content['dates'] = dates
	content['today_hot_blog']=today_hot_data
	content['yestoday_hot_data']=yestoday_hot_data
	content['seven_days_hot_blog']=seven_days_hot_blog
	return render(request,'home.html',content)

