# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
from repository import models
import datetime

def parser(category="all"):

    USER_KEYS = {
        "web": ["BuiltIn", "Collections", "String", "DateTime", "Screenshot", "SeleniumLibrary"],
        "app": ["BuiltIn", "Collections", "String", "DateTime", "Screenshot", "AppiumLibrary"],
        "http": ["BuiltIn", "Collections", "String", "DateTime", "RequestsLibrary"],
        "all": ["BuiltIn", "Collections", "String", "Screenshot", "DateTime",
                "SeleniumLibrary", "AppiumLibrary",
                "Process", "OperatingSystem"]
    }

    cwd = os.getcwd() + "/keyword"
    for k in USER_KEYS[category]:
        path = cwd + "/%s.xml" % k
        tree = ET.parse(path)
        root = tree.getroot()
        name = root.attrib["name"]
        children = []
        dic = {
            'library_name': name,
            'documentation': '',
            'class_name': name,
            'filepath': name
        }
        if not models.Library.objects.filter(library_name=name).count():
            dic['create_time'] = datetime.datetime.now()
            library_id=models.Library.objects.create(**dic)
        else:
            library_id = models.Library.objects.filter(library_name=name).first()
        for kw in root.iter("kw"):
            # 关键字
            keyword = kw.attrib["name"]

            # 关键字参数
            params = []
            for arg in kw.iter("arg"):
                params.append(arg.text)

            # 使用说明
            doc = kw.find("doc").text
            if not doc:
                doc=''
            dic = {
                'library': library_id,
                'method_name': keyword,
                'documentation': doc,
                'Arguments': params,
                'Return_Value': '',
                'create_time': datetime.datetime.now()
            }
            if not models.Method.objects.filter(method_name=keyword).count():
                models.Method.objects.create(**dic)
    return  '初始化完成！'