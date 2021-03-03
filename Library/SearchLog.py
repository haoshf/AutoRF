import json

class SearchLog(object):


    def __init__(self):
        pass

    def Loglist_mes(self,pageFlag,pageNum,pageSize,types,startTime,endTime,queryStaffId,formId):

        log_mes = {
                "pageFlag": pageFlag,
                "pageNum": pageNum,
                "pageSize": pageSize,
                "paramMap": {
                    "startTime": {
                        "name": "startTime",
                        "value": startTime
                    },
                    "endTime": {
                        "name": "endTime",
                        "value": endTime
                    },
                    "queryStaffId": {
                        "name": "queryStaffId",
                        "value": queryStaffId
                    },
                    "formId": {
                        "name": "formId",
                        "value": formId
                    },
                    "type": {
                        "name": "type",
                        "value": types
                    }
                }
            }
        if formId != '':
            form = {
                "name": "formId",
                "symbol": "equal",
                "value": formId
            }
            log_mes['paramMap']['formId']=form
        return json.dumps(log_mes)