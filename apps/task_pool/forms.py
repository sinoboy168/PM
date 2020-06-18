######################################
# Django 模块
######################################
from django import forms


######################################
# 自定义模块
######################################
from .models import *

######################################
# 添加巡检任务单
######################################
class AddInspectionListForm(forms.Form):
    area = forms.CharField(required=True)
    machine = forms.CharField( required=True)
    creator = forms.CharField(max_length=20)
    operator1 = forms.CharField(max_length=20, required=True)
    create_time = forms.DateTimeField()
    operator2 = forms.CharField(max_length=20, required=True)
    point = forms.CharField(max_length=20, required=True)
    create_time = forms.DateTimeField()
    cycle = forms.CharField(max_length=20)
    desc = forms.CharField(max_length=200, required=True)
    status = models.CharField()


######################################
# 添加保养任务单
######################################
class AddMaintenanceListForm(forms.Form):
    area = forms.CharField(required=True)
    machine = forms.CharField( required=True)
    creator = forms.CharField(max_length=20)
    operator1 = forms.CharField(max_length=20, required=True)
    create_time = forms.DateTimeField()
    operator2 = forms.CharField(max_length=20, required=True)
    point = forms.CharField(max_length=20, required=True)
    create_time = forms.DateTimeField()
    cycle = forms.CharField(max_length=20)
    desc = forms.CharField(max_length=200, required=True)
    status = models.CharField()





