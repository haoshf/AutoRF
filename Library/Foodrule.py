import json


class Foodrule(object):
    def __init__(self):
        self.mes = {
            '订餐类型名称': 'ruleName',
            '上传订餐图片': 'orderImgNum',
            '可订餐开始时间': 'startTime',
            '可订餐结束时间': 'endTime',
            '重复': 'orderDate',
            '自定义': 'orderDateList',
            '跳过节日': 'isSkipHoliday',
            '订餐提醒': 'orderRemind',
            '订餐通知': 'orderNotify',
            '订餐说明': 'orderRemark',
        }

    def save_foodrule(self, **kwargs):

        foodrule = {
            "ruleId": "",
            "ruleName": "",
            "orderRemark": "",
            "orderImgNum": "",
            "assignDOS": [],
            "isSkipHoliday": "0",
            "orderDate": "1",
            "orderNotify": "",
            "orderRemind": "",
            "startTime": "",
            "endTime": "",
        }

        for key, value in kwargs.items():

            if str(value).startswith('!'):
                value = int(value[1:])
            if key == '订餐人员设置':
                for staff in value:
                    assign = {}
                    assign['name'] = staff['staffName']
                    assign['staffId'] = staff['staffId']
                    assign['objectType'] = 1
                    foodrule['assignDOS'].append(assign)
            elif key == '订餐部门设置':
                for dept in value:
                    assign = {}
                    assign['name'] = dept['deptName']
                    assign['deptId'] = dept['deptId']
                    assign['objectType'] = 2
                    foodrule['assignDOS'].append(assign)
            else:
                foodrule[self.mes[key]] = value

        return json.dumps(foodrule)

    def up_foodrule(self, detail,**kwargs):

        foodrule = {
            "ruleId": "",
            "ruleName": "",
            "orderRemark": "",
            "orderImgNum": "",
            "assignDOS": [],
            "isSkipHoliday": "0",
            "orderDate": "1",
            "orderNotify": "",
            "orderRemind": "",
            "startTime": "",
            "endTime": "",
            "orderDateList":""
        }
        for k1, v1 in detail.items():
            for k2 in foodrule.keys():
                if k1 == k2:
                    if v1:
                        if ':00' in v1:
                            v1 = v1[:-3]

                    if k2 == 'assignDOS':
                        for staff in v1:
                            assign = {}
                            assign['name'] = staff['name']
                            assign['objectType'] = staff['objectType']
                            if staff['objectType'] == '1':
                                assign['staffId'] = staff['staffId']
                            else:
                                assign['deptId'] = staff['deptId']

                            foodrule['assignDOS'].append(assign)
                    else:
                        foodrule[k2] = v1

        for key, value in kwargs.items():

            if str(value).startswith('!'):
                value = int(value[1:])
            if key == '订餐人员设置':
                for staff in value:
                    assign = {}
                    assign['name'] = staff['staffName']
                    assign['staffId'] = staff['staffId']
                    assign['objectType'] = 1
                    foodrule['assignDOS'].append(assign)
            elif key == '订餐部门设置':
                for dept in value:
                    assign = {}
                    assign['name'] = dept['deptName']
                    assign['deptId'] = dept['deptId']
                    assign['objectType'] = 2
                    foodrule['assignDOS'].append(assign)
            else:
                foodrule[self.mes[key]] = value

        return json.dumps(foodrule)