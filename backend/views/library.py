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
from ..auth.auth import check_login,check_ajax_login
from django.db.models import Q

#库管理
def library(request, *args, **kwargs):

    library_name = request.GET.get('library_name')
    data = {
        'library_name':'',
    }
    if library_name:
        library_list = models.Library.objects.filter(~Q(library_name='SqlDB.py')&Q(library_name__startswith=library_name))
        data['library_name'] =library_name
    else:
        library_list = models.Library.objects.filter(~Q(library_name='SqlDB.py'))
    current_page = request.GET.get('p')
    per_page_count = request.GET.get('p_count')
    if not per_page_count:
        per_page_count=10
    data['p_count'] = int(per_page_count)
    posts = Pagination(current_page,library_list.count(),int(per_page_count))
    url = 'library.html?%s&'%(urlencode(data))
    page_str = posts.page_str(url)
    return render(request, 'library.html', {'library_list': library_list.all()[posts.start:posts.end],'page_str':page_str,'data':data})


@check_login
def up_library(request):

    from types import FunctionType, MethodType
    files = request.FILES.getlist('k3')
    for file in files:
        filepath = '/Library/'+file.name
        f = open('.'+filepath, 'wb')
        for line in file.chunks():
            f.write(line)
        f.close()
        time.sleep(2)
        imp = 'Library.{0}'.format(file.name[:-3])
        q = importlib.import_module(imp)
        t = eval('q.{0}'.format(file.name[:-3]))
        dic = {
            'library_name': file.name,
            'documentation': t.__doc__,
            'class_name': t.__name__,
            'filepath': filepath
        }
        if models.Library.objects.filter(library_name=file.name).count():
            dic['update_time'] = datetime.datetime.now()
            library = models.Library.objects.filter(library_name=file.name)
            library.update(**dic)
            library_id=library.first()
        else:
            dic['create_time'] = datetime.datetime.now()
            library_id = models.Library.objects.create(**dic)
        for k,v in t.__dict__.items():
            if isinstance(v,FunctionType) and k !='__init__':
                Arguments = list(signature(v).parameters.keys())
                Arguments.pop(0)
                dic = {
                    'library': library_id,
                    'method_name': k,
                    'documentation': v.__doc__,
                    'Arguments': Arguments,
                    'Return_Value': ''
                }
                if models.Method.objects.filter(method_name=k).count():
                    dic['update_time'] = datetime.datetime.now()
                    models.Method.objects.filter(method_name=k).update(**dic)
                else:
                    dic['create_time'] = datetime.datetime.now()
                    models.Method.objects.create(**dic)
    return redirect('/library.html')

def library_detail(request,nid):

    obj = models.Library.objects.filter(id=nid).first()
    lib_path = (os.getcwd() + "/Library/{}".format(obj.library_name)).replace("\\", "/")

    if os.path.exists(lib_path):
        if "Windows" in platform.platform():
            f = codecs.open(lib_path, "r", encoding='UTF-8')
        else:
            f = codecs.open(lib_path, "r", encoding='UTF-8')

        pyfile = f.read()
        f.close()
        return render(request,'library_detail.html', {'pyfile':pyfile,'library':obj.library_name})
    else:
        return render(request,'library_detail.html', {'pyfile':'第三方资源库，不支持查看','library':obj.library_name})

@check_ajax_login
def del_library(request):

    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        print('nid',nid)
        models.Library.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False

    return HttpResponse(json.dumps(ret))


#初始化资源
@check_login
def init(request):
    data = {'status':True}
    try:
        data['mes']=parser.parser()
    except Exception:
        data['status'] = False
    return HttpResponse(json.dumps(data))