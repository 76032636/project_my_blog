from django.contrib import admin
from .models import BlogType , Blog

# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
	"""docstring for blogtype"""
	list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	"""方法或属性，所以如果是外键的内容，需要在model里面定义一个关联外键的方法"""
	list_display=('title','blog_type','author','creat_time','last_updated_time','id','read_num')

'''@admin.register(Read_Number)
class Read_Number(admin.ModelAdmin):
	"""docstring for ClassName"""
	list_display=('read_number','blog')
'''