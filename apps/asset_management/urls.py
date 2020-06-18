"""
Host management app
"""
from django.urls import path
from .views import *

app_name = 'asset_management'

urlpatterns = [
    # 设备列表
    path('machine/list', MachineListView.as_view(), name='machine_list'),
    # 设备入库-添加
    path('machine/move/in', MachineMoveInView.as_view(), name='machine_move_in'),
    path('add/area', AddAreaView.as_view(), name='add_area'),
]

