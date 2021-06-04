from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository import models
import datetime,json,time
from utils.pagination import Pagination
from django.urls import reverse
from django.core.paginator import Paginator, Page
import os,codecs,platform
import importlib
from inspect import signature
from utils import parser
from urllib.parse import urlencode
from backend.auth.auth import check_login,check_ajax_login
import subprocess
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
import psutil,signal

#库管理
def jmx(request):
    jmx_list = []
    for root, dirs, files in os.walk('./JmeterFile'):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        for file in files:
            if file.endswith('.jmx'):
                jmx_list.append(file)

    return render(request, 'jmx.html', {'jmx_list': jmx_list})

@check_login
def up_jmx(request):

    from types import FunctionType, MethodType
    files = request.FILES.getlist('k3')
    print(files)
    for file in files:
        print('?????',file)
        filepath = './JmeterFile/'+file.name
        f = open(filepath, 'wb')
        for line in file.chunks():
            f.write(line)
        f.close()

    return redirect('/api/jmx_list')

def jmx_detail(request,page):

    lib_path = (os.getcwd() + "/JmeterFile/{}.jmx".format(page)).replace("\\", "/")
    if os.path.exists(lib_path):
        if "Windows" in platform.platform():
            f = codecs.open(lib_path, "r", encoding='UTF-8')
        else:
            f = codecs.open(lib_path, "r", encoding='UTF-8')

        pyfile = f.read()
        f.close()
        return render(request,'jmx_detail.html', {'pyfile':pyfile,'page':page})
    else:
        return render(request,'jmx_detail.html', {'pyfile':'第三方资源库，不支持查看','page':page})

@check_ajax_login
def run_xn(request):
    ret = {'status': False, 'mes': False}
    try:
        jmx = request.POST.get('jmx')
        xiancheng = request.POST.get('xiancheng')
        shijian = request.POST.get('shijian')
        print(jmx,xiancheng,shijian)
        if 'Linux' in platform.platform():
            command = "./JmeterFile/start.sh {0} {1} {2}" .format(jmx,xiancheng,shijian)
        else:
            command = "./JmeterFile/start.sh {0} {1} {2}" .format(jmx,xiancheng,shijian)
        shell = True
        _out_fd = open("./JmeterFile/%s.log"%jmx[:-4], "w")
        process = subprocess.Popen(command, shell=shell, stdout=_out_fd, stderr=subprocess.STDOUT)
        ret['status'] = True

    except Exception as e:
        print(e, type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))

@check_login
def xn_logs(request):

    jmx = request.GET.get('jmx')
    log_path = "./JmeterFile/%s.log"%jmx[:-4]

    logs = "还没捕获到日志信息^_^"
    if os.path.exists(log_path):
        if "Windows" in platform.platform():
            f = codecs.open(log_path, "r", encoding='UTF-8')
        else:
            f = codecs.open(log_path, "r", encoding='UTF-8')

        logs = f.read()
        f.close()

    return render(request,'xn_logs.html', {'logs':logs,'jmx':jmx})

@check_login
def xn_download(request):
    jmx = request.GET.get('jmx')
    file_path = "./JmeterFile/%s.zip"%jmx[:-4]
    import re
    r = re.compile(r'\w*%s\w*\.zip$'%jmx[:-4])
    for root, dirs, files in os.walk('./JmeterFile'):
        l = [x for x in files if r.match(x)]
        if l==[]:
            return HttpResponse("Sorry but Not Found the File")
        else:
            file_path ="./JmeterFile/%s"%l[0]
            print('-----------------',file_path)
            break

    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """

        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    try:
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
        response = StreamingHttpResponse(file_iterator(file_path))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment;filename="{}.zip"'.format(escape_uri_path(jmx[:-4]))
    except:
        return HttpResponse("Sorry but Not Found the File")
    return response

def jmx_del(request):
    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        print('nid',nid)
        for file in nid:
            os.remove('./JmeterFile/%s'%file)
    except Exception as e:
        ret['status'] = False

    return HttpResponse(json.dumps(ret))


def check_locu(request):

    ret = {'status': False, 'mes': False}
    net_con = psutil.net_connections()
    for con_info in net_con:
        if con_info.laddr.port == 8080:
            print('.............', con_info.laddr.port)
            ret['mes'] = '正在运行中,是否重新运行？'
            return HttpResponse(json.dumps(ret))
    else:
        ret['status'] = True
        return HttpResponse(json.dumps(ret))

def locust_run(request):

    ret = {'status': False, 'mes': False}
    host = request.get_host().split(':')[0]
    print('??????',host)
    ret['host'] = host
    try:
        if request.GET.get('status')=='1':
            net_con = psutil.net_connections()
            for con_info in net_con:
                if con_info.laddr.port == 8080:
                    print('.............', con_info.laddr.port)
                    os.popen("taskkill -pid %s -f" % con_info.pid)
                    return redirect('/api/locust_run.html')
        command = "locust -f ./utils/day2.py --host=https://boptest1.jvtdtest.top --web-host=0.0.0.0 -P 8080"
        shell = True
        _out_fd = open("locust.log", "w")
        process = subprocess.Popen(command, shell=shell, stdout=_out_fd, stderr=subprocess.STDOUT)
        ret['status'] = True
        time.sleep(2)
    except Exception as e:
        print(e, type(e))
        ret['mes'] = str(e)
    return render(request,'locust_layout.html',{'ret':ret})