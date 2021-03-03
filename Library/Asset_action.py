import json
import copy
import re

class Asset_action(object):


    def __init__(self):
        pass


    def actionHandler(self,form_mes,action_name,**kwargs):

        action_mes={
            "actionId": "",
            "formId": "",
            "parametList": [],
            "recordId": "",
            "itemList":[]
        }


        for action in form_mes['actionList']:
            if action_name==action['actionName']:
                action_mes['actionId'] = action['actionId']
                action_mes['formId'] = action['formId']

        for itemList in form_mes['formBean']['formItems']:
            item = {}
            item['itemId']=itemList['itemId']
            item['itemTitle']=itemList['itemTitle']

            if itemList['componentType']=='text':
                for key,value in kwargs.items():
                    if key == itemList['itemTitle']:
                        item['values'] = value
                    else:
                        item['values'] = ''
            action_mes['itemList'].append(item)

        return json.dumps(action_mes)

    def save_action(self, addForm, **kwargs):

        form = {
            "formId": addForm['formId'],
            "recordId": "",
            "actionId": "",
            "itemList": addForm['itemList']
            }
        if 'groupList' in addForm.keys():
            form['groupList']=addForm['groupList']

        for item in form['itemList']:
            showFormat = 'yyyy-MM-dd'
            halfDay = {"option": [{"value": "上午", "label": "上午"}, {"value": "下午", "label": "下午"}], "time": ""}

            if not item.get('values'):
                item['values'] = ''
            for key, value in kwargs.items():

                if key == item['itemTitle']:
                    if item['componentType'] == 'radio' or item['componentType'] == 'checkbox':
                        depts = []
                        for dept in item['props']['options']:
                            option = {}
                            val = {}
                            val['id'] = dept['optionId']
                            val['name'] = dept['optionName']
                            option['value'] = json.dumps(val, ensure_ascii=False)
                            option['label'] = dept['optionName']
                            if dept.get('children'):
                                option['children'] = []
                                for child in dept['children']:
                                    ch = {}
                                    chd = {}
                                    ch['id'] = child['optionId']
                                    ch['name'] = child['optionName']
                                    chd['value'] = json.dumps(ch, ensure_ascii=False)
                                    chd['label'] = child['optionName']
                                    chd['__label'] = chd['label']
                                    chd['__value'] = chd['value']
                                    option['children'].append(chd)
                                    if '-' in value:
                                        vas = value.split('-')
                                        if option['label'] == vas[0] and chd['label'] == vas[1]:
                                            item['values'] = json.dumps([val, ch], ensure_ascii=False)
                            else:
                                option['__label'] = option['label']
                                option['__value'] = option['value']
                            depts.append(option)
                            if option['label'] == value:
                                item['values'] = json.dumps([val], ensure_ascii=False)
                        item['props']['options'] = depts

                    else:
                        item['values'] = value
                    break
                else:continue

        for group in form['groupList']:
            detailRecordList = []
            for detail in group['detailRecordList']:
                det = copy.deepcopy(detail)
                for key, value in kwargs.items():
                    a = 0
                    while a < len(det['itemList']):
                        item = det['itemList'][a]
                        a += 1
                        if re.findall('^' + item['itemTitle'] + '\d*', key):
                            if item.get('values'):
                                detailRecordList.append(det)
                                det = copy.deepcopy(detail)
                                a = 0
                                item = det['itemList'][a]
                            if item['componentType'] == 'radio':
                                depts = []
                                for dept in item['props']['options']:
                                    option = {}
                                    val = {}
                                    val['id'] = dept['optionId']
                                    val['name'] = dept['optionName']
                                    option['value'] = json.dumps(val, ensure_ascii=False)
                                    option['label'] = dept['optionName']
                                    option['children'] = []
                                    option['__label'] = option['label']
                                    option['__value'] = option['value']
                                    depts.append(option)
                                    if option['label'] == value:
                                        item['values'] = option['value']
                                item['props']['options'] = depts

                            else:
                                item['values'] = value

                detailRecordList.append(det)

            group['detailRecordList'] = detailRecordList

        return json.dumps(form, ensure_ascii=False)

