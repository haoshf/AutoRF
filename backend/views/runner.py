from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository import models
import datetime,json,time
from utils.run import Runner
from utils.building import Building
import os,codecs,platform
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Q
from ..auth.auth import check_login,check_ajax_login


Runner = Runner()
#运行配置
@check_ajax_login
def run_testcase(request):

    ret = {'status': True,'read_mes':False}
    try:
        nid = request.POST.getlist('nid[]')
        user = request.session.get('user_info')
        print('??????????')
        if nid:
            print('zzzzzzzzz')
            work_dir = Building().build_testcase(nid,str(user['id']))
            Runner.run(work_dir)
        else:
            print('xxxxxxxxxxx')
            ret['status'] = False
            ret['mes'] = '请先勾选用例！'
    except Exception as e:
        print('cccccccccccc')
        ret['status'] = False
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))

def stop(request):
    nid = request.GET.get('nid')
    try:
        Runner.stop()
        a = '已终止!'
    except Exception:
        a = '已停止运行！'
    return render(request,'logs.html', {'logs':a,'nid':nid})

@check_login
def run_logs(request):
    nid = request.GET.get('nid')
    user = request.session.get('user_info')
    if not nid:
        log_path = os.getcwd().replace("\\", "/") + "/robot/%s/getImgcode.log"%user['id']
    else:
        task = models.Task.objects.filter(id=nid).first()
        log_path = os.getcwd().replace('\\','/') + task.log_path+"getImgcode.log"

    logs = "还没捕获到日志信息^_^"
    if os.path.exists(log_path):
        if "Windows" in platform.platform():
            f = codecs.open(log_path, "r", encoding='UTF-8')
        else:
            f = codecs.open(log_path, "r", encoding='UTF-8')

        logs = f.read()
        f.close()

    return render(request,'logs.html', {'logs':logs,'nid':nid})

@check_login
def look_report(request):
    nid = request.GET.get('nid')

    return render(request,'reports.html',{'nid':nid})

@xframe_options_exempt
def reportpage(request):

    nid = request.GET.get('nid')
    user = request.session.get('user_info')

    print('nid__________',type(nid),nid)
    if not nid:
        return HttpResponse('''<html><script>window.history.go(-2)</script><body></body></html>''')
    elif not eval(nid):
        log_path = os.getcwd().replace("\\", "/") + "/robot/%s/report.html"%user['id']
    else:
        task = models.Task.objects.filter(id=nid).first()
        log_path = os.getcwd().replace('\\','/') + task.report_path+"report.html"
        print(log_path)
    reportmes = '报告未生成，请耐心等待！'
    if os.path.exists(log_path):
        if "Windows" in platform.platform():
            f = codecs.open(log_path, "r", encoding='UTF-8')
        else:
            f = codecs.open(log_path, "r", encoding='UTF-8')

        reportmes = f.read()
        f.close()
    return HttpResponse(reportmes)

@xframe_options_exempt
def logpage(request):
    url = request.environ['HTTP_REFERER']
    print('???????????',url)
    nid = url.split('=')[1]
    user = request.session.get('user_info')
    print('nid__________',type(nid),nid)
    if not eval(nid):
        log_path = os.getcwd().replace('\\', '/') + "/robot/%s/log.html"%user['id']
    else:
        task = models.Task.objects.filter(id=nid).first()
        log_path = os.getcwd().replace('\\','/') + task.report_path+"/log.html"

    if os.path.exists(log_path):
        if "Windows" in platform.platform():
            f = codecs.open(log_path, "r", encoding='UTF-8')
        else:
            f = codecs.open(log_path, "r", encoding='UTF-8')

        logmes = f.read()
        f.close()
    return HttpResponse(logmes)