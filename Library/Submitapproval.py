# coding=utf-8

import json
import copy
from .Saveform import Saveform

class Submitapproval(object):

    def __init__(self):pass

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


