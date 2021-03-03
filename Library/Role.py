import json

class Role(object):


    def __init__(self):
        pass

    def add_Rolefunc(self,role_group,role_dict,roleName,groupId,*funcName):

        rolefunc_mes = {
                "roleId": role_dict['data']['roleId'],
                "roleName": roleName,
                "groupId": groupId,
                "funcList": []
            }
        for funclist in role_dict['data']['funcList']:
            func_dict = {}
            func_dict['funcId'] = funclist['funcId']
            func_dict['funcName'] = funclist['funcName']
            rolefunc_mes['funcList'].append(func_dict)

        for func in role_group['data'][0]['childrens']:
            for children in func['childrens']:
                for name in funcName:
                    if name == children['funcName']:
                        func_dict = {}
                        func_dict['funcId'] = children['funcId']
                        func_dict['funcName'] = children['funcName']
                        rolefunc_mes['funcList'].append(func_dict)


        return json.dumps(rolefunc_mes)