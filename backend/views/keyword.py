from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository import models
import datetime,json,time
from backend.forms import Keyword
from utils.pagination import Pagination
from django.urls import reverse
from django.core.paginator import Paginator, Page
from utils.building import Building
from django.db.models import Q
from urllib.parse import urlencode
from ..auth.auth import check_login,check_ajax_login

#关键字管理
def keyword(request, *args, **kwargs):

    resource_list = models.Resource.objects.all()
    library_list = models.Library.objects.all()
    keyword_name = request.GET.get('keyword_name')
    resource = request.GET.get('resource')
    library = request.GET.get('library')
    current_page = request.GET.get('p')
    per_page_count = request.GET.get('p_count')
    if not per_page_count:
        per_page_count=10
    data = {
        'keyword_name':'',
        'resource':'',
        'library':''
    }
    keyword_list = models.Keyword.objects
    method_list = models.Method.objects
    if keyword_name:
        keyword_list = keyword_list.filter(keyword_name__startswith=keyword_name)
        method_list = method_list.filter(method_name__startswith=keyword_name)
        data['keyword_name'] =keyword_name

    if resource:
        keyword_list = keyword_list.filter(resource=resource)
        data['resource'] = int(resource)
    if library:
        method_list = method_list.filter(library=library)
        data['library'] = int(library)

    keyword_list_1 =[ keyword for keyword in keyword_list.all()]
    keyword_list_2 =[ keyword for keyword in method_list.all()]
    keyword_list = keyword_list_1 + keyword_list_2
    posts = Pagination(current_page,len(keyword_list),int(per_page_count))
    page_str = posts.page_str('keyword.html?%s&'%(urlencode(data)))
    return render(request, 'keyword.html', {'keyword_list': keyword_list[posts.start:posts.end],'resource_list':resource_list,'library_list':library_list,'page_str':page_str,'data':data,'p_count':int(per_page_count)})

@check_login
def keyword_add(request):
    table_size = {'tr': '12345', 'td': '12345'}
    table_tr_list = []
    for i in table_size['tr']:
        table_td_list = []
        for j in table_size['td']:
            table_td_list.append('')
        table_tr_list.append(table_td_list)
    if request.method == 'GET':
        form = Keyword(request=request)
    else:
        form = Keyword(request=request,data=request.POST)
        resource = request.POST.get('resource')

        if form.is_valid():
            dic = {}
            dic['create_time'] = datetime.datetime.now()
            dic['resource'] = models.Resource.objects.filter(id=form.cleaned_data['resource']).first()
            form.cleaned_data.pop('resource')
            dic.update(form.cleaned_data)
            models.Keyword.objects.create(**dic)
            return redirect('/keyword.html')

    return render(request, 'keyword_add.html',{'form':form,'table_tr_list':table_tr_list})

@check_login
def keyword_edit(request,nid):

    obj = models.Keyword.objects.filter(id=nid).first()
    if request.method == 'GET':
        if not obj:
            return render(request, 'backend_no_article.html')
        #关联的资源

        init_dict = {
            'id': obj.id,
            'resource':obj.resource.id,
            'keyword_name': obj.keyword_name,
            'Documentation': obj.Documentation,
            'Arguments': obj.Arguments,
            'Teardown': obj.Teardown,
            'Return_Value': obj.Return_Value,
            'Timeout': obj.Timeout,
            'Tags': obj.Tags,
            'Table_value': obj.Table_value,
        }
        Table_value = json.loads(init_dict['Table_value'])
        table_size = {'tr': [1,2,3,4,5], 'td': [1,2,3,4,5]}
        table_tr_list = Building().deal_table(Table_value,table_size)

        form = Keyword(request=request, data=init_dict)
        return render(request, 'keyword_edit.html', {'form': form, 'nid': nid,'table_tr_list':table_tr_list})
    else:
        form = Keyword(request=request,data=request.POST)
        if form.is_valid():
            if form.cleaned_data['keyword_name'] != obj.keyword_name:
                form = Keyword(request=request,data=request.POST)
            if form.is_valid():
                dic = {}
                dic['update_time'] = datetime.datetime.now()
                dic.update(form.cleaned_data)
                models.Keyword.objects.filter(id=nid).update(**dic)
                return redirect('/keyword.html')
    return render(request, 'keyword_edit.html',{'form':form, 'nid': nid})

@check_ajax_login
def del_keyword(request):

    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        models.Keyword.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False

    return HttpResponse(json.dumps(ret))

#查询操作
@check_login
def keywords_select(request):
    data = {'status':True}
    try:
        resource = request.GET.get('resource')
        suite = request.GET.get('suite')
        keyword_list = [{'keyword': '${}'},{'keyword': '@{}'},{'keyword': '&{}'},{'keyword': '${json}'},]
        if resource:
            res = models.Resource.objects.filter(id=resource).first()
            keywords = models.Keyword.objects.filter(Q(resource__in=eval(res.Resource))|Q(resource=resource))
        if suite:
            sui = models.Suite.objects.filter(id=suite).first()
            keywords = models.Keyword.objects.filter(resource__in=eval(sui.Resource))
        for keyword in keywords:
            keyword_dict = {'keyword': keyword.keyword_name}
            if keyword_dict not in keyword_list:
                keyword_list.append(keyword_dict)
        data['keyword_list'] = keyword_list

    except Exception:
        data['status'] =False
    return HttpResponse(json.dumps(data))