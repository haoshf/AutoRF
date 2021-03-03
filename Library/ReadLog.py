import json

class ReadLog(object):


    def __init__(self):
        pass

    def ReadLog(self,pageFlag,pageNum,pageSize,staffIds,deptIds,startTime,endTime,isReaded,formId=''):

        log_mes = {
                "pageFlag": pageFlag,
                "pageNum": pageNum,
                "pageSize": pageSize,
                "paramMap": {
                    "staffIds": {
                        "name": "staffIds",
                        "symbol": "equal",
                        "value": staffIds
                    },
                    "deptIds": {
                        "name": "deptIds",
                        "symbol": "equal",
                        "value": deptIds
                    },
                    "startTime": {
                        "name": "startTime",
                        "symbol": "equal",
                        "value": startTime
                    },
                    "endTime": {
                        "name": "endTime",
                        "symbol": "equal",
                        "value": endTime
                    },
                    "isReaded": {
                        "name": "isReaded",
                        "symbol": "equal",
                        "value": isReaded
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