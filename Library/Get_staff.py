import json
from collections import Iterable

class Get_staff(object):


    def __init__(self):
        pass

    def staff_list(self,AllDeptUser,types,*dept_staffnames):

        result = []
        dept_stafflist = []

        if types == 'staff':
            self.staff_mes(result, dept_stafflist, AllDeptUser, *dept_staffnames)
        else:
            for deptname in dept_staffnames:
                dept_dict = {}
                if deptname == AllDeptUser['deptName'] and deptname not in dept_stafflist:
                    dept_dict['deptId'] = AllDeptUser['deptId']
                    dept_dict['deptName'] = AllDeptUser['deptName']
                    result.append(dept_dict)
                    dept_stafflist.append(AllDeptUser['deptName'])
            self.dept_mes(result, dept_stafflist, AllDeptUser, *dept_staffnames)
        print(result)
        def dept(lst):
            try:
                for item in lst['deptList']:
                    if types == 'staff':
                        self.staff_mes(result,dept_stafflist,item,*dept_staffnames)
                    else:
                        self.dept_mes(result,dept_stafflist,item,*dept_staffnames)

                    try:
                        if isinstance(item['deptList'], Iterable):
                            dept(item)
                    except Exception:
                        pass
            except Exception:
                pass
        dept(AllDeptUser)
        return result


    def staff_mes(self,result,stafflist,item,*staffnames):

        for staffname in staffnames:
            try:
                for staf in item['staffList']:
                    staff_dict = {}
                    if staffname == staf['staffName'] and staffname not in stafflist:
                        staff_dict['staffId'] = staf['staffId']
                        staff_dict['staffName'] = staf['staffName']
                        result.append(staff_dict)
                        stafflist.append(staffname)
            except Exception:
                pass

        return

    def dept_mes(self,result,deptlist,item,*deptnames):

        for deptname in deptnames:

            try:
                for dep in item['deptList']:
                    dept_dict = {}
                    if deptname == dep['deptName'] and deptname not in deptlist:
                        dept_dict['deptId'] = str(dep['deptId'])
                        dept_dict['deptName'] = dep['deptName']
                        result.append(dept_dict)
                        deptlist.append(deptname)
            except Exception:
                pass

        return


    def get_role(self,roleList,*roles):
        L = []
        for role_mes in roleList:
            for role in roles:
                role_dict = {}
                if role_mes['roleName'] == role:
                    role_dict['roleId'] = role_mes['roleId']
                    role_dict['roleName'] = role_mes['roleName']
                    L.append(role_dict)

        return L