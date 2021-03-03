#!/usr/bin/env python
# coding=utf-8
__author__ = 'haoshuaifei'
import base64
import json
import requests
import traceback
import os
from urllib3 import encode_multipart_formdata
from requests.auth import AuthBase
from JsonModify import JsonModify
# f = os.path.dirname(__file__)
# work = os.path.dirname(os.path.dirname(f))
# os.chdir(work)

class SendRequests(object):
    def __init__(self):
        self.cookiestr = ''

    def post_with_header(self, data, url, *header):

        headers = JsonModify().update_json('{}',*header)
        print('*******url：******:%s' % (url))
        print('*******请求头：******:%s' % (headers))
        print('*******请求参数：******:%s' % (data))
        headers = json.loads(headers)

        #请求为列表时，处理
        if isinstance(data,list):
            if isinstance(data,dict):
                data = [json.loads(js) for js in data]
            # else:
            #     print('*******请求参数：******:%s' % (data))
            #     resultObj = requests.post(url, headers = headers, json = data).text
            #     print("*******运行结果：********", resultObj)
            #     return json.loads(resultObj)
        else:
            if data != '':
                data = json.loads(data)

        if headers.__len__() == 0:
            r = requests.post(url, json = data,verify=False)
            resultObj = r.text
            return json.loads(resultObj)
        else:
            try:
                r = requests.post(url, headers = headers, json = data)
            except:
                traceback.print_exc()
                raise
            resultObj = r.text
            print("*******运行结果：********", resultObj)
            return json.loads(resultObj)

    def append_thing(self, parameter):
        if (parameter.find('.append') != -1 & parameter.find(": ''") != -1):
            return False
        else:
            return True

    def base64_conversion(self, pwd):
        print(pwd,type(pwd))
        pwd = base64.b64encode(pwd.encode('utf-8'))# 密码
        return pwd

    def get_with_header(self, url, *header):
        headers = {}
        strDict = 'headers'
        # headers['Cookie'] = self.cookiestr
        for parameter in header:
            exec (strDict + parameter)
        if headers.__len__() == 0:
            r = requests.get(url)
            resultObj = r.text
            return json.loads(resultObj)
        else:
            try:
                r = requests.get(url, headers = headers)
            except:
                traceback.print_exc()
                raise
            resultObj = r.text
            print('url',url)
            print('headers',headers)
            print("*******运行结果：********", resultObj)
            try:
                return json.loads(resultObj)
            except Exception:
                return resultObj

    def upload_with_header(self, data, url, filename,filepath,*header):
        headers = {}
        strDict = 'headers'
        for parameter in header:
            exec (strDict + parameter)
        data = json.loads(data)
        data['file'] = (filename, open(filepath, 'rb').read())
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        headers['Content-Type'] = encode_data[1]

        if headers.__len__() == 0:
            r = requests.post(url, data = data)
            resultObj = r.text
            return json.loads(resultObj)
        else:
            print('*******请求参数：******:%s' % (data))
            try:
                r = requests.post(url, headers = headers, data = data)
            except:
                traceback.print_exc()
                raise
            resultObj = r.text
            print("*******运行结果：********", resultObj)
            return json.loads(resultObj)

    def Auth(self, url,username,password):

        r = requests.post(url,auth=(username,password))
        return json.loads(r.text)

    def download_with_header(self, data, url,filepath, *header):
        print('*******url：******:%s' % (url))
        print('*******请求参数：******:%s' % (data))
        headers = JsonModify().update_json('{}',*header)
        headers = json.loads(headers)
        if data == '':
            r = requests.get(url, headers=headers)
        else:
            # 请求为列表时，处理
            if isinstance(data,list):
                if isinstance(data,dict):
                    data = [json.loads(js) for js in data]
            else:
                data = json.loads(data)
            try:
                r = requests.post(url, headers=headers, json=data)
            except:
                traceback.print_exc()
                raise

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):  # 循环写入，chunk_size是文件大小
                f.write(chunk)
        return r.status_code