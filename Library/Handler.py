import json


class Handler(object):


    def __init__(self):
        pass


    def action(self,form_mes,*values):

        action_mes={
            'eventId':form_mes['eventList'][0]['eventId'],
            'parametList': [],
            'formId': form_mes['eventList'][0]['formId'],
            'itemList':form_mes['formRecord']['itemList'],
        }
        for itemList in action_mes['itemList']:
            itemList['value'] = ''

        return json.dumps(action_mes)

    def add_action(self,form_mes,*value):

        action_mes={
            'actionId':form_mes['actionList'][0]['actionId'],
            'parametList': [],
            'formId': form_mes['formRecord']['formId'],
            'itemList':form_mes['formRecord']['itemList'],
            'groupList':[]
        }

        return json.dumps(action_mes)

    def cancel_action(self,form_mes,*value):

        action_mes={
            'actionId':form_mes['actionList'][0]['actionId'],
            'parametList': [],
            'formId': form_mes['formRecord']['formId'],
            'recordId':form_mes['formRecord']['recordId'],
            'itemList':form_mes['formRecord']['itemList'],
            'groupList':[]
        }
        for itemList in action_mes['itemList']:
            itemList['value'] = ''

        return json.dumps(action_mes)