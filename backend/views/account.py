#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from io import BytesIO
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from utils.check_code import create_validate_code
from repository import models
from backend.forms import LoginForm
from django.core import serializers


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects. \
                filter(username=username, password=password). \
                values('id', 'nickname').first()

            if not user_info:
                # result['message'] = {'__all__': '用户名或密码错误'}
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            print(form.errors)
            if 'check_code' in form.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))



def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.clear()

    return redirect('/')


def get_userinfo(request):
    ret = {'status': False, 'mes': {}}
    try:
        user_id = request.GET.get('nid')
        ret['status'] = True
        userinfo = serializers.serialize("json", models.UserInfo.objects.filter(id=user_id).all())
        project = serializers.serialize("json", models.Project.objects.filter().all())
        ret['mes']['userinfo'] = json.loads(userinfo)[0]['fields']
        ret['mes']['project'] = json.loads(project)
    except Exception as e:
        print(e, type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))

def saveUserInfo(request):
    """
    修改用户信息
    :param request:
    :return:
    """

    ret = {'status': False, 'mes': False}
    try:
        # userId = request.POST.get('id')
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # nickname = request.POST.get('nickname')
        # email = request.POST.get('email')
        # project_msg = request.POST.getlist('project_msg')
        # print(project_msg)
        user = json.loads(request.body)
        user_obj = models.UserInfo.objects.filter(id=user['id'])
        userInfo = {
            'username':user['username'],
            'password': user['password'],
            'nickname': user['nickname'],
            'email': user['email'],
            'projectAccount': json.dumps(user['projectAccount']),
            'avatar': user_obj.first().avatar
        }
        user_obj.update(**userInfo)
        user_info = models.UserInfo.objects. \
            filter(username=user_obj.first().username). \
            values('id', 'nickname').first()
        request.session['user_info'] = user_info
        ret['status'] = True

    except Exception as e:
        print(e, type(e))
        ret['mes'] = str(e)
    return HttpResponse(json.dumps(ret))