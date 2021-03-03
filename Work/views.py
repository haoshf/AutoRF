from django.shortcuts import render,HttpResponse,redirect
from repository import models
from utils.run import Runner
from utils.building import Building
import json,os,datetime
from utils.pagination import Pagination
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
from utils.trigger import Trigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import JsonResponse
from django.core import serializers
from backend.auth.auth import check_login,check_ajax_login
from utils.Send_email import sendEmail

def task(request):
    project_list = models.Project.objects.all()
    project = request.GET.get('project')
    current_page = request.GET.get('p')
    per_page_count = request.GET.get('p_count')
    task_list = models.Task.objects.order_by('-id')
    if not per_page_count:
        per_page_count=10
    posts = Pagination(current_page,task_list.count(),int(per_page_count))
    data = {
        'testcase_name':'',
        'project_id':'',
    }
    if project:
        task_list = task_list.filter(task_name_id=project)
        data['project_id'] = int(project)
    url = 'task.html?%s&'%(urlencode(data))
    page_str = posts.page_str(url)
    return render(request,'task.html',{'task_list':task_list.all()[posts.start:posts.end],'page_str':page_str,'p_count':int(per_page_count),'project_list':project_list,'data':data})

task_list = []
#项目运行生成任务
@check_ajax_login
def run_project(request):

    ret = {'status': False,'mes':False}
    try:
        project_id = request.GET.get('nid')
        user = request.session.get('user_info')
        user_id = models.UserInfo.objects.filter(id=user['id']).first()
        work_dir,task = Building().build_project(project_id,user_id)
        if not task:
            ret['mes'] = '项目下'+work_dir+'不能为空！'
            return HttpResponse(json.dumps(ret))
        process = Runner().run(work_dir)
        ret['status'] = True
        task_list.append((task,process))

    except Exception as e:
        print(e,type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))

#套件运行生成任务
@check_ajax_login
def run_suite(request):

    ret = {'status': False,'mes':False}
    try:
        suite_ids = request.GET.getlist('nid[]')
        user = request.session.get('user_info')
        user_id = models.UserInfo.objects.filter(id=user['id']).first()
        if suite_ids:
            work_dir,task = Building().build_suite(suite_ids,user_id)
            if not task:
                ret['mes'] = '套件下'+work_dir + '不能为空！'
                return HttpResponse(json.dumps(ret))
            if not work_dir:
                ret['status'] = False
                ret['mes'] = '请先勾选同一项目下的套件！'
            else:
                process=Runner().run(work_dir)
                task_list.append((task, process))
                ret['status'] = True
        else:
            ret['mes'] = '请先勾选套件！'
    except Exception as e:
        ret['status'] = False
        print(e,type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))

#重新启动任务
@check_login
def rerun(request):

    task_id = request.GET.get('nid')
    task = models.Task.objects.filter(id=task_id)
    user = request.session.get('user_info')
    user_id = models.UserInfo.objects.filter(id=user['id']).first()
    dic = {
        'status': '运行中',
        'user': user_id,
        'start_time': datetime.datetime.now(),
        'end_time':None,
        'take_time': '',
        'report_path': '',
    }
    task.update(**dic)
    work_dir= os.getcwd().replace('\\','/')+task.first().log_path
    process = Runner().run(work_dir)
    task_list.append((task.first(), process))

    return redirect('/work/task.html')

def check_status():

    print('?????????', task_list)
    # nid = request.GET.get('nid')
    ret = {'status':False}
    for i in range(len(task_list)):
        print('?????????',task_list[i])
        if task_list[i][1].poll() is not None:
            task = models.Task.objects.filter(id=task_list[i][0].id).first()
            now_date = datetime.datetime.now()
            output_dir = os.getcwd().replace('\\','/')+task.log_path
            tree = ET.parse(output_dir + "output.xml")
            root = tree.getroot()
            status = root.find("./suite/status").attrib["status"]
            starttime = datetime.datetime.strptime(root.find("./suite/status").attrib["starttime"],'%Y%m%d %X.%f')
            endtime = datetime.datetime.strptime(root.find("./suite/status").attrib["endtime"],'%Y%m%d %X.%f')
            dic = {
                'start_time':starttime,
                'end_time':endtime,
                'report_path':task.log_path,
                'status':status
            }
            models.Task.objects.filter(id=task_list[i][0].id).update(**dic)
            os.remove(output_dir + "output.xml")
            taskid = str(task_list[i][0].id)
            task_list.pop(i)
            sendEmail(task.task_name,output_dir)
            # if nid == taskid:
            #     ret['status']=True
            #     return HttpResponse(json.dumps(ret))
            return taskid
        else:
            return HttpResponse(json.dumps(ret))

    return redirect('/work/task.html')

@check_login
def stop_process(request):

    task_id = request.GET.get('nid')
    print(task_list)
    for i in range(len(task_list)):

        if str(task_id) == str(task_list[i][0].id):
            task_list[i][1].terminate()
            os.kill(task_list[i][1].pid,-9)
            if not task_list[i][1].poll():
                dic = {
                    'status': '中断'
                }
                models.Task.objects.filter(id=task_list[i][0].id).update(**dic)
                task_list.pop(i)

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

#调度任务
def trigger_list(request):

    trigger_list = models.Trigger.objects.order_by('-id')

    return render(request, 'trigger.html',{'trigger_list':trigger_list})

def get_trigger(request):
    ret = {'status': False,'mes':False}
    try:
        project_id = request.GET.get('nid')
        ret['status'] = True
        if models.Trigger.objects.filter(trigger_name=project_id):
            mes = serializers.serialize("json", models.Trigger.objects.filter(trigger_name=project_id).all())
            ret['mes']= json.loads(mes)[0]['fields']
        else:
            ret['mes'] = False
    except Exception as e:
        print(e,type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))

def Cron(nid,user_id):
    work_dir, task = Building().build_project(nid,user_id)
    process = Runner().run(work_dir)
    task_list.append((task, process))
scheduler = Trigger(Cron)  # 创建一个调度器对象
scheduler.setup()
trigger = scheduler.load_job_list()

if scheduler.get_jobs():
    scheduler.start()

@check_login
def trigger_start(request,nid):
    trig = models.Trigger.objects.filter(id=nid)
    trig.update(enable=True)
    scheduler.add_work_job(nid)
    if not scheduler.is_running():
        scheduler.start()
    return redirect('/work/trigger.html')

@check_login
def trigger_stop(request,nid):

    trig = models.Trigger.objects.filter(id=nid)
    trig.update(enable=False)
    scheduler.remove_job(nid)
    if not scheduler.get_jobs():
        scheduler.shutdown()
    return redirect('/work/trigger.html')

@check_ajax_login
def trigger_update(request):
    ret = {'status': False,'mes':False}
    try:
        project_id = request.POST.get('project_id')
        cron = request.POST.get('cron')
        enable = request.POST.get('enable')
        user = request.session.get('user_info')
        user_id = models.UserInfo.objects.filter(id=user['id']).first()
        project = models.Project.objects.filter(id=project_id).first()
        trigger_dic = {
            'trigger_name':project,
            'enable':enable,
            'user':user_id,
            'Cron':cron,
            'status':0
        }
        print(trigger_dic)
        trig = models.Trigger.objects.filter(trigger_name=project)
        if trig:
            trig.update(**trigger_dic)
            trig_id = trig.first().id
            if enable:
                scheduler.add_work_job(trig_id)
                if not scheduler.is_running():
                    scheduler.start()
            else:
                scheduler.remove_job(trig_id)
        else:
            trig_id = models.Trigger.objects.create(**trigger_dic)
            if enable:
                scheduler.add_work_job(trig_id)
                if not scheduler.is_running():
                    scheduler.start()
        ret['status'] = True


    except Exception as e:
        print(e,type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))

@check_ajax_login
def check_start(request):

    ret = {'status': False,'mes':False}
    if request.GET.get('start') == '启动刷新':
        try:
            print('??????????????')
            trigger.add_job(func=check_status, trigger='cron', replace_existing=True,
                                               second='*/10',minute='*', hour='*', day='*', month='*', day_of_week='*',
                                                       id="check")
            if not scheduler.is_running():
                scheduler.start()
            ret['status'] = True
            ret['start'] = '停止刷新'
        except Exception as f:
            ret['mes'] = str(f)
    else:
        try:
            scheduler.remove_job("check")
            if not scheduler.get_jobs():
                scheduler.shutdown()
            ret['status'] = True
            ret['start'] = '启动刷新'
        except Exception as f:
            ret['mes'] = str(f)
    return HttpResponse(json.dumps(ret))

@check_ajax_login
def mt_check(request):

    ret = {'status': False,'mes':False}
    nid = request.GET.get('nid')
    task_id = check_status()
    if nid == task_id:
        ret['status']=True
    return HttpResponse(json.dumps(ret))