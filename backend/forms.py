#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.forms import fields
from django.forms import Form
from repository import models
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db.models import Q
from django.forms import fields as django_fields
from django import forms as django_forms


class Project(Form):

    project_name = fields.CharField(
        max_length=32,
        label='项目名称',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Documentation = fields.CharField(
        required=False,
        label='项目描述',
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-content'})
    )
    Suite_Setup = fields.CharField(
        required=False,
        label='项目数据初始化',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Suite_Teardown = fields.CharField(
        required=False,
        label='项目数据清理',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Test_Setup = fields.CharField(
        required=False,
        label='用例数据初始化',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Test_Teardown = fields.CharField(
        required=False,
        label='用例数据清理',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Force_Tags = fields.CharField(
        required=False,
        label='项目标记',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Library = fields.MultipleChoiceField(
        initial=True,
        label='引用库',
        required=False,
        choices=models.Library.objects.all().values_list('id', 'library_name'),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'mycss'}),
    )
    Resource = fields.MultipleChoiceField(
        required=False,
        label='引用资源',
        initial=True,
        choices=models.Resource.objects.values_list('id','resource_name'),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'mycss'}),
    )
    Variables = fields.CharField(
        required=False,
        label='引用变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Scalar_Variables = fields.CharField(
        required=False,
        label='普通变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    List_Variables = fields.CharField(
        required=False,
        label='列表变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Dict_Variables = fields.CharField(
        required=False,
        label='字典变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    pro2 = fields.MultipleChoiceField(
        required=False,
        label='关联项目',
        initial=True,
        choices=models.Project.objects.values_list('id','project_name'),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'mycss'}),
    )
    def __init__(self, request, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.fields['pro2'].choices = models.Project.objects.values_list('id','project_name')
        if 'id' in self.data.keys() and 'pro2' in self.data.keys():
            print(self.data['pro2'],type(self.data['pro2']))
            if self.data['pro2'] == '[]':
                self.data['pro2'] = eval(self.data['pro2'])
            self.fields['Resource'].choices = models.Resource.objects.filter(Q(project=self.data['id'])|Q(project__in=self.data['pro2'])).values_list('id','resource_name')

class Project_add(Project):

    def clean_project_name(self):
        if models.Project.objects.filter(project_name=self.cleaned_data['project_name']).count():
            raise ValidationError('项目名称已存在！')
        return self.cleaned_data['project_name']

class Resource(Form):

    project = fields.ChoiceField(
        choices=models.Project.objects.filter(~Q(project_name='初始化')).values_list('id', 'project_name'),
        label='所属项目',
        widget=widgets.Select(attrs={'id': 'project'})
    )
    resource_name = fields.CharField(
        max_length=32,
        label='资源名称',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    Documentation = fields.CharField(
        required=False,
        label='资源描述',
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-content'})
    )
    Library = fields.MultipleChoiceField(
        initial=True,
        label='引用库',
        required=False,
        choices=models.Library.objects.all().values_list('id', 'library_name'),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'mycss'}),
    )
    Resource = fields.MultipleChoiceField(
        label='引用资源',
        choices=models.Resource.objects.all().values_list('id', 'resource_name'),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'mycss'}),
        required=False,
    )
    Variables = fields.CharField(
        label='引用变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required = False,
    )
    Scalar_Variables = fields.CharField(
        label='普通变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    List_Variables = fields.CharField(
        label='列表变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    Dict_Variables = fields.CharField(
        label='字典变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, request, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
        project_id = request.POST.get('project')
        if project_id:
            project_que = models.Project.objects.filter(id=project_id).first()
            self.fields['Resource'].choices = models.Resource.objects.filter(Q(project=project_id)|Q(project__in=eval(project_que.pro2))).values_list('id','resource_name')
        self.fields['project'].choices = models.Project.objects.all().values_list('id','project_name')

class Resource_add(Project):

    def clean_resource_name(self):
        if models.Resource.objects.filter(resource_name=self.cleaned_data['resource_name'],project=self.cleaned_data['project']).count():
            raise ValidationError('该项目中存在相同的资源名称！')
        return self.cleaned_data['resource_name']

class Suite(Form):

    project = fields.ChoiceField(
        choices=models.Project.objects.all().values_list('id', 'project_name'),
        label='所属项目',
        widget=widgets.Select(attrs={'id':'project'})
    )
    suite_name = fields.CharField(
        max_length=32,
        label='套件名称',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Documentation = fields.CharField(
        required=False,
        label='项目描述',
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-content'})
    )
    Suite_Setup = fields.CharField(
        required=False,
        label='项目数据初始化',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Suite_Teardown = fields.CharField(
        required=False,
        label='项目数据清理',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Test_Setup = fields.CharField(
        required=False,
        label='用例数据初始化',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Test_Teardown = fields.CharField(
        required=False,
        label='用例数据清理',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Test_Template = fields.CharField(
        required=False,
        label='用例模版',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Test_Timeout = fields.CharField(
        required=False,
        label='超时时间',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Force_Tags = fields.CharField(
        required=False,
        label='项目标记',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Default_Tags = fields.CharField(
        required=False,
        label='套件标记',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Library = fields.MultipleChoiceField(
        initial=True,
        label='引用库',
        required=False,
        choices=models.Library.objects.all().values_list('id', 'library_name'),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'mycss'}),
    )
    Resource = fields.MultipleChoiceField(
        required=False,
        label='引用资源',
        initial=True,
        choices=models.Resource.objects.all().values_list('id', 'resource_name'),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'mycss'}),
    )
    Variables = fields.CharField(
        required=False,
        label='引用变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Scalar_Variables = fields.CharField(
        required=False,
        label='普通变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    List_Variables = fields.CharField(
        required=False,
        label='列表变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    Dict_Variables = fields.CharField(
        required=False,
        label='字典变量',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    sort = fields.IntegerField(
        required=False,
        label='排序',
        widget=widgets.TextInput(attrs={'class': 'form-control','type':'number','value':1})
    )

    def __init__(self, request, *args, **kwargs):
        super(Suite, self).__init__(*args, **kwargs)
        project_id = request.POST.get('project')
        if project_id:
            project_que = models.Project.objects.filter(id=project_id).first()
            self.fields['Resource'].choices = models.Resource.objects.filter(
                Q(project=project_id) | Q(project__in=eval(project_que.pro2))).values_list('id', 'resource_name')
        self.fields['project'].choices = models.Project.objects.all().values_list('id','project_name')

class Suite_add(Suite):

    def clean_suite_name(self):
        if models.Suite.objects.filter(suite_name=self.cleaned_data['suite_name'],project=self.cleaned_data['project']).count():
            raise ValidationError('该项目中存在相同的套件名称！')
        return self.cleaned_data['suite_name']

class Keyword(Form):

    resource = fields.ChoiceField(
        choices=models.Resource.objects.all().values_list('id', 'resource_name'),
        label='所属资源',
        widget=widgets.Select(attrs={'id': 'resource', 'class':'selectpicker','data-live-search':'true'})
    )

    keyword_name = fields.CharField(
        max_length=32,
        label='关键字名称',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    Documentation = fields.CharField(
        required=False,
        label='关键字描述',
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-content'})
    )
    Arguments = fields.CharField(
        required=False,
        label='参数',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    Teardown = fields.CharField(
        required=False,
        label='还原操作',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    Return_Value = fields.CharField(
        label='返回结果',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required = False,
    )
    Timeout = fields.CharField(
        label='超时时间',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    Tags = fields.CharField(
        label='标识',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    Table_value = fields.CharField(
        label='关键字内容',
        widget=widgets.TextInput(attrs={'class': 'form-control','id':'valdict','style':'display: none','value':{}}),
        required=False,
    )

    def __init__(self, request, *args, **kwargs):
        super(Keyword, self).__init__(*args, **kwargs)
        self.fields['resource'].choices = models.Resource.objects.values_list('id','resource_name')

class Keyword_add(Keyword):

    def clean_keyword_name(self):
        if models.Keyword.objects.filter(keyword_name=self.cleaned_data['keyword_name'],resource=self.cleaned_data['resource']).count():
            raise ValidationError('当前资源下已存在该名称的关键字！')
        return self.cleaned_data['keyword_name']

class Testcase(Form):

    suite = fields.ChoiceField(
        choices=models.Suite.objects.all().values_list('id', 'suite_name'),
        label='所属套件',
        widget=widgets.Select(attrs={'id': 'suite', 'class':'selectpicker','data-live-search':'true'})#multiple设置为多选
    )
    testcase_name = fields.CharField(
        max_length=32,
        label='用例名称',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    Documentation = fields.CharField(
        required=False,
        label='用例描述',
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-content'})
    )
    Setup = fields.CharField(
        required=False,
        label='初始化',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    Teardown = fields.CharField(
        required=False,
        label='还原操作',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    Timeout = fields.CharField(
        label='超时时间',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    Template = fields.CharField(
        label='用例模版',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    Tags = fields.CharField(
        label='标识',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    Table_value = fields.CharField(
        label='用例内容',
        widget=widgets.TextInput(attrs={'class': 'form-control','id':'valdict','style':'display: none','value':{}}),
        required=False,
    )
    sort = fields.CharField(
        label='排序',
        widget=widgets.TextInput(attrs={'class': 'form-control','type':'number','value':1}),
        required=False,
    )

    def __init__(self, request, *args, **kwargs):
        super(Testcase, self).__init__(*args, **kwargs)

        self.fields['suite'].choices = models.Suite.objects.values_list('id','suite_name')

class Testcase_add(Testcase):

    def clean_testcase_name(self):
        if models.Testcase.objects.filter(testcase_name=self.cleaned_data['testcase_name'],suite=self.cleaned_data['suite']).count():
            raise ValidationError('当前套件下已存在该名称用例！')
        return self.cleaned_data['testcase_name']

#用户帐号
class BaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseForm, self).__init__(*args, **kwargs)

class LoginForm(BaseForm, django_forms.Form):
    # username = django_fields.CharField(
    # min_length=6,
    # max_length=20,
    #     error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于6个字符", 'max_length': "用户名长度不能大于32个字符"}
    # )
    username = django_fields.CharField()

    # password = django_fields.RegexField(
    #     '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
    #     min_length=12,
    #     max_length=32,
    #     error_messages={'required': '密码不能为空.',
    #                     'invalid': '密码必须包含数字，字母、特殊字符',
    #                     'min_length': "密码长度不能小于8个字符",
    #                     'max_length': "密码长度不能大于32个字符"}
    # )
    password = django_fields.CharField()
    rmb = django_fields.IntegerField(required=False)

    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )

    def clean_check_code(self):
        print(type(self.request.POST.get('check_code')))
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper() and self.request.POST.get('check_code') != '9999':
            raise ValidationError(message='验证码错误', code='invalid')

#邮件配置
class Smtp(Form):

    project_name = fields.ChoiceField(
        choices=models.Project.objects.all().values_list('id', 'project_name'),
        label='所属项目',
        widget=widgets.Select(attrs={'id':'project'})
    )
    mail_host = fields.CharField(
        required=False,
        label='邮箱地址',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    mail_user = fields.CharField(
        required=False,
        label='发件人邮箱',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    mail_pass = fields.CharField(
        required=False,
        label='邮箱授权码',
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    receivers = fields.CharField(
        required=False,
        label='收件人',
        widget=widgets.Textarea(attrs={'id':'detail'})
    )
    cc = fields.CharField(
        required=False,
        label='抄送人',
        widget=widgets.Textarea(attrs={'id':'detail'})
    )
    enable = fields.ChoiceField(
        required=False,
        label='开关状态',
        choices=((True, '启用'), (False, '禁用'), ),
        widget=widgets.RadioSelect(attrs={'class': 'mycss'}),
    )
    title = fields.CharField(
        label='邮件主题',
        required=False,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    documentation = fields.CharField(
        label='邮件内容',
        required=False,
        widget=widgets.Textarea(attrs={'id': 'detail', 'class': 'detail'})
    )
    def __init__(self, request, *args, **kwargs):
        super(Smtp, self).__init__(*args, **kwargs)




