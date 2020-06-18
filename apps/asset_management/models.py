######################################
# Django 模块
######################################
from django.db import models
from django.db.models import Q

######################################
# 系统模块
######################################
import datetime

######################################
# 自定义模块
######################################
from users.models import UserProfile






######################################
# 区域表
######################################
class Area(models.Model):
    name = models.CharField(verbose_name='区域名称', max_length=30)
    add_user = models.ForeignKey(UserProfile, related_name='area_add_user', verbose_name='添加人',
                                 on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='入库时间', auto_now_add=True)
    update_user = models.ForeignKey(UserProfile, related_name='area_update_user',null=True, verbose_name='修改人',
                                    on_delete=models.CASCADE)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True,)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用')))
    desc = models.CharField(verbose_name='描述', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '区域'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


######################################
# 设备表
######################################
class Machine(models.Model):
    name = models.CharField(verbose_name='区域名称', max_length=30)
    area = models.ForeignKey(Area, verbose_name='区域名称', related_name='area_machine', max_length=30,
                             on_delete=models.CASCADE)
    supplier = models.CharField(verbose_name='供应商', max_length=30)
    add_user = models.ForeignKey(UserProfile, related_name='machine_add_user', verbose_name='添加人',
                                 on_delete=models.CASCADE)
    type = models.CharField(verbose_name='型号', max_length=30)
    add_time = models.DateTimeField(verbose_name='入库时间', auto_now_add=True)
    manufacturing_date = models.DateTimeField(verbose_name='生产时间')
    update_user = models.ForeignKey(UserProfile, related_name='machine_update_user', verbose_name='修改人',
                                    on_delete=models.CASCADE, null= True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True,null= True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用'), (2, '迁出'), (4, '报废')))
    ID_fixed_assets = models.CharField(verbose_name='固定资产编号', max_length=20)
    operator = models.ForeignKey(UserProfile, related_name='operator_user', verbose_name='操作人员',
                                 on_delete=models.CASCADE, null=True)
    desc = models.CharField(verbose_name='描述', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



