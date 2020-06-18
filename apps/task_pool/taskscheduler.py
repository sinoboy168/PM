import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from .models import *
import logging
from django_apscheduler.models import DjangoJobExecution
from django.forms.models import model_to_dict
sched = BackgroundScheduler()
sched.add_jobstore(DjangoJobStore(), "default")

logging.basicConfig()
#logging.getLogger('apscheduler').setLevel(logging.DEBUG)#调试模式，会显示更多的提示信息

DjangoJobExecution.objects.delete_old_job_executions(604_800)  # Delete job executions older than 7 days

total = InspectionTaskCycleSetting.objects.all().count()
if total:
    for row in  InspectionTaskCycleSetting.objects.all():
        #inspection_item = InspectionTaskCycleSetting.objects.first()  # 点检计划表
        list_id = row.id  #
        cycle = row.cycle  # 循环周期
        update_time = row.add_time#任务设定创建/更新时间



        # @sched.scheduled_job("interval", seconds=5, id='test_job')
        # 增加点检任务单
        def add_inspection_list(**args):
            format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 系统当前时间
            inspection_list = InspectionTaskList()  # 点检任务表
            inspection_list.create_time = format_time # 创建时间
            inspection_list.creator = 'system'
            inspection_list.point = args.get('point')
            inspection_list.area_id= args.get('area')
            inspection_list.machine_id = args.get('machine')
            inspection_list.operator1_id = args.get('operator1')   # 操作人员1
            inspection_list.operator2_id = args.get('operator2')   # 操作人员2
            inspection_list.desc = args.get('desc')  # 任务描述
            inspection_list.cycle = args.get('cycle')  # 点检生成周期
            inspection_list.save()
            print(format_time)


        sched.add_job(add_inspection_list, 'interval', seconds=600 * cycle, misfire_grace_time=600, kwargs=model_to_dict(row), id=str(update_time) + str(list_id))
        # sched.add_job(add_inspection_list, 'date', run_date=datetime(2020, 4, 20, 17, 00, 0), id='add_inspection_list')
        # 监控任务
register_events(sched)

try:
    sched.start()  # 调度器开始
except Exception as e:
    print(e)
    # 报错则调度器停止执行
    sched.shutdown()
# print(sched.get_jobs())
# sched.remove_job('test_job2')

