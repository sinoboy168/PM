from django import template
from ..models import *

register = template.Library()

# 转义
@register.filter
def Change_Str(str_value):
    return str(str_value)


# 获取最新记录
