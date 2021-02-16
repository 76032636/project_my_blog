import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import Read_Number,ReadDetail



def Read_Statistics_Once_Read(request,obj):
	ct = ContentType.objects.get_for_model(obj)
	key = "%s_%s_read" %(ct.model,obj.pk)
	date=timezone.now().date()
	if not request.COOKIES.get(key):
		readnum,created = Read_Number.objects.get_or_create(content_type =ct,object_id = obj.id)
		readnum.read_number += 1
		readnum.save()

		readdetail , created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.id,date=date)
		readdetail.read_number += 1
		readdetail.save()
	return key

def Get_seven_days_read_date(content_type):
	today = timezone.now().date()
	read_nums_seven_day=[]
	dates = []
	for i in range(7,0,-1):
		date = today - datetime.timedelta(days=i)
		read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
		result = read_details.aggregate(read_number_for_that_day = Sum('read_number'))
		dates.append(date.strftime('%m/%d'))
		read_nums_seven_day.append(result['read_number_for_that_day'] or 0)
	return read_nums_seven_day,dates

def today_hot_blog(content_type):
	today = timezone.now().date()
	read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_number')
	return read_details[:5]

def yestoday_hot_blog(content_type):
	today = timezone.now().date()-datetime.timedelta(days=1)
	read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_number')
	print('这昨日天')
	print(read_details)
	return read_details[:5]

