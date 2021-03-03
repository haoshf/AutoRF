import json
import datetime


class Item(object):
    def __init__(self):

        self.news_item = {
            '标题': 'title',
            '分类': 'groupId',
            '缩略图': 'image',
            '内容': 'content',
            '附件': 'attachment',
            '私聊': 'privateChat',
            '发布时间': 'publishTime'
        }
        self.appTime = datetime.datetime.now().strftime('%Y-%m-%d %X')

    def save_item(self, staffId, bpId, **kwargs):

        item_mes = {
            "updateBy": staffId,
            "operateType": "",
            "bpId": bpId,
            "status": "",
            "title": "",
            "groupId": "",
            "content": "",
            "attachment": [],
            "image": "",
            "needConfirm": "0",
            "canBeShare": "0",
            "publishTime": "",
            "receiverList": [],
            "privateChat": 0
        }
        for key, value in kwargs.items():
            if key == '部门':
                for v in value:
                    dept = {}
                    dept['name'] = v['deptName']
                    dept['type'] = 'dept'
                    dept['value'] = v['deptId']
                    item_mes['receiverList'].append(dept)
            elif key == '人员':
                for v in value:
                    user = {}
                    user['name'] = v['staffName']
                    user['type'] = 'user'
                    user['value'] = v['staffId']
                    item_mes['receiverList'].append(user)
            elif key == '角色':
                for v in value:
                    role = {}
                    role['name'] = v['roleName']
                    role['type'] = 'role'
                    role['value'] = v['roleId']
                    item_mes['receiverList'].append(role)

            elif key == '立即发布':
                item_mes['operateType'] = 'publish'
                item_mes['publishTime'] = self.appTime
                item_mes['status'] = '2'
            elif key == '定时发布':
                item_mes['operateType'] = 'publish'
                item_mes['publishTime'] = value
                item_mes['status'] = '1'

            elif key == '存为草稿':
                item_mes['operateType'] = 'add'
                item_mes['publishTime'] = self.appTime
                item_mes['status'] = '0'
            else:
                item_mes[self.news_item[key]] = value

        return json.dumps(item_mes)


    def up_item(self,news, **kwargs):

        item_mes = {
            "updateBy": "",
            "operateType": "",
            "bpId": "",
            "status": "",
            "newsId":"",
            "title": "",
            "groupId": "",
            "content": "",
            "attachment": [],
            "image": "",
            "needConfirm": "0",
            "canBeShare": "0",
            "publishTime": "",
            "receiverList": [],
            "privateChat": 0
        }

        for key,value in news['data']['newsInfo'].items():
            if key in list(item_mes.keys()):
                item_mes[key] =value

        for key, value in kwargs.items():
            if key == '部门':
                for v in value:
                    dept = {}
                    dept['name'] = v['deptName']
                    dept['type'] = 'dept'
                    dept['value'] = v['deptId']
                    item_mes['receiverList'].append(dept)
            elif key == '人员':
                for v in value:
                    user = {}
                    user['name'] = v['staffName']
                    user['type'] = 'user'
                    user['value'] = v['staffId']
                    item_mes['receiverList'].append(user)
            elif key == '角色':
                for v in value:
                    role = {}
                    role['name'] = v['roleName']
                    role['type'] = 'role'
                    role['value'] = v['roleId']
                    item_mes['receiverList'].append(role)

            elif key == '立即发布':
                item_mes['operateType'] = 'publish'
                item_mes['publishTime'] = self.appTime
                item_mes['status'] = '2'
            elif key == '定时发布':
                item_mes['operateType'] = 'publish'
                item_mes['publishTime'] = value
                item_mes['status'] = '1'
            elif key == '存为草稿':
                item_mes['operateType'] = 'add'
                item_mes['publishTime'] = self.appTime
                item_mes['status'] = '0'
            else:
                item_mes[self.news_item[key]] = value

        return json.dumps(item_mes)