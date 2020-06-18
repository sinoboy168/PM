
######################################
# Django 模块
######################################
from django.contrib import admin

######################################
# 自己写的模块
######################################
from .models import *



######################################
# 注册
######################################
admin.site.register(InspectionTaskCycleSetting)
admin.site.register(InspectionTaskList)