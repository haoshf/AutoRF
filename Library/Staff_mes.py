import json

class Staff_mes(object):


    def __init__(self):

        self.staff = {
            "姓名":"staffName",
            "花名": "roster",
            "部门":"deptList",
            "职位": "position",
            "工号": "staffCode",
            "E-mail": "bpEmail",
            "性别":"gender",
            "手机": "mobile",
            "角色": "roleList",
            "入职时间": "joinDate",
            "参加工作年限": "workYears",
            "学历":"education",
            "考勤规则":"ruleId",
            "试用期":"probation"
        }

    def add_staff(self,bpId,**staffs):
        staff_dict = {
                "bpId": bpId,
                "userId": "",
                "staffName": "蒙奇D路飞",
                "roster": "",
                "staffCode": 10,
                "gender": "M",
                "position": "海贼",
                "mobile": "13930663066",
                "bpEmail": "10@qq.com",
                "joinDate": "2020-08-11",
                "workYears": 0,
                "education": "",
                "ruleId": 1,
                "probation": 1,
                "state": "1"
            }
        for key,value in staffs.items():
            if '!' in value:
                value = int(value[1:])
            staff_dict[self.staff[key]]  = value

        return json.dumps(staff_dict)

    def update_staff(self,staff_mes,**staffs):
        staff_dict = staff_mes.copy()
        staff_dict.pop('user')
        staff_dict.pop('funcLis')

        roleList = []
        deptList = []
        for role_dict in staff_dict['roleList']:
            role = {}
            role['roleId'] = role_dict['roleId']
            role['roleName'] = role_dict['roleName']
            roleList.append(role)

        for dept_dict in staff_dict['deptList']:
            dept = {}
            dept['deptId'] = dept_dict['deptId']
            dept['deptName'] = dept_dict['deptName']
            deptList.append(dept)

        staff_dict.pop('roleList')
        staff_dict.pop('deptList')
        staff_dict['roleList'] = roleList
        staff_dict['deptList'] = deptList
        print(staff_dict)
        for key,value in staffs.items():

            staff_dict[self.staff[key]] = value

        return json.dumps(staff_dict)