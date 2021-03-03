import json


class Application(object):
    def __init__(self):

        self.app_mes = {
            '该应用是否免费': 'freeFlag',
            '应用程序名称': 'name',
            '应用描述': 'description',
            '应用图标': 'icon',
            '版本': 'version',
            '开发者信息': 'developer',
            '手机号': 'mobile',
            '应用类型': 'funcType',
            'PC端URL': 'menuUrl',
            '移动端URL': 'appUrl',
            'actionKey': 'actionKey',
            '规格版本': 'version',
            '使用人数': 'useNumber',
            '周期': 'cycle',
            '版本升级': 'addFlag',
            '分类':'platformGroupId',
        }

    def add_app(self, **kwargs):

        app_mes = self.app_mes
        app_dict = {
            "applicationDO": {
                "description": "描述",
                "funcDO": {
                    "appUrl": "http://baidu.com",
                    "actionKey": "http://baidu.com",
                    "funcType": "external",
                    "menuUrl": "http://baidu.com"
                },
                "icon": "/bp/0/2020-07-27/2c02d26d02b94c808ba11e61d89c6b02.jpg",
                "name": "付费应用",
                "isCommon": 0,
                "funcId": ""
            },
            "freeFlag": 0,
            "developer": "开发者",
            "expireEndDay": "",
            "expireStartDay": "",
            "mobile": "13938863072",
            "price": "",
            "sellStatus": 0,
            "version": "1.10",
            "addFlag": 1
            # "applicationVersionSpecs": "{\"version\":[\"1\"],\"useNumber\":[\"2\"],\"cycle\":[\"3\"]}",
            # "applicationVersionSpecDOList": [
            #     {
            #         "applicationSpecs": {
            #             "version": "1",
            #             "useNumber": "2",
            #             "cycle": "3"
            #         },
            #         "price": 0.01,
            #         "showFlag": 1
            #     }
            # ]
        }
        applicationVersionSpecs = {'version': [], 'useNumber': [], 'cycle': []}

        for key, value in kwargs.items():
            if value == '是': value = 1
            if value == '否': value = 0
            if key == '应用程序类别':
                app_dict['applicationDO']['funcId'] = value['funcId']
                app_dict['applicationDO']['name'] = value['funcName']

            elif key in ['应用程序名称', '应用描述', '应用图标']:
                if key == '应用图标':
                    value = value['data']['fileName']
                app_dict['applicationDO'][app_mes[key]] = value

            elif key in ['应用类型', 'PC端URL', '移动端URL', 'actionKey']:
                if key == '应用类型':
                    value = 'external' if value == '外部应用' else 'app'

                app_dict['applicationDO']['funcDO'][app_mes[key]] = value

            elif key in ['规格版本', '使用人数', '周期']:
                applicationVersionSpecs[app_mes[key]] = value

            elif key == '价格':
                price = value

            elif key == '是否显示该规格':
                showFlag = value

            else:
                app_dict[app_mes[key]] = value

        if app_dict['freeFlag'] == 0:
            app_dict['applicationVersionSpecs'] = json.dumps(applicationVersionSpecs)
            applicationVersionSpecDOList = []
            a = 0
            for version in applicationVersionSpecs['version']:
                for useNumber in applicationVersionSpecs['useNumber']:
                    for cycle in applicationVersionSpecs['cycle']:
                        applicationVersion = {'applicationSpecs': {}}
                        applicationVersion['applicationSpecs']['version'] = version
                        applicationVersion['applicationSpecs']['useNumber'] = useNumber
                        applicationVersion['applicationSpecs']['cycle'] = cycle
                        applicationVersion['price'] = price[a] if a < len(price) else 0.01
                        applicationVersion['showFlag'] = showFlag[a] if a < len(showFlag) else 1
                        applicationVersionSpecDOList.append(applicationVersion)
                        a += 1

            app_dict['applicationVersionSpecDOList'] = applicationVersionSpecDOList

        return json.dumps(app_dict)


    def up_app(self,detail,**kwargs):

        app_mes = self.app_mes
        app_dict = {
            "applicationDO": {
                "description": detail['description'],
                "funcDO": detail['funcDO'],
                "icon": detail['icon'],
                "name": detail['name'],
                "isCommon": detail['isCommon'],
                "funcId": detail['funcId'],
                "applicationId": detail['applicationId'],
            },
            "freeFlag": detail['freeFlag'],
            "developer": detail['developer'],
            "expireEndDay": detail['expireEndDay'],
            "expireStartDay": detail['expireStartDay'],
            "mobile": detail['mobile'],
            "price": detail['price'],
            "sellStatus": detail['sellStatus'],
            "version": detail['version'],
            "addFlag": 1,
            "applicationVersionSpecDOList": [],
            "platformGroupId": detail['platformGroupId'],
            "applicationVersionId": detail['applicationVersionId'],
        }
        if app_dict['freeFlag'] == 1:
            applicationVersionSpecs = {'version': [], 'useNumber': [], 'cycle': []}
        else:
            applicationVersionSpecs = detail['applicationVersionSpecs']


        for DOList in detail['applicationVersionSpecDOList']:

            SpecDOList = {}
            SpecDOList['applicationSpecs'] = json.loads(DOList['applicationSpecs'])
            SpecDOList['price'] = DOList['price']
            SpecDOList['showFlag'] = DOList['showFlag']
            app_dict['applicationVersionSpecDOList'].append(SpecDOList)

        for key, value in kwargs.items():
            if value == '是': value = 1
            if value == '否': value = 0
            if key == '应用程序类别':
                app_dict['applicationDO']['funcId'] = value['funcId']
                app_dict['applicationDO']['name'] = value['funcName']

            elif key in ['应用程序名称', '应用描述', '应用图标']:
                if key == '应用图标':
                    value = value['data']['fileName']
                app_dict['applicationDO'][app_mes[key]] = value

            elif key in ['应用类型', 'PC端URL', '移动端URL', 'actionKey']:
                if key == '应用类型':
                    value = 'external' if value == '外部应用' else 'app'

                app_dict['applicationDO']['funcDO'][app_mes[key]] = value

            elif key in ['规格版本', '使用人数', '周期']:
                applicationVersionSpecs[app_mes[key]] = value

            elif key == '价格':
                price = value

            elif key == '是否显示该规格':
                showFlag = value

            else:
                app_dict[app_mes[key]] = value

        if app_dict['freeFlag'] == 0:
            if isinstance(applicationVersionSpecs,dict):
                app_dict['applicationVersionSpecs'] = json.dumps(applicationVersionSpecs)
                applicationVersionSpecDOList = []
                a = 0
                for version in applicationVersionSpecs['version']:
                    for useNumber in applicationVersionSpecs['useNumber']:
                        for cycle in applicationVersionSpecs['cycle']:
                            applicationVersion = {'applicationSpecs': {}}
                            applicationVersion['applicationSpecs']['version'] = version
                            applicationVersion['applicationSpecs']['useNumber'] = useNumber
                            applicationVersion['applicationSpecs']['cycle'] = cycle
                            applicationVersion['price'] = price[a] if a < len(price) else 0.01
                            applicationVersion['showFlag'] = showFlag[a] if a < len(showFlag) else 1
                            applicationVersionSpecDOList.append(applicationVersion)
                            a += 1

                app_dict['applicationVersionSpecDOList'] = applicationVersionSpecDOList
            else:
                app_dict['applicationVersionSpecs'] = applicationVersionSpecs
        return json.dumps(app_dict)