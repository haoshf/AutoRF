# coding=utf-8
import json


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