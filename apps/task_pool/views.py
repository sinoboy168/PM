######################################
# Django 模块
######################################
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.core.cache import cache

######################################
# 第三方模块
######################################
from pure_pagination import PageNotAnInteger, Paginator

######################################
# 系统模块
######################################

import time
import json
import xlwt#EXCEL 写入文件
import xlrd#EXCEL 读取文件
from io import BytesIO

######################################
# 自建模块--定时生产任务
######################################
from .forms import *
from .models import *


#from .taskscheduler import *


#点检任务列表
######################################
class InspectionListView(View):

    def get(self, request):
        if request.user.role > 1:

            # 页面选择
            web_chose_left_1 = 'task_pool'
            web_chose_left_2 = 'inspection'

            web_title = "点检列表"

            users = UserProfile.objects.filter(status=1)  # 用户信息
            machines = Machine.objects.all()
            areas = Area.objects.all()
            records = InspectionTaskList.objects.all().order_by('-create_time')  # 点检任务清单

            # 搜索，导出条件筛选
            start_time = request.GET.get("start_time", "")
            stop_time = request.GET.get("stop_time", "")
            area_list = request.GET.getlist("area_check", "")
            machine_list = request.GET.getlist("machine_check", "")
            user_list = request.GET.getlist("user_check", "")
            status_list = request.GET.getlist("status_check", "")

            export_data = ""
            # 判断用户操作
            action = request.GET.get("action", "")
            if action == "export_all":
                export_data = records # 导出全部
            if action != "":
                if (action == "search") or (action == "export_search"):
                    if start_time != "":
                        records = records.filter(create_time__gte=start_time)

                    if stop_time != "":
                        records = records.filter(create_time__lte=stop_time)

                    if area_list != "":
                        records = records.filter(area__in=area_list).distinct()

                    if machine_list != "":
                        records = records.filter(machine__in=machine_list).distinct()

                    if user_list != "":

                        records = records.filter(Q(operator1__in=user_list) | Q(operator2__in=user_list)).distinct()

                    if status_list != "":
                        records = records.filter(status__in=status_list).distinct()

                    web_title = '点检任务单查询'

                    if action == "export_search":
                        export_data = records#条件导出

                if (action == "export_search") or (action == "export_all"):
                    # 创建 excel
                    new_excel = xlwt.Workbook(encoding='utf-8')
                    excel_page = new_excel.add_sheet(u'故障记录')

                    # 插入第一行标题
                    excel_page.write(0, 0, u'区域')
                    excel_page.write(0, 1, u'设备名称')
                    excel_page.write(0, 2, u'创建者')
                    excel_page.write(0, 3, u'创建时间')
                    excel_page.write(0, 4, u'负责人1')
                    excel_page.write(0, 5, u'负责人2')
                    excel_page.write(0, 6, u'点检位置')
                    excel_page.write(0, 7, u'作业标准')
                    excel_page.write(0, 8, u'检查结果')
                    excel_page.write(0, 9, u'任务状态')
                    excel_page.write(0, 10, u'作业周期')


                    # 初始行
                    excel_row = 1

                    if (export_data != '') and export_data:
                        for each in export_data:
                            name_excel = each.machine.name
                            area_excel = each.area.name
                            creator_excel = each.creator
                            create_time_excel = each.create_time
                            operator1_excel = each.operator1.chinese_name
                            operator2_excel = each.operator2.chinese_name
                            point_excel = each.point
                            cycle_excel = each.cycle
                            desc_excel = each.desc
                            result_excel = each.result
                            status_excel = ''

                            if each.status == 'done':
                                status_excel = '已处理'

                            if each.status == 'pending':
                                status_excel = '未处理'

                            if each.status == 'other':
                                status_excel = '其它'



                            # 定义时间格式
                            time_style = 'YYYY/MM/DD HH:mm'
                            style = xlwt.XFStyle()
                            style.num_format_str = time_style

                            # 写数据
                            excel_page.write(excel_row, 0, area_excel)
                            excel_page.write(excel_row, 1, name_excel)
                            excel_page.write(excel_row, 2, creator_excel)
                            excel_page.write(excel_row, 3, create_time_excel)
                            excel_page.write(excel_row, 4, operator1_excel)
                            excel_page.write(excel_row, 5, operator2_excel, style)
                            excel_page.write(excel_row, 6, point_excel)
                            excel_page.write(excel_row, 7, desc_excel, style)
                            excel_page.write(excel_row, 8, result_excel)
                            excel_page.write(excel_row, 9, status_excel)
                            excel_page.write(excel_row, 10, cycle_excel)

                            # 行数加1
                            excel_row += 1

                        # 导出文件
                        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
                        filename = '点检任务表_' + time_now + '.xls'
                        response = HttpResponse(content_type='application/vnd.ms-excel')
                        response['Content-Disposition'] = 'attachment;filename={}'.format(
                            filename.encode('utf-8').decode("ISO-8859-1"))
                        output = BytesIO()
                        new_excel.save(output)
                        output.seek(0)
                        response.write(output.getvalue())
                        return response

            # 搜索
            keyword = request.GET.get('keyword', '')
            if keyword != '':
                records = records.filter(
                    Q(machine__name__icontains=keyword) | Q(area__name__icontains=keyword) | Q(creator__icontains=keyword) | Q(
                        desc__icontains=keyword) | Q(operator1__chinese_name__icontains=keyword) |
                    Q(operator2__chinese_name__icontains=keyword)| Q(point__icontains=keyword))

            record_nums = records.count()

            # 判断页码
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            # 对取到的数据进行分页，记得定义每页的数量
            p = Paginator(records, 15, request=request)

            # 分页处理后的 QuerySet
            records = p.page(page)

            context = {
                'web_chose_left_1': web_chose_left_1,
                'web_chose_left_2': web_chose_left_2,
                'web_title': web_title,
                'users': users,
                'machines': machines,
                'areas': areas,
                'records': records,
                'keyword': keyword,
                'record_nums': record_nums,
                'start_time': start_time,
                'stop_time': stop_time,
                'area_list': area_list,
                'user_list': user_list,
                'machine_list': machine_list,
                'status_list': status_list,
            }

            return render(request, 'task_pool/inspection_list.html', context=context)
        else:
            return HttpResponse(status=403)
#####################################
######################################
# 完成点检记录
######################################

class DoneInspectionListView(View):
    def post(self, request):
        print(request.POST)
        if request.user.role > 1:
            try:
                inspection_obj = InspectionTaskList.objects.get(id=int(request.POST.get("record_id")))
                inspection_obj.status = 'done'
                inspection_obj.save()
                return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"failed", "msg":"未知错误！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)

######################################
# 变更点检任务单责任人
######################################

class ChangeOperatorView(View):
    def post(self, request):

        if request.user.role > 1:
            try:
                inspection_obj = InspectionTaskList.objects.get(id=int(request.POST.get("record_id")))
                inspection_obj.operator1_id=request.POST.get("operator1")
                inspection_obj.operator2_id = request.POST.get("operator2")
                inspection_obj.save()
                return HttpResponse('{"status":"success", "msg":"变更成功！"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"failed", "msg":"未知错误！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)

######################################
# 添加巡检任务单
######################################
class AddInspectionListView(View):
    def post(self, request):
        if request.user.role > 1:
            add_inspection_form = AddInspectionListForm(request.POST)

            if add_inspection_form.is_valid():
                pass
            obj = add_inspection_form.clean()
            # 获取数据
            added_list = InspectionTaskList()
            added_list.area_id = obj['area']
            added_list.machine_id = obj['machine']
            added_list.operator1_id = obj['operator1']
            added_list.operator2_id = obj['operator2']
            added_list.point = obj['point']
            added_list.desc = obj['desc']
            added_list.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #添加时间为当前时间
            added_list.status = 'pending'
            added_list.cycle =0  #表示临时增加

            added_list.save()
            return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')

        else:
            return HttpResponse(status=403)




######################################
#点检任务设定新增列表
######################################
class Add_Task_SettingView(View):

    def get(self, request):
        if request.user.role > 1:

            # 页面选择
            web_chose_left_1 = 'task_pool'
            web_chose_left_2 = 'add_task_setting'

            web_title = "新增定期任务"

            context = {
                'web_chose_left_1': web_chose_left_1,
                'web_chose_left_2': web_chose_left_2,
                'web_title': web_title,

            }

            return render(request, 'task_pool/add_task_setting.html', context=context)
        else:
            return HttpResponse(status=403)

    def post(self, request):
        if request.user.role > 1:
            f = request.FILES.get('file')
            file_type = f.name.split('.')[1]
            if file_type in ['xlsx', 'xls']:
                # 开始解析上传的excel表格
                wb = xlrd.open_workbook(filename=None, file_contents=f.read())
                table = wb.sheets()[0]
                nrows = table.nrows  # 行数
                settings = []
                for i in range(1, nrows):
                    rowValue = table.row_values(i)
                    settings.append(rowValue)

                cache.set('settings', settings, 60*30)#设置缓存30秒
                context = {
                    'web_chose_left_1': 'task_pool',
                    'web_chose_left_2': 'add_task_setting',
                    'web_title': "新增定期任务",
                    'settings': settings,
                    'settings_nums': len(settings)
                }
                return render(request, 'task_pool/add_task_setting.html', context=context)
            else:
                return HttpResponse('{ "msg":"请选择EXCEL文件！"}', content_type='application/json')
######################################
# 添加EXCEL设定表
######################################

class Add_By_ExcelView(View):
    def post(self, request):
        list_settings = cache.get('settings', None)
        if request.user.role > 1:
            try:
                for row in range(len(list_settings)):
                    obj=InspectionTaskCycleSetting()
                    obj.area_id = Area.objects.get(name=list_settings[row][0]).id  # 区域
                    obj.machine_id =Machine.objects.get(name= list_settings[row][1]).id # 设备
                    obj.operator1_id =UserProfile.objects.get(chinese_name=list_settings[row][2]).id# 负责人1
                    obj.operator2_id = UserProfile.objects.get(chinese_name=list_settings[row][3]).id# 负责人2
                    obj.point = list_settings[row][4]  # 巡检点
                    obj.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 开始时间
                    obj.add_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 创建时间
                    obj.desc = list_settings[row][5]  # 作业标准
                    obj.cycle = list_settings[row][6]  # 作业周期
                    obj.save()
                return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"failed", "msg":"请检查表格数据！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)




#点检任务列表
######################################
class MaintenanceListView(View):

    def get(self, request):
        if request.user.role > 1:

            # 页面选择
            web_chose_left_1 = 'task_pool'
            web_chose_left_2 = 'maintenance'

            web_title = "点检列表"

            users = UserProfile.objects.filter(status=1)  # 用户信息
            machines = Machine.objects.all()
            areas = Area.objects.all()
            records = MaintenanceTaskList.objects.all().order_by('-create_time')  # 点检任务清单

            # 搜索，导出条件筛选
            start_time = request.GET.get("start_time", "")
            stop_time = request.GET.get("stop_time", "")
            area_list = request.GET.getlist("area_check", "")
            machine_list = request.GET.getlist("machine_check", "")
            user_list = request.GET.getlist("user_check", "")
            status_list = request.GET.getlist("status_check", "")

            export_data = ""
            # 判断用户操作
            action = request.GET.get("action", "")
            if action == "export_all":
                export_data = records # 导出全部
            if action != "":
                if (action == "search") or (action == "export_search"):
                    if start_time != "":
                        records = records.filter(create_time__gte=start_time)

                    if stop_time != "":
                        records = records.filter(create_time__lte=stop_time)

                    if area_list != "":
                        records = records.filter(area__in=area_list).distinct()

                    if machine_list != "":
                        records = records.filter(machine__in=machine_list).distinct()

                    if user_list != "":

                        records = records.filter(Q(operator1__in=user_list) | Q(operator2__in=user_list)).distinct()

                    if status_list != "":
                        records = records.filter(status__in=status_list).distinct()

                    web_title = '点检任务单查询'

                    if action == "export_search":
                        export_data = records#条件导出

                if (action == "export_search") or (action == "export_all"):
                    # 创建 excel
                    new_excel = xlwt.Workbook(encoding='utf-8')
                    excel_page = new_excel.add_sheet(u'故障记录')

                    # 插入第一行标题
                    excel_page.write(0, 0, u'区域')
                    excel_page.write(0, 1, u'设备名称')
                    excel_page.write(0, 2, u'创建者')
                    excel_page.write(0, 3, u'创建时间')
                    excel_page.write(0, 4, u'负责人1')
                    excel_page.write(0, 5, u'负责人2')
                    excel_page.write(0, 6, u'点检位置')
                    excel_page.write(0, 7, u'作业标准')
                    excel_page.write(0, 8, u'保养结果')
                    excel_page.write(0, 9, u'任务状态')
                    excel_page.write(0,10, u'作业周期')


                    # 初始行
                    excel_row = 1

                    if (export_data != '') and export_data:
                        for each in export_data:
                            machine_excel = each.machine.name
                            area_excel = each.area.name
                            creator_excel = each.creator
                            create_time_excel = each.create_time
                            operator1_excel = each.operator1.chinese_name
                            operator2_excel = each.operator2.chinese_name
                            point_excel = each.point
                            desc_excel = each.desc
                            result_excel = each.result
                            cycle_excel = each.cycle

                            status_excel = ''

                            if each.status == 'done':
                                status_excel = '已处理'

                            if each.status == 'pending':
                                status_excel = '未处理'

                            if each.status == 'other':
                                status_excel = '其它'



                            # 定义时间格式
                            time_style = 'YYYY/MM/DD HH:mm'
                            style = xlwt.XFStyle()
                            style.num_format_str = time_style

                            # 写数据
                            excel_page.write(excel_row, 0, area_excel)
                            excel_page.write(excel_row, 1, machine_excel)
                            excel_page.write(excel_row, 2, creator_excel)
                            excel_page.write(excel_row, 3, create_time_excel)
                            excel_page.write(excel_row, 4, operator1_excel)
                            excel_page.write(excel_row, 5, operator2_excel, style)
                            excel_page.write(excel_row, 6, point_excel)
                            excel_page.write(excel_row, 7, desc_excel, style)
                            excel_page.write(excel_row, 8, result_excel)
                            excel_page.write(excel_row, 9, status_excel)
                            excel_page.write(excel_row, 10, cycle_excel)

                            # 行数加1
                            excel_row += 1

                        # 导出文件
                        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
                        filename = '保养任务表_' + time_now + '.xls'
                        response = HttpResponse(content_type='application/vnd.ms-excel')
                        response['Content-Disposition'] = 'attachment;filename={}'.format(
                            filename.encode('utf-8').decode("ISO-8859-1"))
                        output = BytesIO()
                        new_excel.save(output)
                        output.seek(0)
                        response.write(output.getvalue())
                        return response

            # 搜索
            keyword = request.GET.get('keyword', '')
            if keyword != '':
                records = records.filter(
                    Q(machine__name__icontains=keyword) | Q(area__name__icontains=keyword) | Q(creator__icontains=keyword) | Q(
                        desc__icontains=keyword) | Q(operator1__chinese_name__icontains=keyword) |
                    Q(operator2__chinese_name__icontains=keyword)| Q(point__icontains=keyword))

            record_nums = records.count()

            # 判断页码
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            # 对取到的数据进行分页，记得定义每页的数量
            p = Paginator(records, 15, request=request)

            # 分页处理后的 QuerySet
            records = p.page(page)

            context = {
                'web_chose_left_1': web_chose_left_1,
                'web_chose_left_2': web_chose_left_2,
                'web_title': web_title,
                'users': users,
                'machines': machines,
                'areas': areas,
                'records': records,
                'keyword': keyword,
                'record_nums': record_nums,
                'start_time': start_time,
                'stop_time': stop_time,
                'area_list': area_list,
                'user_list': user_list,
                'machine_list': machine_list,
                'status_list': status_list,
            }

            return render(request, 'task_pool/inspection_list.html', context=context)
        else:
            return HttpResponse(status=403)
#####################################
######################################
# 完成点检记录
######################################

class DoneMaintenanceListView(View):
    def post(self, request):
        print(request.POST)
        if request.user.role > 1:
            try:
                maintenance_obj = MaintenanceTaskList.objects.get(id=int(request.POST.get("record_id")))
                maintenance_obj.status = 'done'
                maintenance_obj.save()
                return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"failed", "msg":"未知错误！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)

######################################
# 变更保养任务单责任人
######################################

class ChangeMaintenanceOperatorView(View):
    def post(self, request):

        if request.user.role > 1:
            try:
                maintenance_obj = MaintenanceTaskList.objects.get(id=int(request.POST.get("record_id")))
                maintenance_obj.operator1_id=request.POST.get("operator1")
                maintenance_obj.operator2_id = request.POST.get("operator2")
                maintenance_obj.save()
                return HttpResponse('{"status":"success", "msg":"变更成功！"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"failed", "msg":"未知错误！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)

######################################
# 添加保养任务单
######################################
class AddMaintenanceListView(View):
    def post(self, request):
        if request.user.role > 1:
            add_maintenance_form = AddMaintenanceForm(request.POST)

            if add_maintenance_form.is_valid():
                pass
            obj = add_maintenance_form.clean()
            # 获取数据
            added_list = MaintenanceTaskList()
            added_list.area_id = obj['area']
            added_list.machine_id = obj['machine']
            added_list.operator1_id = obj['operator1']
            added_list.operator2_id = obj['operator2']
            added_list.point = obj['point']
            added_list.desc = obj['desc']
            added_list.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #添加时间为当前时间
            added_list.status = 'pending'
            added_list.cycle =0  #表示临时增加

            added_list.save()
            return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')

        else:
            return HttpResponse(status=403)





