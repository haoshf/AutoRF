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
from urllib.parse import urlencode
# f = os.path.dirname(__file__)
# work = os.path.dirname(os.path.dirname(f))
# os.chdir(work)

class SendRequests(object):
    def __init__(self):
        self.session = requests.session()

    def post_with_header(self, data, url, *header):

        jsonStr = 'headers'
        headers = {}
        for parameter in header:
            print(jsonStr + parameter)
            try:
                exec(jsonStr + parameter)
            except:
                print('Expression execute failed![',jsonStr + parameter,']')

        # headers = JsonModify().update_json('{}',*header)
        # headers = json.loads(headers)
        print('*******url：******:%s' % (url))
        print('*******请求参数：******:%s' % (data))
        #请求为列表时，处理
        if isinstance(data,list):
            if isinstance(data,dict):
                data = [json.loads(js) for js in data]
        else:
            if data != '':
                try:
                    data = json.loads(data)
                except Exception:
                    pass
        try:
            if 'application/json' in headers.values():
                r = self.session.post(url, headers = headers, json = data)
            else:
                r = self.session.post(url, headers = headers, data = data)
        except:
            traceback.print_exc()
            raise
        resultObj = r.text
        print("*******运行结果：********", resultObj)
        try:
            return json.loads(resultObj)
        except Exception:
            return resultObj

    def get_with_header(self, url, *header):

        jsonStr = 'headers'
        headers = {}
        for parameter in header:
            print(jsonStr + parameter)
            try:
                exec(jsonStr + parameter)
            except:
                print('Expression execute failed![',jsonStr + parameter,']')

        try:
            r = self.session.get(url, headers = headers)
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

    def upload_with_header(self, data, url,file, filename,filepath,*header):
        jsonStr = 'headers'
        headers = {}
        for parameter in header:
            print(jsonStr + parameter)
            try:
                exec(jsonStr + parameter)
            except:
                print('Expression execute failed![',jsonStr + parameter,']')
        data = json.loads(data)
        data[file] = (filename, open(filepath, 'rb').read())
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        headers['Content-Type'] = encode_data[1]


        print('*******请求参数：******:%s' % (data))
        try:
            r = self.session.post(url, headers = headers, data = data)
        except:
            traceback.print_exc()
            raise
        resultObj = r.text
        print("*******运行结果：********", resultObj)
        return json.loads(resultObj)

    def download_with_header(self, data, url,filepath, *header):
        print('*******url：******:%s' % (url))
        print('*******请求参数：******:%s' % (data))
        jsonStr = 'headers'
        headers = {}
        for parameter in header:
            print(jsonStr + parameter)
            try:
                exec(jsonStr + parameter)
            except:
                print('Expression execute failed![',jsonStr + parameter,']')
        if data == '':
            r = self.session.get(url, headers=headers)
        else:
            # 请求为列表时，处理
            if isinstance(data,list):
                if isinstance(data,dict):
                    data = [json.loads(js) for js in data]
            else:
                data = json.loads(data)
            try:
                r = self.session.post(url, headers=headers, json=data)
            except:
                traceback.print_exc()
                raise

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):  # 循环写入，chunk_size是文件大小
                f.write(chunk)
        return r.status_code