from django.db import models
from users.models import UserProfile
from asset_management.models import Machine, Area
from asset_management.models import DomainNameResolveInfo, ProjectInfo


##################################
#巡检任务周期设定表
##################################
class InspectionTaskCycleSetting(models.Model):
    area = models.ForeignKey(Area, related_name='inspection_machine_area_name', verbose_name="设备所在区域",on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, related_name='inspection_machine_name', verbose_name='巡检设备',
                                on_delete=models.CASCADE)
    operator1 = models.ForeignKey(UserProfile,related_name='inspection_operator1',verbose_name='负责人1',on_delete=models.CASCADE)
    operator2 = models.ForeignKey(UserProfile, related_name='inspection_operator2', verbose_name='负责人2',on_delete=models.CASCADE, null=True)
    point = models.CharField(max_length=20,verbose_name='检查点', null=True)
    start_time = models.DateTimeField(verbose_name='起始时间', null=True)
    add_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)
    desc = models.CharField(verbose_name='检查内容描述', max_length=200, blank=True, null=True)
    cycle = models.SmallIntegerField(verbose_name="任务生成周期", null=True)
    class Meta:
        verbose_name = '巡检任务周期设定表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.point

######################################
#巡检任务列表
######################################
class InspectionTaskList(models.Model):
    area = models.ForeignKey(Area, related_name='inspection_machine_area_list_name', verbose_name="设备所在区域",on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, related_name='inspection_machine_name_list', verbose_name='巡检设备',
                                on_delete=models.CASCADE)
    creator = models.CharField(max_length=20,verbose_name='创建人', null=True)
    operator1 = models.ForeignKey(UserProfile,related_name='inspection_list_operator1',verbose_name='负责人1',on_delete=models.CASCADE, null=True)
    operator2 = models.ForeignKey(UserProfile, related_name='inspection_list_operator2', verbose_name='负责人2',on_delete=models.CASCADE, null=True)
    point = models.CharField(max_length=20,verbose_name='检查点', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', null=True,auto_now_add=True)
    cycle=models.SmallIntegerField(verbose_name="任务生成周期", null=True)
    desc = models.CharField(verbose_name='检查内容描述', max_length=200, blank=True, null=True)
    status = models.CharField(verbose_name='状态', max_length=8, choices=(('done', '已处理'), ('pending', '未处理'), ('other','其他')), default='pending')
    result =models.CharField(verbose_name='检查结果', max_length=50, null=True)
    class Meta:
        verbose_name = '巡检任务表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.point


##################################
#保养任务周期设定表
##################################
class MaintenanceTaskCycleSetting(models.Model):
    area = models.ForeignKey(Area, related_name='maintenance_machine_area_name', verbose_name="设备所在区域",on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, related_name='maintenance_machine_name', verbose_name='巡检设备',
                                on_delete=models.CASCADE)
    operator1 = models.ForeignKey(UserProfile,related_name='maintenance_operator1',verbose_name='负责人1',on_delete=models.CASCADE)
    operator2 = models.ForeignKey(UserProfile, related_name='maintenance_operator2', verbose_name='负责人2',on_delete=models.CASCADE, null=True)
    point = models.CharField(max_length=20,verbose_name='检查点', null=True)
    start_time = models.DateTimeField(verbose_name='起始时间', null=True)
    add_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)
    desc = models.CharField(verbose_name='检查内容描述', max_length=200, blank=True, null=True)
    cycle = models.SmallIntegerField(verbose_name="任务生成周期", null=True)
    class Meta:
        verbose_name = '巡检任务周期设定表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.point

######################################
#保养任务列表
######################################
class MaintenanceTaskList(models.Model):
    area = models.ForeignKey(Area, related_name='maintenance_machine_area_list_name', verbose_name="设备所在区域",on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, related_name='maintenance_machine_name_list', verbose_name='巡检设备',
                                on_delete=models.CASCADE)
    creator = models.CharField(max_length=20,verbose_name='创建人', null=True)
    operator1 = models.ForeignKey(UserProfile,related_name='maintenance_list_operator1',verbose_name='负责人1',on_delete=models.CASCADE, null=True)
    operator2 = models.ForeignKey(UserProfile, related_name='maintenance_list_operator2', verbose_name='负责人2',on_delete=models.CASCADE, null=True)
    point = models.CharField(max_length=20,verbose_name='检查点', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', null=True,auto_now_add=True)
    cycle=models.SmallIntegerField(verbose_name="任务生成周期", null=True)
    desc = models.CharField(verbose_name='检查内容描述', max_length=200, blank=True, null=True)
    status = models.CharField(verbose_name='状态', max_length=8, choices=(('done', '已处理'), ('pending', '未处理'), ('other','其他')), default='pending')
    result =models.CharField(verbose_name='检查结果', max_length=50, null=True)
    class Meta:
        verbose_name = '巡检任务表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.point


######################################
# 故障标签表
######################################
class TroubleTag(models.Model):
    name = models.CharField(verbose_name='分类名称', max_length=20)

    class Meta:
        verbose_name = '故障标签表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
######################################
# 故障表
######################################
class TroubleRecord(models.Model):
    name = models.CharField(verbose_name='平台名称', max_length=20)
    url = models.ForeignKey(DomainNameResolveInfo, verbose_name='域名', related_name='tr_url1', blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectInfo, verbose_name='项目', related_name='tr_project1', on_delete=models.CASCADE)
    event = models.CharField(verbose_name='事件和原因', max_length=50)
    tags = models.ManyToManyField(TroubleTag, verbose_name='标签')
    event_time = models.DateTimeField(verbose_name='故障时间')
    handle_user = models.ManyToManyField(UserProfile, related_name='Trouble_user',verbose_name='处理人')
    handle_way = models.CharField(verbose_name='处理办法', max_length=100)
    handle_time = models.DateTimeField(verbose_name='处理时间')
    handle_result = models.PositiveSmallIntegerField(verbose_name='处理结果', choices=((1, '已处理'), (2, '未处理'), (3, '其它')), default=1)
    desc = models.CharField(verbose_name='备注', max_length=100, blank=True, null=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((0, '关闭'), (1, '开启')), default=1)

    class Meta:
        verbose_name = '故障表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.event

class DeployRecord(models.Model):
    name = models.CharField(verbose_name='平台名称', max_length=20)
    url = models.ForeignKey(DomainNameResolveInfo, verbose_name='域名', related_name='dep_url', blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectInfo, verbose_name='项目', related_name='dep_project', on_delete=models.CASCADE)
    deploy_time = models.DateTimeField(verbose_name='上线时间')
    request_user = models.CharField(verbose_name='发起人', max_length=20)
    deploy_user = models.ForeignKey(UserProfile, verbose_name='处理人', related_name='dep_user', on_delete=models.CASCADE)
    deploy_result = models.PositiveSmallIntegerField(verbose_name='上线结果', choices=((1, '成功'), (2, '失败')), default=1)
    desc = models.CharField(verbose_name='备注', max_length=100, blank=True, null=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((0, '关闭'), (1, '开启')), default=1)

    class Meta:
        verbose_name = '上线表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name