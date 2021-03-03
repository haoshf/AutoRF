#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
import json

def check_login(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login.html')
    return inner

def check_ajax_login(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            ret = {'status': None}
            return HttpResponse(json.dumps(ret))
    return inner