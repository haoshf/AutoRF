from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository import models
import datetime,json,time
from backend.forms import Suite,Suite_add
from utils.pagination import Pagination
from django.urls import reverse
from django.core.paginator import Paginator, Page
from utils.building import Building
from utils import parser
import os,codecs,platform
from django.db.models import Q
import re
from urllib.parse import urlencode
from ..auth.auth import check_login,check_ajax_login

#套件管理
def suite(request, *args, **kwargs):

    project_list = models.Project.objects.all()
    suite_name = request.GET.get('suite_name')
    project_id = request.GET.get('project')
    current_page = request.GET.get('p')
    per_page_count = request.GET.get('p_count')
    data = {
        'suite_name':'',
        'project':'',
        'p_count': ''
    }
    suite_list = models.Suite.objects
    if suite_name:
        suite_list = suite_list.filter(suite_name__startswith=suite_name)
        data['suite_name'] =suite_name
    if project_id:
        suite_list = suite_list.filter(project=project_id)
        data['project'] = int(project_id)

    if not per_page_count:
        per_page_count=10
    data['p_count'] = int(per_page_count)
    posts = Pagination(current_page,suite_list.count(),int(per_page_count))
    url = 'suite.html?%s&'%(urlencode(data))
    page_str = posts.page_str(url)
    return render(request, 'suite.html', {'suite_list': suite_list.order_by('suite_name').order_by('sort').all()[posts.start:posts.end],'project_list':project_list,'page_str':page_str,'data':data})

@check_login
def suite_add(request):
    if request.method == 'GET':
        form = Suite(request=request)
    else:
        form = Suite_add(request=request,data=request.POST)
        if form.is_valid():
            dic = {}
            dic['create_time'] = datetime.datetime.now()
            dic['project'] = models.Project.objects.filter(id=form.cleaned_data['project']).first()
            form.cleaned_data.pop('project')
            dic.update(form.cleaned_data)
            models.Suite.objects.create(**dic)
            return redirect('/suite.html')
    return render(request, 'suite_add.html',{'form':form})

@check_login
def suite_edit(request,nid):

    obj = models.Suite.objects.filter(id=nid).first()
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
            'suite_name': obj.suite_name,
            'Documentation': obj.Documentation,
            'Suite_Setup': obj.Suite_Setup,
            'Suite_Teardown': obj.Suite_Teardown,
            'Test_Setup': obj.Test_Setup,
            'Test_Teardown': obj.Test_Teardown,
            'Test_Template':obj.Test_Template,
            'Force_Tags': obj.Force_Tags,
            'Default_Tags': obj.Default_Tags,
            'Library': obj.Library,
            'Resource': resource,
            'Variables':obj.Variables,
            'Scalar_Variables':obj.Scalar_Variables,
            'List_Variables': obj.List_Variables,
            'Dict_Variables': obj.Dict_Variables,
            'sort':obj.sort,
        }
        form = Suite(request=request, data=init_dict)
        return render(request, 'suite_edit.html', {'form': form, 'nid': nid,'resource_list':pro_res,'rowIds':rowIds})
    else:
        form = Suite(request=request,data=request.POST)
        if form.is_valid():
            if form.cleaned_data['suite_name'] != obj.suite_name:
                form = Suite_add(request=request,data=request.POST)
            if form.is_valid():
                dic = {}
                dic['update_time'] = datetime.datetime.now()
                dic.update(form.cleaned_data)
                models.Suite.objects.filter(id=nid).update(**dic)
                return redirect('/suite.html')
    return render(request, 'suite_edit.html',{'form':form, 'nid': nid})

@check_ajax_login
def del_suite(request):

    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        models.Suite.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False

    return HttpResponse(json.dumps(ret))

#上传套件入库
@check_login
def up_suite(request):
    from types import FunctionType, MethodType
    project_id = request.POST.get('project')
    project = models.Project.objects.filter(id=project_id).first()
    file_json = json.loads(request.POST.get('filePath'))
    files = request.FILES.getlist('k3')
    print(files)
    if not os.path.exists('./robot/%s/'%project.project_name):
        os.makedirs('./robot/%s/'%project.project_name)
        os.makedirs('./robot/%s/suite'%project.project_name)
    elif not os.path.exists('./robot/%s/suite'%project.project_name):
        os.makedirs('./robot/%s/suite'%project.project_name)
    for file in files:
        if file.name == '__init__.robot':
            continue
        else:
            file_ = file_json[file.name].split('/')[:-1]
            if len(file_)<2:
                filePath = '-'.join(file_)
            else:
                filePath= '-'.join(file_[1:])
            print(filePath)
            if filePath:
                suite_sort = re.search("\d+",filePath)
                if suite_sort:
                    suite_name = filePath.replace(suite_sort[0],'')+'-'+file.name[:-6]
                    sort = int(suite_sort[0])
                else:
                    suite_name = filePath+'-'+file.name[:-6]
                    sort = 99
                print('sort',sort,suite_name)
            else:
                suite_sort = re.search("^\d+",file.name[:-6])
                if suite_sort:
                    suite_name = file.name[:-6].replace(suite_sort[0],'')
                    sort = int(suite_sort[0])
                else:
                    suite_name = file.name[:-6]
                    sort = 1
            filepath = './robot/%s/suite/%s.robot'%(project.project_name,suite_name)
            f = open(filepath, 'wb')
            for line in file.chunks():
                f.write(line)
            f.close()
            time.sleep(1)
            f = open(filepath, 'r',encoding='utf8')
            suite_id = models.Suite.objects.filter(Q(suite_name=suite_name)&Q(project=project_id)).first()

            suite_dict = {
                'project': project,
                'suite_name': suite_name,
                'Documentation': '',
                'Suite_Setup': '',
                'Suite_Teardown': '',
                'Test_Setup': '',
                'Test_Teardown': '',
                'Test_Template':'',
                'Force_Tags': '',
                'Default_Tags':'',
                'Library': [],
                'Resource': [],
                'Variables':'',
                'Scalar_Variables':'',
                'List_Variables': '',
                'Dict_Variables': '',
                'sort':sort,
            }
            Table_list = []
            Variables = False
            for line in f.readlines():
                print('--------->',line)
                if line.startswith('*** Settings ***'):
                    continue
                elif line.startswith('Documentation'):
                    suite_dict['Documentation']=line.split('    ')[-1]
                elif line.startswith('...'):
                    suite_dict['Documentation']+=line.split('    ')[-1]
                elif line.startswith('Suite Setup'):
                    suite_dict['Suite_Setup']=re.split('^Suite Setup\s+',line)[-1].replace('    ','|')
                elif line.startswith('Suite Teardown'):
                    suite_dict['Suite_Teardown'] = re.split('^Suite Teardown\s+',line)[-1].replace('    ','|')
                elif line.startswith('Test Setup'):
                    suite_dict['Test_Setup'] = re.split('^Test Setup\s+',line)[-1].replace('    ','|')
                elif line.startswith('Test Teardown'):
                    suite_dict['Test_Teardown'] = re.split('^Test Teardown\s+',line)[-1].replace('    ','|')
                elif line.startswith('Force Tags'):
                    suite_dict['Force_Tags'] = re.split('^Force Tags\s+',line)[-1].replace('    ','|')
                elif line.startswith('Default Tags'):
                    suite_dict['Default_Tags'] = re.split('^Default Tags\s+',line)[-1].replace('    ','|')
                elif line.startswith('Test Template'):
                    suite_dict['Test_Template'] = re.split('^Test Template\s+',line)[-1].replace('    ','|')
                elif line.startswith('Library'):
                    library_name = line.split(' ')[-1].split('/')[-1].replace('\n','')
                    Lib = models.Library.objects.filter(library_name=library_name).first()
                    suite_dict['Library'].append(str(Lib.id))
                elif line.startswith('Resource'):
                    print('Resource',line.split(' ')[-1].split('/')[-1][:-7].lstrip())
                    Lib = models.Resource.objects.filter(Q(resource_name=line.split(' ')[-1].split('/')[-1][:-7].lstrip())&(Q(project=project_id)|Q(project__in=eval(project.pro2)))).first()
                    suite_dict['Resource'].append(str(Lib.id))
                elif line.startswith('*** Variables ***'):
                    Variables = True
                elif line.startswith('$') and Variables:
                    if suite_dict['Scalar_Variables']:
                        suite_dict['Scalar_Variables']+='|'+re.sub('\s+','=',line.strip())
                    else:
                        suite_dict['Scalar_Variables'] += re.sub('\s+', '=', line.strip())
                elif line.startswith('@') and Variables:
                    if suite_dict['List_Variables']:
                        suite_dict['List_Variables']+='|'+re.sub('\s+','=',line.strip())
                    else:
                        suite_dict['List_Variables'] += re.sub('\s+', '=', line.strip())
                elif line.startswith('&') and Variables:
                    if suite_dict['Dict_Variables']:
                        suite_dict['Dict_Variables']+='|'+re.sub('\s+','=',line.strip())
                    else:
                        suite_dict['Dict_Variables'] += re.sub('\s+', '=', line.strip())
                elif line.startswith('*** Test Cases ***'):
                    Variables = False
                    t = 0
                    suite = models.Suite.objects.filter(Q(suite_name=suite_name)&Q(project=project_id))
                    if suite.count():
                        suite_dict['update_time']=datetime.datetime.now()
                        suite.update(**suite_dict)
                        suite_id = suite.first()
                        models.Testcase.objects.filter(suite=suite_id).delete()
                    else:
                        suite_id = models.Suite.objects.create(**suite_dict)
                elif not line.startswith('   ') and not line.isspace():
                    Table_list = []
                    i = 1
                    Table_value = {}
                    testcase_dict = {
                        'suite':suite_id,
                        'testcase_name': line.rstrip(),
                        'Documentation': '',
                        'Setup': '',
                        'Teardown': '',
                        'Template': '',
                        'Timeout': '',
                        'Tags': '',
                        'Table_value': '',
                        'sort':1
                    }
                elif line.startswith('    [Documentation]'):
                    Documentation = True
                    testcase_dict['Documentation'] = line.split('    ')[2:]
                elif line.startswith('    ...'):
                    if Documentation:
                        testcase_dict['Documentation'] += line.split('    ')[2:]
                    else:
                        Table_list += line.split('    ')[2:]
                elif line.startswith('    [Tags]'):
                    testcase_dict['Tags'] = re.split(r'^\s+\[Tags\]\s+',line)[-1].replace('    ','|')
                elif line.startswith('    [Setup]'):
                    testcase_dict['Setup'] = re.split(r'^\s+\[Setup\]\s+',line)[-1].replace('    ','|')
                elif line.startswith('    [Template]'):
                    testcase_dict['Template'] = re.split(r'^\s+\[Template\]\s+',line)[-1].replace('    ','|')
                elif line.startswith('    [Timeout]'):
                    testcase_dict['Timeout'] = re.split(r'^\s+\[Timeout\]\s+',line)[-1].replace('    ','|')
                elif line.startswith('    [Teardown]'):
                    testcase_dict['Teardown'] = re.split(r'^\s+\[Teardown\]\s+',line)[-1].replace('    ','|')

                elif line.startswith('    '):
                    Documentation = False
                    if Table_list != []:
                        for j, value in enumerate(Table_list):
                            k = str(i) + '-' + str(j + 1)
                            Table_value[k] = value.rstrip()
                        i += 1
                    Table_list = line.split('    ')[1:]
                else:
                    try:
                        print('Table_list',Table_list)
                        if Table_list != [] and Table_list:
                            for j, value in enumerate(Table_list):
                                k = str(i) + '-' + str(j + 1)
                                Table_value[k] = value.rstrip()
                            i += 1
                            testcase_dict['Table_value']=json.dumps(Table_value)
                            testcase_dict['Documentation']=''.join(testcase_dict['Documentation'])
                            t+=1
                            testcase_dict['sort']=t
                            if models.Testcase.objects.filter(testcase_name=testcase_dict['testcase_name']).count():
                                testcase_dict['update_time']=datetime.datetime.now()
                                models.Testcase.objects.filter(testcase_name=testcase_dict['testcase_name']).update(**testcase_dict)
                            else:
                                models.Testcase.objects.create(**testcase_dict)
                        Table_list = []

                    except Exception as f:
                        print('未发现用例！',f)
                        pass
            try:
                if Table_list != [] and Table_list:
                    for j, value in enumerate(Table_list):
                        k = str(i) + '-' + str(j + 1)
                        Table_value[k] = value.rstrip()
                    i += 1
                    t += 1
                    testcase_dict['sort'] = t
                    testcase_dict['Table_value'] = json.dumps(Table_value)
                    testcase_dict['Documentation'] = ''.join(testcase_dict['Documentation'])
                    if models.Testcase.objects.filter(testcase_name=testcase_dict['testcase_name']).count():
                        testcase_dict['update_time'] = datetime.datetime.now()
                        models.Testcase.objects.filter(testcase_name=testcase_dict['testcase_name']).update(**testcase_dict)
                    else:
                        models.Testcase.objects.create(**testcase_dict)
                Table_list = []
            except Exception as f:
                print('未发现用例！', f)
                pass

    return redirect('/')