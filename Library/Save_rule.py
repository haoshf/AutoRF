import json
import datetime


class Save_rule(object):
    def __init__(self):
        self.rule = {
            '考勤规则名称': 'ruleName',
            '极速打卡设置': 'ruleType',
            '工作日': 'weekWorkDays',
            '节假日': 'enableHolidayAdjust',
            '外勤打卡': 'enableOutRegister',
            '允许补卡': 'enableRegisterFix',
            '限制补卡次数': 'enableRegisterFixNum',
            '补卡次数': 'registerFixNum',
            '限制补卡时间': 'enableRegisterFixDays',
            '补卡时间': 'registerFixDays',
            '打卡提醒': 'enableRemind',
            '上班提醒': 'onRemindMinutes',
            '上班提醒语': 'onRemindDesc',
            '下班提醒': 'offRemindMinutes',
            '下班提醒语': 'offRemindDesc',
            '允许迟到': 'enableLate',
            '迟到时间': 'lateMinutes',
            '迟到次数': 'lateNum',
            "允许早退": "enableLeave",
            "早退时间": "leaveMinutes",
            "早退次数": "leaveNum",
            "晚走晚到": "enableArriveLate",
            "晚走时间": "leaveLateMin",
            "晚到时间": "arriveLateMin",
            "严重迟到": "enableSeriousLate",
            "严重迟到时间": "seriousLateMinutes",
            "严重早退": "enableSeriousLeave",
            "严重早退时间": "seriousLeaveMinutes",
            "旷工": "enableAbsent",
            "迟到旷工时间": "absentLateMinutes",
            "早退旷工时间": "absentLeaveMinutes",
            "下班打卡": "disableOff",
        }

    def add_rule(self, bpId, staffId, **kwargs):
        rule_mes = {
            "ruleTargetDoList": [],
            "ruleUnRecordTargetDoList": [],
            "ruleReportUserDoList": [],
            "ruleShiftDoList": [],
            "ruleWifiDoList": [],
            "ruleAddressDoList": [],
            "ruleDo": {
                "enableSpeedPunch": "1",
                "weekWorkDays": "1111100",
                "ruleName": "",
                "ruleType": "0",
                "enableHolidayAdjust": "0",
                "enableOutRegister": "0",
                "enableRegisterFix": "0",
                "enableRegisterFixNum": "0",
                "registerFixNum": 0,
                "enableRegisterFixDays": "0",
                "registerFixDays": 0,
                "startDate": "",
                "specifiedDate": "0",
                "enableRemind": "0",
                "onRemindMinutes": 0,
                "onRemindDesc": "",
                "offRemindMinutes": 0,
                "offRemindDesc": "0",
                "enableLate": "0",
                "lateMinutes": 0,
                "lateNum": 0,
                "enableLeave": "0",
                "leaveMinutes": 0,
                "leaveNum": 0,
                "enableArriveLate": "0",
                "arriveLateMin": 0,
                "leaveLateMin": 0,
                "enableSeriousLate": "0",
                "seriousLateMinutes": 0,
                "enableSeriousLeave": "0",
                "seriousLeaveMinutes": 0,
                "enableAbsent": "0",
                "absentLateMinutes": 0,
                "absentLeaveMinutes": 0,
                "disableOff": "0",
                "reportToLeader": "0",
                "reportToUser": "0",
                "updateBy": "22",
                "bpId": bpId
            },
            "staffId": staffId
        }

        for key, value in kwargs.items():

            if key == '立即生效':
                rule_mes['ruleDo']['specifiedDate'] = '0'
                rule_mes['ruleDo']['startDate'] = datetime.datetime.now().strftime('%Y-%m-%d')
            elif key == '指定生效':
                rule_mes['ruleDo']['specifiedDate'] = '1'
                rule_mes['ruleDo']['startDate'] = value
            elif key == '考勤对象':
                for v in value:
                    ruleTarget = {}
                    ruleTarget['name'] = v['staffName']
                    ruleTarget['isNeedRecord'] = 1
                    ruleTarget['staffId'] = v['staffId']
                    ruleTarget['targetType'] = 1
                    rule_mes['ruleTargetDoList'].append(ruleTarget)
            elif key == '无需打卡人员':
                for v in value:
                    ruleTarget = {}
                    ruleTarget['name'] = v['staffName']
                    ruleTarget['isNeedRecord'] = 0
                    ruleTarget['staffId'] = v['staffId']
                    ruleTarget['targetType'] = 1
                    rule_mes['ruleUnRecordTargetDoList'].append(ruleTarget)
            elif key == '班次':
                for v in value:
                    ruleShift = {}
                    ruleShift['shiftId'] = v
                    rule_mes['ruleShiftDoList'].append(ruleShift)
            elif key == '考勤地点':
                for i in range(len(value) // 3):
                    ruleAddress = {}
                    ruleAddress['type'] = '0'
                    ruleAddress['name'] = value[3 * i]
                    ruleAddress['geographic'] = value[3 * i + 1]
                    ruleAddress['scope'] = value[3 * i + 2]
                    ruleAddress['sort'] = str(i)
                    rule_mes['ruleAddressDoList'].append(ruleAddress)
            elif key == 'WiFi考勤':
                for i in range(len(value) // 2):
                    ruleWifi = {}
                    ruleWifi['macAddress'] = value[3 * i]
                    ruleWifi['remark'] = value[3 * i + 1]
                    ruleWifi['sort'] = str(i)
                    ruleWifi['name'] = ''
                    rule_mes['ruleWifiDoList'].append(ruleWifi)
            else:
                rule_mes['ruleDo'][self.rule[key]] = value

        return json.dumps(rule_mes)


    def update_rule(self, staffId, rule_mes, **kwargs):

        rule_mes['staffId'] = staffId
        for key, value in kwargs.items():

            if key == '立即生效':
                rule_mes['ruleDo']['specifiedDate'] = '0'
                rule_mes['ruleDo']['startDate'] = datetime.datetime.now().strftime('%Y-%m-%d')
            elif key == '指定生效':
                rule_mes['ruleDo']['specifiedDate'] = '1'
                rule_mes['ruleDo']['startDate'] = value
            elif key == '考勤对象':
                rule_mes['ruleTargetDoList'] = []
                for v in value:
                    ruleTarget = {}
                    ruleTarget['name'] = v['staffName']
                    ruleTarget['isNeedRecord'] = 1
                    ruleTarget['staffId'] = v['staffId']
                    ruleTarget['targetType'] = 1
                    rule_mes['ruleTargetDoList'].append(ruleTarget)
            elif key == '无需打卡人员':
                rule_mes['ruleUnRecordTargetDoList'] = []
                for v in value:
                    ruleTarget = {}
                    ruleTarget['name'] = v['staffName']
                    ruleTarget['isNeedRecord'] = 0
                    ruleTarget['staffId'] = v['staffId']
                    ruleTarget['targetType'] = 1
                    rule_mes['ruleUnRecordTargetDoList'].append(ruleTarget)
            elif key == '班次':
                rule_mes['ruleShiftDoList'] = []
                for v in value:
                    ruleShift = {}
                    ruleShift['shiftId'] = v
                    rule_mes['ruleShiftDoList'].append(ruleShift)
            elif key == '考勤地点':
                rule_mes['ruleAddressDoList'] = []
                for i in range(len(value) // 3):
                    ruleAddress = {}
                    ruleAddress['type'] = '0'
                    ruleAddress['name'] = value[3 * i]
                    ruleAddress['geographic'] = value[3 * i + 1]
                    ruleAddress['scope'] = value[3 * i + 2]
                    ruleAddress['sort'] = str(i)
                    rule_mes['ruleAddressDoList'].append(ruleAddress)
            elif key == 'WiFi考勤':
                rule_mes['ruleWifiDoList'] = []
                for i in range(len(value) // 2):
                    ruleWifi = {}
                    ruleWifi['macAddress'] = value[3 * i]
                    ruleWifi['remark'] = value[3 * i + 1]
                    ruleWifi['sort'] = str(i)
                    ruleWifi['name'] = ''
                    rule_mes['ruleWifiDoList'].append(ruleWifi)
            else:
                rule_mes['ruleDo'][self.rule[key]] = value

        return json.dumps(rule_mes)
