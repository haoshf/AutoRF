# coding=utf-8
import json
from urllib.parse import urlencode
from urllib.parse import unquote
from bs4 import BeautifulSoup
import copy

class JsonModify(object):
    def __init__(self):
        pass


    def update_json(self,url,*parameters):
        """
        格式化json
        :param url:传入地址或url,读取或者重拼json
        :param parameters:
        :return:
        """
        try:
            if isinstance(url,dict):
                jsonStr = url
            else:
                jsonStr = json.loads(url)
        except Exception:
            json_Str = open(url).read()
            json_Str = json_Str.replace('\t', '').replace('\n', '')
            jsonStr = json.loads(json_Str)
        strDict = 'jsonStr'
        for parameter in parameters:
            print(strDict + parameter)
            try:
                exec(strDict + parameter)
            except:
                print('Expression execute failed![',strDict + parameter,']')
        print('++++++++++++++++',type(jsonStr))
        print('++++++++++++++++', jsonStr)
        return json.dumps(jsonStr)

    def del_json(self,url,*parameters):
        """
        删除json中的key,value
        :param url:传入地址或url,读取或者重拼json
        :param parameters:
        :return:
        """
        try:
            if isinstance(url,dict):
                jsonStr = url
            else:
                jsonStr = json.loads(url)
        except Exception:
            json_Str = open(url).read()
            json_Str = json_Str.replace('\t', '').replace('\n', '')
            jsonStr = json.loads(json_Str)
        print(type(jsonStr))
        for parameter in parameters:
            jsonStr.pop(parameter)
        return json.dumps(jsonStr)

    def load_js(self,mes):
        return json.loads(mes)

    def dump_js(self,mes):
        return json.dumps(mes, ensure_ascii=False)

    def url_encode(self,data):
        return urlencode(data)

    def url_decode(self,data):
        return unquote(data)

    def soup_mes(self,html,kw):
        soup = BeautifulSoup(html,features="lxml")
        return soup.select(kw)[0].get_text()

    def js_foo(self,L, key, value):
        for k, v in value.items():
            s1 = copy.copy(key)
            s1 += '[%s]' % k
            if isinstance(v, dict):
                self.js_foo(L, s1, v)
            elif isinstance(v, list):
                for i, v1 in enumerate(v):
                    s2 = copy.copy(s1)
                    s2 += '[%s]' % str(i)
                    if isinstance(v1, dict):
                        self.js_foo(L, s2, v1)
                    else:
                        L[s2]=v1
                        # string = '%s:%s' % (s2, v1)
                        # L.append(string)
            else:
                L[s1] = v
                # string = '%s:%s' % (s1, v)
                # L.append(string)
        return L

    def json_url(self,json_data):
        print('***请求的json***',json_data)
        L = {}
        for key, value in json_data.items():
            s1 = key
            if isinstance(value, dict):
                self.js_foo(L, s1, value)
            elif isinstance(value, list):
                for i, v1 in enumerate(value):
                    s2 = copy.copy(s1)
                    s2 += '[%s]' % str(i)
                    if isinstance(v1, dict):
                        self.js_foo(L, s2, v1)
            else:
                L[s1] = value
                # string = '%s:%s' % (s1, value)
                # L.append(string)
        # parms = '&'.join(L)
        return L
