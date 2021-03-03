import json


class PubHoliday(object):
    def __init__(self): pass

    def save_pubholi(self, phId,startTime,endTime,*parms):
        pubHoliday_mes = {
            "startTime": startTime,
            "endTime": endTime,
            "phId": phId,
            "workList": []
        }

        for date in parms:
            work = {}
            work['startTime'] = date
            work['endTime'] = date
            pubHoliday_mes['workList'].append(work)

        return json.dumps(pubHoliday_mes)