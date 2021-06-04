# coding=utf-8

import json
import copy
import re


class Saveform(object):
    def __init__(self):
        pass

    def realTime_save(self, startInstance, Title=None, **kwargs):

        realTime_dict = {
            'formId': startInstance['formRecord']['formId'],
            'actionId': '',
            'itemList': startInstance['formRecord']['itemList'],
            'groupList': startInstance['formRecord']['groupList']
        }

        for item in realTime_dict['itemList']:
            showFormat = 'yyyy-MM-dd'
            halfDay = {"option": [{"value": "上午", "label": "上午"}, {"value": "下午", "label": "下午"}], "time": ""}

            if not item.get('values'):
                item['values'] = ''
            if item['itemTitle'] == '发起人':
                pd = json.loads(item['values'])
                if isinstance(pd, dict):
                    pd['headPortrait'] = ''
                    pd['yes'] = False
                    item['values'] = json.dumps([pd], ensure_ascii=False)
                else:
                    for p in pd:
                        p['headPortrait'] = ''
                        p['yes'] = False
                    item['values'] = json.dumps(pd, ensure_ascii=False)
            elif item['itemTitle'] == '发起部门':
                depts = []
                for dept in item['props']['options']:
                    option = {}
                    value = {}
                    value['id'] = dept['optionId']
                    value['name'] = dept['optionName']
                    option['value'] = json.dumps(value, ensure_ascii=False)
                    option['label'] = dept['optionName']
                    option['__label'] = option['label']
                    option['__value'] = option['value']
                    depts.append(option)
                item['props']['options'] = depts
                if item.get('values'):
                    pd = json.loads(item['values'])
                    if isinstance(pd, dict):
                        item['values'] = json.dumps([pd], ensure_ascii=False)

            for key, value in kwargs.items():

                if key == item['itemTitle']:
                    if item['componentType'] == 'radio':
                        if key != '请假类型' and key != '发起部门':
                            depts = []
                            for dept in item['props']['options']:
                                option = {}
                                val = {}
                                val['id'] = dept['optionId']
                                val['name'] = dept['optionName']
                                option['value'] = json.dumps(val, ensure_ascii=False)
                                option['label'] = dept['optionName']
                                if dept.get('children'):
                                    print(dept)
                                    option['children'] = []
                                    for child in dept['children']:
                                        ch = {}
                                        chd = {}
                                        ch['id']=child['optionId']
                                        ch['name']= child['optionName']
                                        chd['value'] = json.dumps(ch, ensure_ascii=False)
                                        chd['label'] = child['optionName']
                                        chd['__label'] = chd['label']
                                        chd['__value'] = chd['value']
                                        option['children'].append(chd)
                                        if '-' in value:
                                            vas = value.split('-')
                                            if option['label'] == vas[0] and chd['label'] == vas[1]:
                                                item['values'] =  json.dumps([val,ch], ensure_ascii=False)
                                else:
                                    option['__label'] = option['label']
                                    option['__value'] = option['value']
                                depts.append(option)
                                if option['label'] == value:
                                    item['values'] = json.dumps([val], ensure_ascii=False)
                            item['props']['options'] = depts


                        elif key == '发起部门':
                            for dept in item['props']['options']:
                                if option['label'] == value:
                                    item['values'] = option['value']


                        elif key == '请假类型':
                            for holiday in Title:
                                option = {}
                                val = {}
                                val['id'] = holiday['holidayId']
                                if holiday['minUnit'] == '1':
                                    minUnit = '(天)'
                                    halfDay = ''
                                elif holiday['minUnit'] == '2':
                                    minUnit = '(半天)'
                                elif holiday['minUnit'] == '3':
                                    minUnit = '(小时)'
                                    showFormat = 'yyyy-MM-dd HH:mm'
                                    halfDay = ''
                                val['name'] = holiday['holidayName'] + minUnit
                                option['value'] = json.dumps(val, ensure_ascii=False)
                                option['label'] = holiday['holidayName']
                                option['children'] = []
                                item['props']['options'].append(option)
                                if option['label'] == value:
                                    item['values'] = option['value']
                            break

                    elif item['itemTitle'] in ['开始时间', '结束时间', '出差开始日期', '出差结束日期']:
                        item['values'] = value
                        item['props']['showFormat'] = showFormat
                        if halfDay != '':
                            item['halfDay'] = copy.deepcopy(halfDay)
                            item['halfDay']['time'] = value[-2:]
                            if key in ['开始时间', '结束时间']:
                                item['valuesDesc'] = value
                        break

                    elif item['itemTitle'] == '项目名称':
                        for refform in Title:
                            for pro in refform['itemList']:
                                if pro['itemTitle'] == '项目名称' and pro['values'] == value:
                                    project = {}
                                    project['id'] = refform['recordId']
                                    project['type'] = refform['formId']
                                    project['name'] = value
                                    item['values'] = json.dumps(project, ensure_ascii=False)
                        break

                    elif item['itemTitle'] == 'refbpm':
                        for refform in Title:
                            for pro in refform['formRecord']['itemList']:
                                v = value.split('-')
                                if pro['itemTitle'] == v[0] and v[1] in pro['values']:
                                    project = {}
                                    project['id'] = refform['instance']['instId']
                                    project['type'] = refform['instance']['processId']
                                    project['name'] = refform['instance']['originateByName'] + '的%s' % item['itemTitle']
                                    item['values'] = json.dumps(project, ensure_ascii=False)
                        break

                    else:
                        item['values'] = value
                        break

        for group in realTime_dict['groupList']:
            detailRecordList = []
            for detail in group['detailRecordList']:
                det = copy.deepcopy(detail)
                for key, value in kwargs.items():
                    print('-----------------',key)
                    a = 0
                    while a < len(det['itemList']):
                        item = det['itemList'][a]
                        a += 1
                        key_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", key)
                        title_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", item['itemTitle'])
                        if re.findall('^' + title_str + '\d*', key_str):
                            if item.get('values'):
                                print(item['values'])
                                detailRecordList.append(det)
                                det = copy.deepcopy(detail)
                                a = 0
                                item = det['itemList'][a]
                            elif item['componentType'] == 'radio':
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

        return json.dumps(realTime_dict, ensure_ascii=False)


    def Submit_app(self,startInstance,Title=None,staff_list=None,**kwargs):
        Submit_app = copy.deepcopy(startInstance)
        realTime_dict = json.loads(Saveform().realTime_save(startInstance,Title,**kwargs))
        Submit_app['formRecord']['itemList']= realTime_dict['itemList']
        Submit_app['formRecord']['groupList']= realTime_dict['groupList']
        Submit_app['instTask']['actionType'] = 'submit'
        Submit_app['instTask']['actionRemark'] = '提交请求'
        for i,approve_mes in enumerate(Submit_app['approveList']):
            approve_mes['approvers'] = []
            approve_mes['selectReporter'] = []
            if approve_mes['nodeText'] == '发起人自选':
                for key, value in kwargs.items():
                    if key in ['审批人','抄送人']:
                        for staff_mes in staff_list['staffList']:
                            for staff in value:
                                if staff==staff_mes['staffName']:
                                    approver = {}
                                    approver['staffId']=staff_mes['staffId']
                                    approver['staffName']=staff_mes['staffName']
                                    approver['deptId']=staff_mes['deptId'][0]
                                    approver['level']=str(i+1)
                                    if key=='审批人':
                                        approve_mes['approvers'].append(approver)
                                    else:
                                        approve_mes['selectReporter'].append(approver)


        return json.dumps(Submit_app)