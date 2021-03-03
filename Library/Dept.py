import json

class Dept(object):

    """
    部门管理
    """
    def __init__(self):
        pass

    def add_dept(self,bpId,parentId,deptName,chatGroupChecked,*staffs):

        dept_dict = {
            "bpId": bpId,
            "parentId": parentId,
            "deptName": deptName,
            "managerList": [
                # {
                #     "staffId": "10000000010031_1000000000072",
                #     "staffName": "13938863072"
                # }
            ],
            "chatGroupChecked": chatGroupChecked,
            "chatGroupName": deptName
            }

        for staff in staffs:
            print(staff)
            manager = {}
            manager['staffId'] = staff['staffId']
            manager['staffName'] = staff['staffName']
            dept_dict['managerList'].append(manager)

        return json.dumps(dept_dict)


    def update_dept(self,dept_result,**kwargs):

        dept_dict = {
                "bpId": dept_result['data']['bpId'],
                "parentId": dept_result['data']['parentId'],
                "deptName": dept_result['data']['deptName'],
                "deptId": dept_result['data']['deptId'],
                "managerList": [
                    # {
                    #     "staffId": "10000000010031_1000000000072",
                    #     "staffName": "13938863072"
                    # }
                ],
                "chatGroupChecked": dept_result['data']['chatGroupChecked'],
                "chatGroupName": dept_result['data']['chatGroupName'],
            }
        if dept_result['data']['chatGroupChecked'] != 0:
            dept_dict["chatGroupOwner"] = dept_result['data']['chatGroupOwner']

        for staff in dept_result['data']['managerList']:
            manager = {}
            manager['staffId'] = staff['staffId']
            manager['staffName'] = staff['staffName']
            dept_dict['managerList'].append(manager)

        for key,value in kwargs.items():
            if key == '上级部门':
                dept_dict['parentId'] = value
            elif key == '部门名称':
                dept_dict['deptName'] = value
                dept_dict['chatGroupName'] = value
            elif key == '部门主管':
                for sf in value:
                    manager = {}
                    manager['staffId'] = value['staffId']
                    manager['staffName'] = value['staffName']
                    dept_dict['managerList'].append(manager)
            elif key == '创建部门群':
                dept_dict["chatGroupChecked"] = value,

        return json.dumps(dept_dict)