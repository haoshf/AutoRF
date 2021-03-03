import json

class Mymeeting(object):


    def __init__(self):
        pass

    def Mymeeting(self,Time):
        """
        我的会议
        :param timestamp:
        :param startTime:
        :param endTime:
        :return:
        """
        meeting_mes = {
                "pageNum": 1,
                "pageSize": 4,
                "paramMap": {
                    "scheduledStatus": {
                        "name": "scheduledStatus",
                        "value": ""
                    },
                    "startTime": {
                        "name": "startTime",
                        "value": "%s 00:00:00"%Time
                    },
                    "endTime": {
                        "name": "endTime",
                        "value": "%s 23:59:59"%Time
                    },
                    "appStart": {
                        "name": "appStart",
                        "value": ""
                    },
                    "meetingId": {
                        "name": "meetingId",
                        "value": ""
                    },
                    "appEnd": {
                        "name": "appEnd",
                        "value": ""
                    },
                    "meetingTheme": {
                        "name": "meetingTheme",
                        "value": ""
                    },
                    "condition": {
                        "name": "condition",
                        "value": "dashboard"
                    },
                    "sponsor": {
                        "name": "sponsor",
                        "value": ""
                    }
                }
            }
        return json.dumps(meeting_mes)