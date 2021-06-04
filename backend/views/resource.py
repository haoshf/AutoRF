from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository import models
import datetime,json,time
from backend.forms import Resource,Resource_add
from utils.pagination import Pagination
from django.urls import reverse
from django.core.paginator import Paginator, Page
import os,codecs,platform
from django.db.models import Q
from urllib.parse import urlencode
from ..auth.auth import check_login,check_ajax_login
import re


#资源管理
def resource(request):
    project_id = request.GET.get('project')
    resource = request.GET.get('resource')
    current_page = request.GET.get('p')
    per_page_count = request.GET.get('p_count')
    data = {
        'project':'',
        'resource':'',
        'p_count':''
    }
    project_list = models.Project.objects.all()
    resource_list = models.Resource.objects
    if resource:
        resource_list = resource_list.filter(resource_name__startswith=resource)
        data['resource']=resource
    if project_id:
        project_pro = models.Project.objects.filter(id=project_id).first()
        resource_list = resource_list.filter(Q(project=project_id)|Q(project__in=eval(project_pro.pro2)))
        data['project']=int(project_id)
        print(data['project'])
    if not per_page_count:
        per_page_count=10
    data['p_count'] = int(per_page_count)
    posts = Pagination(current_page,resource_list.count(),int(per_page_count))
    url = 'resource.html?%s&'%(urlencode(data))
    page_str = posts.page_str(url)
    return render(request, 'resource.html', {'resource_list': resource_list.all()[posts.start:posts.end],'project_list':project_list,'page_str':page_str,'data':data})

@check_login
def resource_add(request):
    if request.method == 'GET':
        form = Resource(request=request)
    else:
        form = Resource(request=request,data=request.POST)
        if form.is_valid():
            dic = {}
            dic['create_time'] = datetime.datetime.now()
            dic['project'] = models.Project.objects.filter(id=form.cleaned_data['project']).first()
            form.cleaned_data.pop('project')
            dic.update(form.cleaned_data)
            models.Resource.objects.create(**dic)
            return redirect('/resource.html')
    return render(request, 'resource_add.html',{'form':form})

@check_login
def resource_edit(request,nid):

    obj = models.Resource.objects.filter(id=nid).first()
    if request.method == 'GET':
        if not obj:
            return render(request, 'backend_no_article.html')
        #关联的资源
        resource = obj.Resource
        resource_list = eval(resource)
        rowIds = [int(res) for res in resource_list]
        pro_res = models.Resource.objects.filter(Q(project=obj.project.id)|Q(project__in=eval(obj.project.pro2))).values('id','resource_name')
        if resource_list != []:
            resource = models.Resource.objects.filter(id__in=resource_list).values_list('id','resource_name')
            if resource:
                resource = list(zip(*resource))[0]
        #关联的库
        library = obj.Library
        library_list = eval(library)
        if library_list != []:
            library = models.Library.objects.filter(id__in=library_list).values_list('id','library_name')
            if library:
                library = list(zip(*library))[0]
        init_dict = {
            'id': obj.id,
            'project':obj.project.id,
            'resource_name': obj.resource_name,
            'Documentation': obj.Documentation,
            'Library': library,
            'Resource': resource,
            'Variables':obj.Variables,
            'Scalar_Variables':obj.Scalar_Variables,
            'List_Variables': obj.List_Variables,
            'Dict_Variables': obj.Dict_Variables,
        }
        form = Resource(request=request, data=init_dict)
        return render(request, 'resource_edit.html', {'form': form, 'nid': nid,'resource_list':pro_res,'rowIds':rowIds})
    else:
        form = Resource(request=request,data=request.POST)
        if form.is_valid():
            if form.cleaned_data['resource_name'] != obj.resource_name:
                form = Resource_add(request=request,data=request.POST)
            if form.is_valid():
                dic = {}
                dic['update_time'] = datetime.datetime.now()
                dic.update(form.cleaned_data)
                models.Resource.objects.filter(id=nid).update(**dic)
                return redirect('/resource.html')
    return render(request, 'resource_edit.html',{'form':form, 'nid': nid})

@check_ajax_login
def del_resource(request):

    ret = {'status': True}
    try:
        print(request.POST)
        nid = request.POST.getlist('nid[]')
        print('...............',nid)
        models.Resource.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False

    return HttpResponse(json.dumps(ret))

#上传资源文件入库
@check_login
def up_resource(request):
    ret = {'status': True}
    from types import FunctionType, MethodType
    project_id = request.POST.get('project')
    project = models.Project.objects.filter(id=project_id).first()
    if not os.path.exists('./robot/%s/'%project.project_name):
        os.makedirs('./robot/%s/'%project.project_name)
        os.makedirs('./robot/%s/resource'%project.project_name)
    elif not os.path.exists('./robot/%s/resource'%project.project_name):
        os.makedirs('./robot/%s/resource'%project.project_name)
    files = request.FILES.getlist('k3')
    a = 0
    error_list = ['error']
    while error_list!=[] and a<2:
        a+=1
        print(a)
        error_list = []
        for file in files:
            print(file)
            if not file.name.endswith('.robot'):
                filepath = './robot/runCase/%s'%file.name
                f = open(filepath, 'wb')
                for line in file.chunks():
                    f.write(line)
                f.close()
            elif file.name == '__init__.robot':
                continue
            else:
                Table_list = []
                filepath = './robot/%s/resource/%s'%(project.project_name,file.name)
                f = open(filepath, 'wb')
                for line in file.chunks():
                    f.write(line)
                f.close()
                time.sleep(1)
                f = open(filepath, 'r',encoding='utf8')
                resource_id = models.Resource.objects.filter(Q(resource_name=file.name[:-6])&(Q(project=project_id)|(Q(project__in=eval(project.pro2))))).first()
                resource_dict = {
                    'project': project,
                    'resource_name': file.name[:-6],
                    'Documentation': '',
                    'Library': [],
                    'Resource': [],
                    'Variables': '',
                    'Scalar_Variables': '',
                    'List_Variables': '',
                    'Dict_Variables': '',
                    'create_time': datetime.datetime.now(),
                }
                Variables = False
                try:
                    for line in f.readlines():
                        print('line=========',line)
                        if line.startswith('*** Settings ***'):
                            continue
                        elif line.startswith('Documentation'):
                            resource_dict['Documentation']=line.split('    ')[-1]
                        elif line.startswith('...'):
                            resource_dict['Documentation']+=line.split('    ')[-1]
                        elif line.startswith('Library'):
                            library_name = line.split(' ')[-1].split('/')[-1].replace('\n','')
                            Lib = models.Library.objects.filter(library_name=library_name).first()
                            resource_dict['Library'].append(Lib.id)
                        elif line.startswith('Resource'):
                            Lib = models.Resource.objects.filter(Q(resource_name=line.split(' ')[-1][:-7].lstrip())&Q(project=project_id)).first()
                            if not Lib:
                                error_list.append(str(file.name[:-6]+'---未找到依赖资源！'))
                                break
                            print('lib****',Lib)
                            resource_dict['Resource'].append(Lib.id)
                        elif line.startswith('*** Variables ***'):
                            Variables = True
                        elif line.startswith('$') and Variables:
                            if resource_dict['Scalar_Variables']:
                                resource_dict['Scalar_Variables'] += '|' + re.sub('\s+', '=', line.strip())
                            else:
                                resource_dict['Scalar_Variables'] += re.sub('\s+', '=', line.strip())
                        elif line.startswith('@') and Variables:
                            if resource_dict['List_Variables']:
                                resource_dict['List_Variables'] += '|' + re.sub('\s+', '=', line.strip())
                            else:
                                resource_dict['List_Variables'] += re.sub('\s+', '=', line.strip())
                        elif line.startswith('&') and Variables:
                            if resource_dict['Dict_Variables']:
                                resource_dict['Dict_Variables'] += '|' + re.sub('\s+', '=', line.strip())
                            else:
                                resource_dict['Dict_Variables'] += re.sub('\s+', '=', line.strip())
                        elif line.startswith('*** Keywords ***'):
                            resource = models.Resource.objects.filter(Q(resource_name=file.name[:-6]) & Q(project=project_id))
                            if resource.count():
                                resource_dict['update_time']=datetime.datetime.now()
                                resource.update(**resource_dict)
                                resource_id = resource.first()
                                models.Keyword.objects.filter(resource=resource_id).delete()
                            else:
                                resource_id = models.Resource.objects.create(**resource_dict)
                        elif not line.startswith('   ') and not line.isspace():
                            i = 1
                            Table_value = {}
                            keyword_dict = {
                                'resource': resource_id,
                                'keyword_name': line.rstrip(),
                                'Documentation': '',
                                'Arguments': '',
                                'Teardown': '',
                                'Return_Value': '',
                                'Timeout': '',
                                'Tags': '',
                                'Table_value': '{}',
                            }
                        elif line.startswith('    [Arguments]'):
                            spot = 'Arguments'
                            keyword_dict['Arguments'] = re.split('^\s+\[Arguments\]\s+',line)[-1].replace('    ','|')
                        elif line.startswith('    [Documentation]'):
                            spot = 'Documentation'
                            keyword_dict['Documentation'] = line.split('    ')[2:]
                        elif line.startswith('    ...'):
                            if spot=='Arguments':
                                keyword_dict[spot] += '|'+re.split('^\s+\.\.\.\s+',line)[-1].replace('    ','|')
                            elif spot=='Documentation':
                                keyword_dict[spot] += line.split('    ')[2:]
                            else:
                                Table_list += line.split('    ')[2:]
                        elif line.startswith('    [Tags]'):
                            keyword_dict['Tags'] = re.split('^\s+\[Tags\]\s+',line)[-1].replace('    ','|')
                        elif line.startswith('    [Timeout]   '):
                            keyword_dict['Timeout'] = re.split('^\s+\[Timeout\]\s+',line)[-1].replace('    ','|')
                        elif line.startswith('    [Teardown]'):
                            keyword_dict['Teardown'] = re.split('^\s+\[Teardown\]\s+',line)[-1].replace('    ','|')
                        elif line.startswith('    [Return]'):
                            keyword_dict['Return_Value'] = re.split('^\s+\[Return\]\s+',line)[-1].replace('    ','|')

                        elif line.startswith('    '):
                            spot = False
                            if Table_list != []:
                                for j, value in enumerate(Table_list):
                                    k = str(i) + '-' + str(j + 1)
                                    Table_value[k] = value.rstrip()
                                i += 1
                            Table_list = line.split('    ')[1:]

                        else:
                            if Table_list != [] and Table_list:
                                for j, value in enumerate(Table_list):
                                    k = str(i) + '-' + str(j + 1)
                                    Table_value[k] = value.rstrip()
                                i += 1
                                keyword_dict['Table_value']=json.dumps(Table_value)
                                keyword_dict['Documentation']=''.join(keyword_dict['Documentation'])
                                keyword = models.Keyword.objects.filter(Q(keyword_name=keyword_dict['keyword_name']) & Q(resource=resource_id))
                                if keyword.count():
                                    keyword_dict['update_time'] = datetime.datetime.now()
                                    keyword.update(**keyword_dict)
                                else:
                                    keyword_dict['create_time']=datetime.datetime.now()
                                    models.Keyword.objects.create(**keyword_dict)
                                Table_list = []
                    if Table_list != [] and Table_list:
                        for j, value in enumerate(Table_list):
                            k = str(i) + '-' + str(j + 1)
                            Table_value[k] = value.rstrip()
                        i += 1
                        keyword_dict['Table_value'] = json.dumps(Table_value)
                        print('Table_value------------------>',Table_value)
                        keyword_dict['Documentation'] = ''.join(keyword_dict['Documentation'])
                        keyword = models.Keyword.objects.filter(Q(keyword_name=keyword_dict['keyword_name'])&Q(resource=resource_id))
                        if keyword.count():
                            keyword_dict['update_time'] = datetime.datetime.now()
                            keyword.update(**keyword_dict)
                        else:
                            keyword_dict['create_time'] = datetime.datetime.now()
                            models.Keyword.objects.create(**keyword_dict)
                        Table_list = []
                except Exception as f:
                    error_list.append(f)
    if error_list!=[]:
        ret = {'status': False,'error':error_list}

    return HttpResponse(json.dumps(ret))


#查询操作
@check_login
def resource_select(request):
    project = request.GET.get('project')
    rowIds = request.GET.getlist('rowIds[]')
    rowIds = [int(row) for row in rowIds]
    project_pro = models.Project.objects.filter(id=project).first()
    resource_list = models.Resource.objects.filter(Q(project=project) | Q(project__in=eval(project_pro.pro2))).all()
    return render(request,'resource_select.html',{'resource_list':resource_list,'rowIds':rowIds})