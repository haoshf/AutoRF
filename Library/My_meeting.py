import json


class My_meeting(object):


    def __init__(self):
        pass


    def cc_staff(self,reserveId,staffs):

        cc_mes = {
                "reserveId": reserveId,
                "ccList": [
                ]
            }

        for staff in staffs:
            ccList = {}
            ccList['name'] = staff['staffName']
            ccList['value'] = staff['staffId']
            ccList['type'] = 'user'
            ccList['headPortrait'] = ''
            cc_mes['ccList'].append(ccList)

        return json.dumps(cc_mes)