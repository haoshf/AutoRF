import json


class Holiday(object):
    def __init__(self):
        self.holiday = {
            '假期名称': 'holidayName',
            '新员工请假': 'isInductionLeave',
            '最小请假单位': 'minUnit',
            '请假时长核算': 'extendNum',
            '假期余额': 'enableBalance',
            '延长有效期': 'isExtendValidity',
            '余额发放方式': 'balanceLssueWay',
            '发放日期': 'lssueTime',
            '额度规则': 'balanceRule',
            '有效期': 'ageingType',
            '每年固定时间': 'ageingDate',
            '按实际工时': 'actualWorkingHours'
        }

    def save_holi(self, deptId, **kwargs):

        holi_mes = {
            "hrAttHolidayDo": {
                "holidayName": "",
                "minUnit": "",
                "isInductionLeave": "",
                "spanType": "1",
                "balanceLssueWay": "1",
                "ageingType": "1",
                "ageingDate": "2020-01-01",
                "extendUnit": "0",
                "extendNum": 1,
                "isExtendValidity": 0,
                "enableBalance": 0,
                "actualWorkingHours": 0
            },
            "balanceRuleDoList": [
                {
                    "workLengthType": "2",
                    "workLength": 1,
                    "operator": "3",
                    "balance": 0
                }
            ],
            "targetList": [
                {
                    "deptId": deptId,
                    "targetType": "0",
                    "staffId": ""
                }
            ]
        }

        for key, value in kwargs.items():
            if str(value).startswith('!'):
                value = int(value[1:])

            if key == '年假':
                holi_mes['balanceRuleDoList'] = []
                for i, v in enumerate(value):
                    balanceRule = {}
                    balanceRule['workLengthType'] = holi_mes['hrAttHolidayDo']['balanceLssueWay']
                    balanceRule['workLength'] = i
                    balanceRule['operator'] = '3'
                    balanceRule['balance'] = int(v)
                    holi_mes['balanceRuleDoList'].append(balanceRule)
            else:
                holi_mes['hrAttHolidayDo'][self.holiday[key]] = value

        return json.dumps(holi_mes)

    def update_holi(self, holi_mes, **kwargs):

        for key, value in kwargs.items():
            if str(value).startswith('!'):
                value = int(value[1:])

            if key == '年假':
                holi_mes['balanceRuleDoList'] = []
                for i, v in enumerate(value):
                    balanceRule = {}
                    balanceRule['workLengthType'] = holi_mes['hrAttHolidayDo']['balanceLssueWay']
                    balanceRule['workLength'] = i
                    balanceRule['operator'] = '3'
                    balanceRule['balance'] = int(v)
                    holi_mes['balanceRuleDoList'].append(balanceRule)
            else:
                holi_mes['hrAttHolidayDo'][self.holiday[key]] = value

        return json.dumps(holi_mes)

    def ope_save_holi(self, **kwargs):

        holi_mes = {
            "holidayName": "",
            "minUnit": "",
            "isInductionLeave": "",
            "spanType": "0",
            "balanceLssueWay": "1",
            "ageingType": "1",
            "ageingDate": "2020-01-01",
            "extendUnit": "0",
            "extendNum": 1,
            "isExtendValidity": 0,
            "enableBalance": 0,
            "actualWorkingHours": 0,
            "hrAttBalanceRuleDOS": [
                {
                    "workLengthType": "2",
                    "workLength": 1,
                    "operator": "3",
                    "balance": 0
                }
            ],
            "lssueTime": "2",
            "balanceRule": "1",
        }

        for key, value in kwargs.items():
            if str(value).startswith('!'):
                value = int(value[1:])

            if key == '年假':
                holi_mes['hrAttBalanceRuleDOS'] = []
                for i, v in enumerate(value):
                    balanceRule = {}
                    balanceRule['workLengthType'] = holi_mes['balanceLssueWay']
                    balanceRule['workLength'] = i
                    balanceRule['operator'] = '3'
                    balanceRule['balance'] = int(v)
                    holi_mes['hrAttBalanceRuleDOS'].append(balanceRule)
            else:
                holi_mes[self.holiday[key]] = value

        return json.dumps(holi_mes)

    def ope_update_holi(self, holi_mes, **kwargs):

        for key, value in kwargs.items():
            if str(value).startswith('!'):
                value = int(value[1:])

            if key == '年假':
                holi_mes['hrAttBalanceRuleDOS'] = []
                for i, v in enumerate(value):
                    balanceRule = {}
                    balanceRule['workLengthType'] = holi_mes['balanceLssueWay']
                    balanceRule['workLength'] = i
                    balanceRule['operator'] = '3'
                    balanceRule['balance'] = int(v)
                    holi_mes['hrAttBalanceRuleDOS'].append(balanceRule)
            else:
                holi_mes[self.holiday[key]] = value

        return json.dumps(holi_mes)