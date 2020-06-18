######################################
# Django 模块
######################################
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.views import View
from django.http import HttpResponse


######################################
# 第三方模块
######################################
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

######################################
# 系统模块
######################################
import json
import time


######################################
# 自建模块
######################################

from .forms import *
from .models import *
from operation_record.models import UserOperationRecord
from opms.settings import WEBSSH_IP, WEBSSH_PORT


##############################################################################
# 主机资产模块

######################################
# 设备入库
######################################

class MachineMoveInView(View):
    def get(self, request):
        if request.user.role > 1:
            # 左侧菜单页面选择
            web_chose_left_1 = 'asset_management'#一级菜单点亮
            web_chose_left_2 = 'machine_move_in'#二级菜单点亮
            web_chose_middle = ''
            # 用户
            users = UserProfile.objects.filter(status=1)
            #设备区域
            areas = Area.objects.all()
            context = {
                'web_chose_left_1': web_chose_left_1,
                'web_chose_left_2': web_chose_left_2,
                'web_chose_middle': web_chose_middle,
                'areas':areas,
                'users': users,
            }

            return render(request, 'host_management/host/machine_move_in.html', context=context)
        else:
            return HttpResponse(status=403)

    def post(self, request):
        if request.user.role > 1:
                obj= Machine()#定义数据库类
               # obj=request_form.cleaned_data#数据库类赋值
                obj.add_user = request.user#添加人为当前用户
                obj.add_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #添加时间为当前时间
                obj.name=request.POST.get('name')
                obj.area_id = request.POST.get('area')
                obj.status = request.POST.get('status')
                obj.supplier = request.POST.get('supplier')
                obj.type = request.POST.get('type')
                obj.manufacturing_date = request.POST.get('manufacturing_date')
                obj.ID_fixed_assets = request.POST.get('ID_fixed_assets')
                obj.operator_id = request.POST.get('operator')
                obj.desc = request.POST.get('desc')


                obj.save()

                #import task_pool.taskscheduler 启动条件测试

                #models.Machine.objects.create(**obj)#增加数据库记录
                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = obj.id
                op_record.operation = 1
                op_record.action = "添加设备[ %s ]" % (request.POST.get('name'))
                op_record.save()
                return redirect('/asset/management/machine/list')


######################################
# 增加设备区域
######################################
class AddAreaView(View):

    def post(self, request):
        if request.user.role > 1:
            request_form = AreaForm(request.POST)
            obj = Area()  # 定义数据库类
            obj.name = request.POST.get('name')
            obj.status = request.POST.get('area_status')
            obj.add_user = request.user  # 添加人为当前用户
            obj.add_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 添加时间为当前时间
            obj.save()
            # 添加操作记录
            op_record = UserOperationRecord()
            op_record.op_user = request.user
            op_record.belong = 1
            op_record.status = 1
            op_record.op_num = obj.id
            op_record.operation = 1
            op_record.action = "添加设备区域[ %s ]" % (request.POST.get('name'))
            op_record.save()
            return redirect('/asset/management/machine/move/in')
######################################
# 设备列表
######################################
class MachineListView(View):
    def get(self, request):
        if request.user.role > 1:
            # 页面选择
            web_chose_left_1 = 'asset_management'
            web_chose_left_2 = 'machine_list'
            web_chose_middle = ''
            # 用户
            users = UserProfile.objects.filter(status=1)
            areas = Area.objects.all()
            # 获取主机记录
            machine_records = Machine.objects.all().order_by('-update_time')
            # 筛选条件
            area_id = int(request.GET.get('area_id', '0'))
            print(area_id)
            if area_id != 0:
                machine_records = machine_records.filter(area_id=area_id)
            # 关键字
            keyword = request.GET.get('keyword', '')
            if keyword != '':
                machine_records = machine_records.filter(Q(ID_fixed_assets__icontains=keyword) |Q(
                    operator__chinese_name__icontains=keyword)| Q(name__icontains=keyword) | Q(
                    area__name__icontains=keyword) | Q(type__icontains=keyword) | Q(desc__icontains=keyword))

            # 记录数量
            record_nums = machine_records.count()

            # 判断页码
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            # 对取到的数据进行分页，记得定义每页的数量
            p = Paginator(machine_records, 6, request=request)

            # 分页处理后的 QuerySet
            machine_records = p.page(page)

            context = {
                'web_chose_left_1': web_chose_left_1,
                'web_chose_left_2': web_chose_left_2,
                'web_chose_middle': web_chose_middle,
                'areas': areas,
                'users': users,
                'area_id':area_id,
                'keyword': keyword,
                'machine_records': machine_records,
                'record_nums': record_nums,
                'WEBSSH_IP': WEBSSH_IP,
                'WEBSSH_PORT': WEBSSH_PORT,
            }
            return render(request, 'host_management/host/host_list.html', context=context)
        else:
            return HttpResponse(status=403)



