"""
Online management app
"""

from django.urls import path

from .views import *

app_name = 'task_pool'

urlpatterns = [


    # 巡检列表
    path('inspection/list', InspectionListView.as_view(), name='Inspection_list'),

    # 完成点检任务单
    path('inspection/done', DoneInspectionListView.as_view(), name='Done_inspection'),

    # 变更巡检责任人
    path('inspection/change_operator', ChangeOperatorView.as_view(), name='change_operator'),

    #巡检任务临时新增
    path('inspection/add', AddInspectionListView.as_view(), name='add_inspection'),



    # 添加任务设定
    path('setting/add', Add_Task_SettingView.as_view(), name='add_task_setting'),

    # 巡检任务设定新增EXCEL
    path('setting/add_excel', Add_By_ExcelView.as_view(), name='add_by_excel'),



    # 维保任务列表
    path('maintenance/list', MaintenanceListView.as_view(), name='Maintenance_list'),

    # 完成维保任务单
    path('maintenance/done', DoneMaintenanceListView.as_view(), name='Done_maintenance'),

    # 变更维保责任人
    path('maintenance/change_operator', ChangeMaintenanceOperatorView.as_view(), name='change_operator_maintenance'),

    #维保任务临时新增
    path('maintenance/add', AddMaintenanceListView.as_view(), name='add_maintenance'),




]


