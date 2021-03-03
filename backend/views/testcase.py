from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository import models
import datetime,json,time
from backend.forms import Testcase,Testcase_add
from utils.pagination import Pagination
from django.urls import reverse
from utils.building import Building
from utils import parser
import os,codecs,platform
from django.db.models import Q
from urllib.parse import urlencode
from ..auth.auth import check_login,check_ajax_login


#用例管理
def testcase(request, *args, **kwargs):

    suite_list = models.Suite.objects.all()
    testcase_name = request.GET.get('testcase_name')
    suite = request.GET.get('suite')
    current_page = request.GET.get('p')
    per_page_count = request.GET.get('p_count')
    data = {
        'testcase_name':'',
        'suite':'',
    }

    testcase_list = models.Testcase.objects.order_by('sort').order_by('suite__sort')
    if testcase_name:
        testcase_list = testcase_list.filter(testcase_name__startswith=testcase_name)
        data['testcase_name'] =testcase_name
    if suite:
        testcase_list = testcase_list.filter(suite=suite)
        data['suite'] = int(suite)
    if not per_page_count:
        per_page_count=10
    posts = Pagination(current_page,testcase_list.count(),int(per_page_count))
    url = 'testcase.html?%s&'%(urlencode(data))
    page_str = posts.page_str(url)
    return render(request, 'testcase.html', {'testcase_list': testcase_list.all()[posts.start:posts.end],'suite_list':suite_list,'page_str':page_str,'data':data,'p_count':int(per_page_count)})

@check_login
def testcase_add(request):
    table_size = {'tr': '12345', 'td': '12345'}
    table_tr_list = []
    for i in table_size['tr']:
        table_td_list = []
        for j in table_size['td']:
            table_td_list.append('')
        table_tr_list.append(table_td_list)

    if request.method == 'GET':
        form = Testcase(request=request)
    else:
        form = Testcase_add(request=request,data=request.POST)
        if form.is_valid():
            dic = {}
            dic['create_time'] = datetime.datetime.now()
            dic['suite'] = models.Suite.objects.filter(id=form.cleaned_data['suite']).first()
            form.cleaned_data.pop('suite')
            dic.update(form.cleaned_data)
            models.Testcase.objects.create(**dic)
            return redirect('/testcase.html')
    return render(request, 'testcase_add.html',{'form':form,'table_tr_list':table_tr_list})

@check_login
def testcase_edit(request,nid):

    obj = models.Testcase.objects.filter(id=nid).first()
    if request.method == 'GET':
        if not obj:
            return render(request, 'backend_no_article.html')
        #关联的资源
        init_dict = {
            'id': obj.id,
            'suite':obj.suite.id,
            'testcase_name': obj.testcase_name,
            'Documentation': obj.Documentation,
            'Setup': obj.Setup,
            'Teardown': obj.Teardown,
            'Template': obj.Template,
            'Timeout': obj.Timeout,
            'Tags': obj.Tags,
            'Table_value': obj.Table_value,
        }
        Table_value = json.loads(init_dict['Table_value'])
        table_size = {'tr': [1,2,3,4,5], 'td': [1,2,3,4,5]}
        table_tr_list = Building().deal_table(Table_value,table_size)
        form = Testcase(request=request, data=init_dict)
        return render(request, 'testcase_edit.html', {'form': form, 'nid': nid,'table_tr_list':table_tr_list,'Table_value':Table_value})
    else:
        form = Testcase(request=request,data=request.POST)
        if form.is_valid():
            print(form.cleaned_data['suite'],obj.suite.id)
            if form.cleaned_data['testcase_name'] != obj.testcase_name or str(form.cleaned_data['suite']) != str(obj.suite.id):
                form = Testcase_add(request=request,data=request.POST)
            if form.is_valid():
                dic = {}
                dic['update_time'] = datetime.datetime.now()
                dic.update(form.cleaned_data)
                models.Testcase.objects.filter(id=nid).update(**dic)
                return redirect('/testcase.html')
    return render(request, 'testcase_edit.html',{'form':form, 'nid': nid})

@check_ajax_login
def del_testcase(request):

    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        models.Testcase.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False

    return HttpResponse(json.dumps(ret))