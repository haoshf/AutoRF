import json
import time,datetime
import re

class Reserve_meeting(object):


    def __init__(self):
        self.meeting={
            '会议主题':'meetingTheme',
            '会议内容':'meetingContent',
            '发起部门':'deptId',
            '会议室':'meetingId',
            '会议服务要求':'serviceRequest',
            '会议服务负责人':'serviceUserId',
            '签到负责人':'checkPerson',
            '会议开始前':'checkBeforeTime',
            '会议开始后':'checkAfterTime',
            '会议提醒':'remindList',
            '推送':'isPush',
            '附件':'annex'
        }
        self.appTime = datetime.datetime.now().strftime('%Y-%m-%d %X')

    def add_meeting(self,staffId,**kwargs):


        mes = {
                "meetingReserveDo": {
                    "reserveId": "",
                    "deptId": "",
                    "staffId": staffId,
                    "appTime": self.appTime,
                    "scheduledStatus": "1",
                    "meetingId": "",
                    "scheduledStartTime": "",
                    "scheduledEndTime": "",
                    "scheduledStartDate": "",
                    "scheduledEndDate": "",
                    "meetingContent": "",
                    "meetingTheme": "",
                    "annex": "[]",
                    "isQrCheck": "0",
                    "isPush": "0",
                    "isService": "0",
                    "serviceUserId": "",
                    "serviceRequest": "",
                    "isRemind": "0",
                    "remindTime": "",
                    "remark": "",
                    "qrCode": "",
                    "checkPerson": "",
                    "checkBeforeTime": "",
                    "checkAfterTime": ""
                },
                "joinList": [
                ],
                "recordList": [
                ],
                "ccList": [
                ],
                "remindList": [
                ]
            }
        for key, value in kwargs.items():

            if key in ['参会人','抄送人','记录人']:
                staff_List = []
                for i in list(value):
                    staff = {}
                    staff['type'] = 'user'
                    staff['name'] = i['staffName']
                    staff['value'] = i['staffId']
                    staff_List.append(staff)
                if key == '参会人':
                    mes['joinList'] = staff_List
                elif key == '记录人':
                    mes['recordList'] = staff_List
                elif key == '抄送人':
                    mes['ccList'] = staff_List

            elif key == '会议提醒':
                mes['meetingReserveDo']['remindList'] = value
                mes['meetingReserveDo']['isRemind'] = '1'

            elif key == '签到负责人':
                mes['meetingReserveDo']['checkPerson'] = value
                mes['meetingReserveDo']['isRemind'] = '1'

            elif key == '会议服务负责人':
                mes['meetingReserveDo']['serviceUserId'] = value
                mes['meetingReserveDo']['isService'] = '1'

            elif key == '预定时间':
                dates = re.findall('(\d{4}-\d{1,2}-\d{1,2})', value)
                times = re.findall('(\d{1,2}:\d{1,2})', value)
                mes['meetingReserveDo']['scheduledStartDate'] = dates[0]
                mes['meetingReserveDo']['scheduledEndDate'] = dates[1]
                mes['meetingReserveDo']['scheduledStartTime'] = times[0]
                mes['meetingReserveDo']['scheduledEndTime'] = times[1]


            else:
                mes['meetingReserveDo'][self.meeting[key]]=value

        return json.dumps(mes)


    def up_meeting(self,meeting_mes,**kwargs):

        mes = {
                "meetingReserveDo": {
                    "reserveId": "",
                    "deptId": "",
                    "staffId": "",
                    "appTime": self.appTime,
                    "scheduledStatus": "",
                    "meetingId": "",
                    "scheduledStartTime": re.findall('(\d{1,2}:\d{1,2})', meeting_mes['startTime'])[0],
                    "scheduledEndTime": re.findall('(\d{1,2}:\d{1,2})', meeting_mes['endTime'])[0],
                    "scheduledStartDate": re.findall('(\d{4}-\d{1,2}-\d{1,2})', meeting_mes['startTime'])[0],
                    "scheduledEndDate": re.findall('(\d{4}-\d{1,2}-\d{1,2})', meeting_mes['endTime'])[0],
                    "meetingContent": "",
                    "meetingTheme": "",
                    "annex": "[]",
                    "isQrCheck": "0",
                    "isPush": "0",
                    "isService": "0",
                    "serviceUserId": "",
                    "serviceRequest": "",
                    "isRemind": "0",
                    "remindTime": "",
                    "remark": "",
                    "qrCode": "",
                    "checkPerson": "",
                    "checkBeforeTime": "",
                    "checkAfterTime": ""
                },
                "joinList": [
                ],
                "recordList": [
                ],
                "ccList": [
                ],
                "remindList": [
                ]
            }
        for key, value in mes['meetingReserveDo'].items():
            if key in list(meeting_mes.keys()) and meeting_mes[key] and key != 'appTime':
                mes['meetingReserveDo'][key] = meeting_mes[key]

        for key, value in mes.items():
            if key in list(meeting_mes.keys()):
                staff_List = []
                for i in meeting_mes[key]:
                    staff = {}
                    staff['type'] = 'user'
                    staff['name'] = i['userName']
                    staff['value'] = i['staffId']
                    staff_List.append(staff)
                if key == 'joinList':
                    mes['joinList'] = staff_List
                elif key == 'recordList':
                    mes['recordList'] = staff_List
                elif key == 'ccList':
                    mes['ccList'] = staff_List

        for key, value in kwargs.items():


            if key in ['参会人','抄送人','记录人']:
                staff_List = []
                for i in list(value):
                    staff = {}
                    staff['type'] = 'user'
                    staff['name'] = i['staffName']
                    staff['value'] = i['staffId']
                    staff_List.append(staff)
                if key == '参会人':
                    mes['joinList'] = staff_List
                elif key == '记录人':
                    mes['recordList'] = staff_List
                elif key == '抄送人':
                    mes['ccList'] = staff_List

            elif key == '会议提醒':
                mes['meetingReserveDo']['remindList'] = value
                mes['meetingReserveDo']['isRemind'] = '1'

            elif key == '签到负责人':
                mes['meetingReserveDo']['checkPerson'] = value
                mes['meetingReserveDo']['isRemind'] = '1'

            elif key == '会议服务负责人':
                mes['meetingReserveDo']['serviceUserId'] = value
                mes['meetingReserveDo']['isService'] = '1'

            elif key == '预定时间':
                dates = re.findall('(\d{4}-\d{1,2}-\d{1,2})', value)
                times = re.findall('(\d{1,2}:\d{1,2})', value)
                mes['meetingReserveDo']['scheduledStartDate'] = dates[0]
                mes['meetingReserveDo']['scheduledEndDate'] = dates[1]
                mes['meetingReserveDo']['scheduledStartTime'] = times[0]
                mes['meetingReserveDo']['scheduledEndTime'] = times[1]

            else:
                mes['meetingReserveDo'][self.meeting[key]]=value

        return json.dumps(mes)