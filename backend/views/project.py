from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository import models
import datetime,json,time,os
from backend.forms import Project,Project_add,Smtp
from utils.pagination import Pagination
from django.urls import reverse
from django.core.paginator import Paginator, Page
from ..auth.auth import check_login,check_ajax_login

#项目管理
def project(request):
    project_list = models.Project.objects.all()
    return render(request,'project.html',{'project_list': project_list})

@check_login
def project_add(request):

    if request.method == 'GET':
        form = Project_add(request=request)
    else:
        form = Project_add(request=request,data=request.POST)
        if form.is_valid():
            dic = {}
            dic['create_time'] = datetime.datetime.now()
            dic.update(form.cleaned_data)
            models.Project.objects.create(**dic)
            return redirect('/project.html')
    return render(request, 'project_add.html',{'form':form})

@check_login
def project_edit(request,nid):

    obj = models.Project.objects.filter(id=nid).first()
    if request.method == 'GET':
        if not obj:
            return render(request, 'backend_no_article.html')
        resource = obj.Resource
        resource_list = eval(resource)
        print('______',resource_list)
        if resource_list != [] and resource_list:
            resource = models.Resource.objects.filter(id__in=resource_list).values_list('id','resource_name')
            if resource:
                resource = list(zip(*resource))[0]
        library = obj.Library
        library_list = eval(library)
        if library_list != [] and library_list:
            library = models.Library.objects.filter(id__in=library_list).values_list('id','library_name')
            if library:
                library = list(zip(*library))[0]
        init_dict = {
            'id': obj.id,
            'project_name': obj.project_name,
            'Documentation': obj.Documentation,
            'Suite_Setup': obj.Suite_Setup,
            'Suite_Teardown': obj.Suite_Teardown,
            'Test_Setup': obj.Test_Setup,
            'Test_Teardown': obj.Test_Teardown,
            'Force_Tags': obj.Force_Tags,
            'Library': library,
            'Resource': resource,
            'Variables':obj.Variables,
            'Scalar_Variables':obj.Scalar_Variables,
            'List_Variables': obj.List_Variables,
            'Dict_Variables': obj.Dict_Variables,
        }
        form = Project(request=request, data=init_dict)
        return render(request, 'project_edit.html', {'form': form, 'nid': nid})
    else:
        form = Project(request=request, data=request.POST)

        if form.is_valid():
            if form.cleaned_data['project_name'] != obj.project_name:
                form = Project_add(request=request, data=request.POST)
            if form.is_valid():
                dic = {}
                dic['update_time'] = datetime.datetime.now()
                dic.update(form.cleaned_data)
                models.Project.objects.filter(id=nid).update(**dic)
                if dic['project_name'] != obj.project_name and os.path.exists('./robot/%s/'%obj.project_name):
                    os.rename('./robot/%s/'%obj.project_name,'./robot/%s/'%dic['project_name'])
                return redirect('/project.html')
    return render(request, 'project_edit.html',{'form':form, 'nid': nid})

@check_ajax_login
def del_project(request):

    ret = {'status': True}
    try:
        nid = request.POST.getlist('nid[]')
        models.Project.objects.filter(id__in=nid).delete()
    except Exception as e:
        ret['status'] = False

    return HttpResponse(json.dumps(ret))

@check_login
def project_smpt(request,nid):

    user = request.session.get('user_info')
    userInfo = models.UserInfo.objects.filter(id=user['id']).first()
    project = models.Project.objects.filter(id=nid).first()
    print(project)
    obj = models.Smtp.objects.filter(project_name=nid).first()
    if request.method == 'GET':
        if not obj:
            init_dict = {
                'project_name': project.id,
                'enable':True,
            }
            form = Smtp(request=request, data=init_dict)
            return render(request, 'project_smpt.html', {'form': form,'nid':nid})
        init_dict = {
            'project_name': project.id,
            'mail_host': obj.mail_host,
            'mail_user': obj.mail_user,
            'mail_pass': obj.mail_pass,
            'receivers': obj.receivers,
            'cc': obj.cc,
            'enable': obj.enable,
            'title': obj.title,
            'documentation': obj.documentation,
        }
        form = Smtp(request=request, data=init_dict)
        return render(request, 'project_smpt.html', {'form': form,'nid': nid})
    else:
        form = Smtp(request=request, data=request.POST)
        if form.is_valid():
            dic = {}
            if not obj:
                dic['create_time'] = datetime.datetime.now()
                dic.update(form.cleaned_data)
                dic['project_name'] = project
                dic['user'] = userInfo
                models.Smtp.objects.create(**dic)
            else:
                dic['update_time'] = datetime.datetime.now()
                dic.update(form.cleaned_data)
                dic['project_name'] = project
                dic['user'] = userInfo
                models.Smtp.objects.filter(project_name=nid).update(**dic)
            return redirect('/project.html')
    return render(request, 'project_smpt.html',{'form':form, 'nid': nid})