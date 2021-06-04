from django.shortcuts import render, HttpResponse, redirect
from repository import models
from utils.run import Runner
from utils.building import Building
import json, os, datetime, time
from utils.pagination import Pagination
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import JsonResponse
from django.core import serializers
from backend.auth.auth import check_login, check_ajax_login
from utils.Send_email import sendEmail
import psutil
from django_apscheduler.models import DjangoJob,DjangoJobExecution


def task(request):
    project_list = models.Project.objects.all()
    project = request.GET.get('project')
    current_page = request.GET.get('p')
    per_page_count = request.GET.get('p_count')
    task_mes_list = models.Task.objects.order_by('-id')
    if not per_page_count:
        per_page_count = 10
    posts = Pagination(current_page, task_mes_list.count(), int(per_page_count))
    data = {
        'testcase_name': '',
        'project_id': '',
    }
    if project:
        task_mes_list = task_mes_list.filter(task_name_id=project)
        data['project_id'] = int(project)
    url = 'task.html?%s&' % (urlencode(data))
    page_str = posts.page_str(url)
    return render(request, 'task.html', {'task_list': task_mes_list.all()[posts.start:posts.end], 'page_str': page_str,
                                         'p_count': int(per_page_count), 'project_list': project_list, 'data': data})


# 项目运行生成任务
@check_ajax_login
def run_project(request):
    ret = {'status': False, 'mes': False}
    try:
        project_id = request.GET.get('nid')
        user = request.session.get('user_info')
        user_id = models.UserInfo.objects.filter(id=user['id']).first()
        work_dir, task = Building().build_project(project_id, user_id)
        if not task:
            ret['mes'] = '项目下' + work_dir + '不能为空！'
            return HttpResponse(json.dumps(ret))

        process = Runner().run(work_dir)
        print('?????????', process.pid)
        models.Task.objects.filter(id=task).update(status=process.pid)
        ret['status'] = True
    except Exception as e:
        print(e, type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))


# 套件运行生成任务
@check_ajax_login
def run_suite(request):
    ret = {'status': False, 'mes': False}
    try:
        suite_ids = request.GET.getlist('nid[]')
        user = request.session.get('user_info')
        user_id = models.UserInfo.objects.filter(id=user['id']).first()
        if suite_ids:
            work_dir, task = Building().build_suite(suite_ids, user_id)
            if not task:
                ret['mes'] = '套件下' + work_dir + '不能为空！'
                return HttpResponse(json.dumps(ret))
            if not work_dir:
                ret['status'] = False
                ret['mes'] = '请先勾选同一项目下的套件！'
            else:
                process = Runner().run(work_dir)
                print('?????????', process.pid)
                models.Task.objects.filter(id=task).update(status=process.pid)
                ret['status'] = True
        else:
            ret['mes'] = '请先勾选套件！'
    except Exception as e:
        ret['status'] = False
        print(e, type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))


# 重新启动任务
@check_login
def rerun(request):
    task_id = request.GET.get('nid')
    task = models.Task.objects.filter(id=task_id)
    user = request.session.get('user_info')
    user_id = models.UserInfo.objects.filter(id=user['id']).first()
    work_dir = os.getcwd().replace('\\', '/') + task.first().log_path
    process = Runner().run(work_dir)
    dic = {
        'status': process.pid,
        'user': user_id,
        'start_time': datetime.datetime.now(),
        'end_time': None,
        'take_time': '',
        'report_path': '',
    }
    task.update(**dic)

    return redirect('/work/task.html')

def check_status():
    # nid = request.GET.get('nid')
    task_list = models.Task.objects.all()
    print('sssssssssssssssssssssss', task_list)
    ret = {'status': False}
    pids = psutil.pids()
    for task in task_list:
        print('?????????', task.status)
        if task.status not in pids and task.status.isdigit():
            time.sleep(2)
            now_date = datetime.datetime.now()
            output_dir = os.getcwd().replace('\\', '/') + task.log_path
            tree = ET.parse(output_dir + "output.xml")
            root = tree.getroot()
            status = root.find("./suite/status").attrib["status"]
            starttime = datetime.datetime.strptime(root.find("./suite/status").attrib["starttime"], '%Y%m%d %X.%f')
            endtime = datetime.datetime.strptime(root.find("./suite/status").attrib["endtime"], '%Y%m%d %X.%f')
            dic = {
                'start_time': starttime,
                'end_time': endtime,
                'report_path': task.log_path,
                'status': status
            }
            models.Task.objects.filter(id=task.id).update(**dic)
            os.remove(output_dir + "output.xml")
            sendEmail(task.task_name, output_dir)
            ret['status'] = True
            return HttpResponse(json.dumps(ret))

    return redirect('/work/task.html')


@check_login
def stop_process(request):
    task_id = request.GET.get('nid')
    task = models.Task.objects.filter(id=task_id)
    os.popen("taskkill -pid %s -f" % task.status)
    task.update(status='运行中断')

    return redirect('/work/task.html')


@check_ajax_login
def del_task(request):
    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        models.Task.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False

    return HttpResponse(json.dumps(ret))


# 调度任务
def trigger_list(request):
    trigger_list = models.Trigger.objects.order_by('-id')

    return render(request, 'trigger.html', {'trigger_list': trigger_list})


def get_trigger(request):
    ret = {'status': False, 'mes': False}
    try:
        project_id = request.GET.get('nid')
        ret['status'] = True
        if models.Trigger.objects.filter(trigger_name=project_id):
            mes = serializers.serialize("json", models.Trigger.objects.filter(trigger_name=project_id).all())
            ret['mes'] = json.loads(mes)[0]['fields']
        else:
            ret['mes'] = False
    except Exception as e:
        print(e, type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))




def run_job(id,user):
    print('id',id)
    work_dir, task = Building().build_project(id, user)
    process = Runner().run(work_dir)
    models.Task.objects.filter(id=task).update(status=process.pid)

def scheduler_start(nid):
    trig = models.Trigger.objects.filter(id=nid)
    cron = trig.first().Cron.replace("\n", "").strip().split(" ")
    # 调度器使用DjangoJobStore()
    scheduler.add_job(run_job, trigger="cron", replace_existing=True, second=cron[0], minute=cron[1], hour=cron[2],
                      day=cron[3], month=cron[4], day_of_week=cron[5], id="%s" % trig.first().id,
                      args=(trig.first().trigger_name_id, trig.first().user))

    trig.update(enable=True)
    if not scheduler.running:
        register_events(scheduler)
        if scheduler.get_jobs():
            scheduler.start()

    return '已启动！'

def scheduler_stop(nid):

    if DjangoJob.objects.filter(id=nid):
        DjangoJobExecution.objects.filter(job=nid).delete()
        DjangoJob.objects.filter(id=nid).delete()

    return '已停止！'



try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    trigger = models.Trigger.objects.all()
    for p in trigger:
        if p.enable:
            cron = p.Cron.replace("\n", "").strip().split(" ")
            # print(cron)
            if len(cron) < 5:
                continue
            if not DjangoJob.objects.filter(id=p.id):
                @register_job(scheduler, trigger="cron",replace_existing=True,second=cron[0], minute=cron[1], hour='2', day=cron[3], month=cron[4],day_of_week=cron[5],id="%s" % p.id)
                def job_loading():
                    run_job(p.trigger_name_id,p.user)
                register_events(scheduler)
    if DjangoJob.objects.all():
        scheduler.start()
        print('??????????????????')
except Exception as e:
    # 有错误就停止定时器
    scheduler.shutdown()




@check_login
def trigger_start(request, nid):
    try:
        scheduler_start(nid)
    except Exception as e:
        return HttpResponse(str(e))
    return redirect('/work/trigger.html')


@check_login
def trigger_stop(request, nid):
    trig = models.Trigger.objects.filter(id=nid)
    trig.update(enable=False)
    try:
        scheduler_stop(nid)
    except Exception as e:
        return HttpResponse(str(e))
    return redirect('/work/trigger.html')


@check_ajax_login
def trigger_update(request):
    ret = {'status': False, 'mes': False}
    try:
        project_id = request.POST.get('project_id')
        cron = request.POST.get('cron')
        enable = request.POST.get('enable')
        user = request.session.get('user_info')
        user_id = models.UserInfo.objects.filter(id=user['id']).first()
        project = models.Project.objects.filter(id=project_id).first()
        trigger_dic = {
            'trigger_name': project,
            'enable': enable,
            'user': user_id,
            'Cron': cron,
            'status': 0
        }
        print(trigger_dic)
        trig = models.Trigger.objects.filter(trigger_name=project)
        if trig:
            trig.update(**trigger_dic)
            trig_id = trig.first().id
            if enable:
                scheduler_start(trig_id)

            else:
                scheduler_stop(trig_id)
        else:
            trig_id = models.Trigger.objects.create(**trigger_dic)
            if enable:
                scheduler_start(trig_id.id)
        ret['status'] = True


    except Exception as e:
        print(e, type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))


@check_ajax_login
def check_start(request):

    ret = {'status': False, 'mes': False}
    if request.GET.get('start') == '启动刷新':
        try:
            scheduler.add_job(func=check_status, trigger='cron', replace_existing=True, second='*/10', minute='*', hour='*', day='*', month='*', day_of_week='*',id='check')
            register_events(scheduler)
            if not scheduler.running:
                scheduler.start()
            ret['status'] = True
            ret['start'] = '停止刷新'
        except Exception as f:
            ret['mes'] = str(f)
    else:
        try:
            scheduler_stop("check")
            ret['status'] = True
            ret['start'] = '启动刷新'
        except Exception as f:
            ret['mes'] = str(f)
    return HttpResponse(json.dumps(ret))


@check_ajax_login
def mt_check(request):

    ret = {'status': False, 'mes': False, 're_check': False}
    print(scheduler.get_jobs())
    print(scheduler.get_job('check'))
    if DjangoJob.objects.filter(id='check'):
        ret['re_check'] = True
    nid = request.GET.get('nid')
    try:
        task_id = check_status()
        if nid == task_id:
            ret['status'] = True
    except KeyError:
        pass
    return HttpResponse(json.dumps(ret))