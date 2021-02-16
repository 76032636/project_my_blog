from django.contrib import admin
from .models import Read_Number,ReadDetail

# Register your models here.
@admin.register(Read_Number)
class Read_NumberAdmin(admin.ModelAdmin):
	"""docstring for ClassName"""
	list_display=('read_number','content_object','id')

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
	"""docstring for ClassName"""
	list_display=('date','read_number','content_object','id')