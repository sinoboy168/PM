######################################
# Django 模块
######################################
from django.forms import Form
from django import forms
from django.forms import fields
import django.utils.timezone as timezone

######################################
# 自定义模块
######################################
from .models import *


######################################
# 添加主机表单
######################################
class AddHostInfoForm(Form):
    in_ip = forms.GenericIPAddressField(required=True)
    hostname = forms.CharField(min_length=2, max_length=20, required=True)
    cpu = forms.CharField(min_length=1, max_length=50, required=True)
    disk = forms.IntegerField(required=True)
    memory = forms.IntegerField(required=True)
    network = forms.IntegerField(required=True)
    ssh_port = forms.IntegerField(required=True)
    admin_user = forms.CharField(min_length=2, max_length=20, required=True)
    admin_pass = forms.CharField(min_length=6, max_length=50, required=True)
    normal_user = forms.CharField(min_length=2, max_length=20, required=False)
    normal_pass = forms.CharField(min_length=2, max_length=50, required=False)


# 区域新增表单#
class AreaForm(forms.Form):
    # add_time = forms.DateTimeField('入库时间', default=timezone.now)
    # update_user = forms.CharField(widget=forms.widgets.Select(choices=((1, '上海'), (2, '北京')), attrs={'class': "form-control"}))
    status = forms.ChoiceField(widget=forms.Select(choices=((1, '正常'), (0, '停用'))))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    desc = forms.CharField(required=True, max_length=200)


# 设备移入表单#

class MachineMoveInForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control"}))
    area = forms.ChoiceField(choices=Area.objects.all().values_list('id', 'name'), required=True)
    supplier = forms.CharField(max_length=20, required=True,
                               widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': u'供应商'}))
    type = forms.CharField(max_length=20, required=True,
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': u'供应商'}))
    manufacturing_date = forms.DateField(required=True, error_messages={'required': u'供应商不能为空', 'invalid': u'格式错误'})
    ID_fixed_assets = forms.CharField(max_length=20)#固定资产编号不是必填项
    # update_time = forms.DateTimeField()
    # add_user = forms.ModelChoiceField(queryset=UserProfile.objects.all().values_list('id', 'name'), related_name='area_add_user', verbose_name='添加人')
    status = forms.ChoiceField(required=True, widget=forms.widgets.Select(choices=((1, '正常'), (0, '停用'), (2, '迁出'), (3, '报废'))))
    operater = forms.CharField(required=True, max_length=20)
    desc = forms.CharField(required=True, max_length=200)


######################################
# 修改主机表单
######################################
class EditHostInfoForm(forms.Form):
    in_ip = forms.GenericIPAddressField(required=True)
    hostname = forms.CharField(min_length=2, max_length=20, required=True)
    cpu = forms.CharField(min_length=1, max_length=50, required=True)
    disk = forms.IntegerField(required=True)
    memory = forms.IntegerField(required=True)
    network = forms.IntegerField(required=True)
    ssh_port = forms.IntegerField(required=True)
    admin_user = forms.CharField(min_length=2, max_length=20, required=True)
    admin_pass = forms.CharField(min_length=6, max_length=50, required=True)
    normal_user = forms.CharField(min_length=2, max_length=20, required=False)
    normal_pass = forms.CharField(min_length=2, max_length=50, required=False)


######################################
# 添加服务表单
######################################
class AddHostServiceForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    version = forms.CharField(max_length=20, required=True)
    listen_user = forms.CharField(max_length=20, required=True)
    listen_port = forms.CharField(max_length=30, required=True)
    ins_path = forms.CharField(max_length=100, required=True)
    log_path = forms.CharField(max_length=100, required=True)
    backup_path = forms.CharField(max_length=100, required=False)
    start_cmd = forms.CharField(max_length=100, required=True)
    desc = forms.CharField(max_length=200, required=False)


######################################
# 编辑服务表单
######################################
class EditHostServiceForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    version = forms.CharField(max_length=20, required=True)
    listen_user = forms.CharField(max_length=20, required=True)
    listen_port = forms.CharField(max_length=30, required=True)
    ins_path = forms.CharField(max_length=100, required=True)
    log_path = forms.CharField(max_length=100, required=True)
    backup_path = forms.CharField(max_length=100, required=False)
    start_cmd = forms.CharField(max_length=100, required=True)
    desc = forms.CharField(max_length=200, required=False)


######################################
# 添加系统表单
######################################
class AddOsForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    version = forms.CharField(max_length=20, required=True)


######################################
# 编辑系统表单
######################################
class EditOsForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    version = forms.CharField(max_length=20, required=True)


######################################
# 添加机房
######################################
class AddIdcForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    address = forms.CharField(max_length=100, required=True)


######################################
# 编辑机房
######################################
class EditIdcForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    address = forms.CharField(max_length=100, required=True)


######################################
# 添加项目
######################################
class AddProjectForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    pro_user = forms.CharField(max_length=20, required=True)
    run_env = forms.CharField(max_length=20, required=True)


######################################
# 编辑项目
######################################
class EditProjectForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    pro_user = forms.CharField(max_length=20, required=True)
    run_env = forms.CharField(max_length=20, required=True)


######################################
# 添加环境
######################################
class AddOpEnvForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)


######################################
# 编辑环境
######################################
class EditOpEnvForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)


######################################
# 添加用途
######################################
class AddUseForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)


######################################
# 编辑用途
######################################
class EditUseForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)


######################################
# 添加数据库信息
######################################
class AddDatabaseInfoForm(forms.Form):
    db_name = forms.CharField(min_length=2, max_length=20, required=True)
    db_version = forms.CharField(max_length=20, required=True)
    db_admin_user = forms.CharField(min_length=2, max_length=20, required=True)
    db_admin_pass = forms.CharField(min_length=2, max_length=50, required=True)


######################################
# 修改数据库信息
######################################
class EditDatabaseInfoForm(forms.Form):
    db_name = forms.CharField(min_length=2, max_length=20, required=True)
    db_version = forms.CharField(max_length=20, required=True)
    db_admin_user = forms.CharField(min_length=2, max_length=20, required=True)
    db_admin_pass = forms.CharField(min_length=2, max_length=50, required=True)


######################################
# 添加数据库库
######################################
class AddDatabaseDBForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    use = forms.CharField(max_length=20, required=True)


######################################
# 编辑数据库库
######################################
class EditDatabaseDBForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20, required=True)
    use = forms.CharField(max_length=20, required=True)


######################################
# 添加数据库用户
######################################
class AddDatabaseUserForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=20, required=True)
    password = forms.CharField(min_length=2, max_length=50, required=True)
    grant_login = forms.CharField(max_length=50, required=True)


######################################
# 编辑数据库用户
######################################
class EditDatabaseUserForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=20, required=True)
    password = forms.CharField(min_length=2, max_length=50, required=True)
    grant_login = forms.CharField(max_length=50, required=True)


######################################
# 添加设备表单
######################################
class AddNetDviceForm(forms.Form):
    category = forms.CharField(max_length=20, required=True)
    name = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=50, required=True)
    ip_in = forms.GenericIPAddressField(required=True)
    ip_out = forms.GenericIPAddressField(required=False)
    admin_user = forms.CharField(max_length=20, required=True)
    admin_pass = forms.CharField(max_length=50, required=True)


######################################
# 修改设备表单
######################################
class EditNetDviceForm(forms.Form):
    category = forms.CharField(max_length=20, required=True)
    name = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=50, required=True)
    ip_in = forms.GenericIPAddressField(required=True)
    ip_out = forms.GenericIPAddressField(required=False)
    admin_user = forms.CharField(max_length=20, required=True)
    admin_pass = forms.CharField(max_length=50, required=True)


######################################
# 添加映射
######################################
class AddPortToPortForm(forms.Form):
    ip_out = forms.GenericIPAddressField(required=False)
    port_out = forms.IntegerField(required=True)
    ip_in = forms.GenericIPAddressField(required=True)
    port_in = forms.IntegerField(required=True)
    use = forms.CharField(max_length=20, required=True)
    desc = forms.CharField(max_length=200, required=False)


######################################
# 编辑映射
######################################
class EditPortToPortForm(forms.Form):
    ip_out = forms.GenericIPAddressField(required=False)
    port_out = forms.IntegerField(required=True)
    ip_in = forms.GenericIPAddressField(required=True)
    port_in = forms.IntegerField(required=True)
    use = forms.CharField(max_length=20, required=True)
    desc = forms.CharField(max_length=200, required=False)


######################################
# 添加域名
######################################
class AddDomainNameForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)


######################################
# 修改域名
######################################
class EditDomainNameForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)


######################################
# 添加域名解析
######################################
class AddDomainNameResolveForm(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    ip = forms.GenericIPAddressField(required=True)


######################################
# 修改域名解析
######################################
class EditDomainNameResolveForm(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    ip = forms.GenericIPAddressField(required=True)
