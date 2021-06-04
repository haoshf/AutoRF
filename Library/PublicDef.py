#!/usr/bin/env python
# coding=utf-8

import json
import random
import datetime
import string
import pypinyin

class PublicDef(object):
    def __init__(self):
        pass

    def dict_num(self, dict_list, key, value):
        """
        输入列表，列表中为多个字典，根据键值对查找到对应字典，返回此字典
        :param dict_list:
        :param key:
        :param value:
        :return:
        """
        for a in list(dict_list):
            if str(a[str(key)]) == str(value):
                print('dict_mes', a)
                return a

        else:
            raise ValueError('未找到结果！')

    def dict_num2(self, dict_list, key1, value1, key2, value2):
        """
        输入列表，列表中为多个字典，根据两个键值对查找到对应字典，返回此字典在列表中的序号
        :param dict_list:
        :param key1:
        :param value1:
        :param key2:
        :param value2:
        :return:
        """
        for a in range(len(dict_list)):

            if list(dict_list)[a][str(key1)] == str(value1) and dict_list[a][str(key2)] == str(value2):
                return int(a)

        else:
            return '未找到结果！'

    def dict_num3(self, dict_list, key0, key, value):
        """
        多重字典、列表，根据键值对返回多重序号
        :param dict_list:
        :param firstkey:
        :param key:
        :param value:
        :return:
        """
        for a in range(len(dict_list)):
            for b in range(len(dict_list[a][key0])):
                if dict_list[a][key0][b][key] == value:
                    return int(a), int(b)
        else:
            raise ValueError('未找到结果！')

    def dict_num4(self, dict_list, key, value):
        """
        输入列表，列表中为多个字典，根据键值对模糊查找到对应字典，返回此字典
        :param dict_list:
        :param key:
        :param value:
        :return:
        """
        for a in list(dict_list):
            if str(value) in str(a[str(key)]):
                print('dict_mes', a)
                return a

        else:
            return '未找到结果！'

    def dict_num5(self, dict_list, **kwargs):
        """
        输入列表，列表中为多个字典，根据两个键值对查找到对应字典，返回此字典在列表中的序号
        :param dict_list:
        :param key1:
        :param value1:
        :param key2:
        :param value2:
        :return:
        """
        for key, value in kwargs.items():
            dict_list = self.pop_list(list(dict_list), key, value)

        if dict_list != []:
            return dict_list[0]
        else:
            return '未找到结果！'

    def dict_num6(self, dict_list, key0, key, value):
        """
        输入列表，列表中为多个字典，根据两个键值对查找到对应字典，返回此字典在列表中的序号
        :param dict_list:
        :param key1:
        :param value1:
        :param key2:
        :param value2:
        :return:
        """
        for a in list(dict_list):

            if a[key0][key] == value:
                return a
        else:
            raise ValueError('未找到结果！')

    def dict_num7(self, dict_list, key0, key, value):
        for a in list(dict_list):
            if key0 in a.keys():
                for b in a[key0]:
                    if key in b.keys():
                        if value in b[key]:
                            return b

        else:
            raise ValueError('未找到结果！')


    def pop_list(self, L, key, value):
        x = 0
        for i, a in enumerate(L[:]):
            if key in a.keys():
                if str(value) not in str(a[key]):
                    L.pop(i - x)
                    x += 1
        return L

    def get_date(self, days):
        date = self.set_date(days)
        return date

    def week(self, delayed_days):
        """
        指定周几
        :param delayed_days:
        :return:
        """
        now = datetime.datetime.now()
        week = now.weekday()
        if int(delayed_days) - 1 <= week:
            dates = int(delayed_days) + 6 - int(week)
        else:
            dates = int(delayed_days) - 1 - int(week)
        date = self.set_date(dates)
        return date

    def random_date(self):
        """
        随机生成一个大于今天，小于1年后的日期
        :return:
        """
        t = random.randint(1, 30)
        end = (datetime.datetime.now() + datetime.timedelta(days=t))

        return end.strftime('%Y-%m-%d')

    def set_birthday(self, days):
        delayed_days = int(days)
        final_date = (datetime.datetime.now() + datetime.timedelta(days=delayed_days))
        return final_date.strftime('%Y%m%d')

    def format_date(self, days):
        delayed_days = int(days)
        final_date = (datetime.datetime.now() + datetime.timedelta(days=delayed_days))
        return final_date.strftime('%Y%m%d')

    def month_simplify(self, month):
        """
        简写月份
        :return:
        """
        if str(month) == '01':
            month = 'JAN'
        elif str(month) == '02':
            month = 'FEB'
        elif str(month) == '03':
            month = 'MAR'
        elif str(month) == '04':
            month = 'APR'
        elif str(month) == '05':
            month = 'MAY'
        elif str(month) == '06':
            month = 'JUN'
        elif str(month) == '07':
            month = 'JUL'
        elif str(month) == '08':
            month = 'AUG'
        elif str(month) == '09':
            month = 'SEP'
        elif str(month) == '10':
            month = 'OCT'
        elif str(month) == '11':
            month = 'NOV'
        elif str(month) == '12':
            month = 'DEC'
        return month

    def departe_time(self, advancehour):
        """
        设置出发时间  这个方法针对用于航班开放值机规则那个模块
        advancehour:比当前时间多*个小时
        :return:
        """
        now = self.set_time()
        hour = now[:2]
        newhour = int(hour) + int(advancehour)
        minute = now[3:5]
        newminute = int(minute) + int(5)

        newnow = now[:5].replace(str(now[:2]), str(newhour))
        newnow = newnow.replace(str(newnow[3:]), str(newminute))

        return newnow

    def base_compute(self, a, compute, b):
        """
        功能：两个数的加减乘除
        :param a: 第一个数
        :param compute: 运算符合，如加、减、乘、除
        :param b: 第二个数
        :return: 返回运算结果
        """
        print('a的值：', a)
        print('a的类型：', type(a))
        print('b的值：', b)
        print('b的类型：', type(b))

        if str(compute) == '+':
            c = int(a) + int(b)
            print('两数相加结果：', c)
            return c
        if str(compute) == '-':
            c = int(a) - int(b)
            print('两数相减结果：', c)
            return c
        if str(compute) == '*':
            c = int(a) * int(b)
            print('两数相乘结果：', c)
            return c
        if str(compute) == '/':
            c = int(a) / int(b)
            print('两数相除结果：', c)
            return c

    def transform_sex(self, sex):
        if sex == 'F':
            return random.choice(['2', '4', '6', '8', '0'])
        elif sex == 'M':
            return random.choice(['1', '3', '5', '7', '9'])
        else:
            return '5'

    def calculate_last(self, start, birthday, code, No17):
        foidlist = []
        for i in list(start): foidlist.append(string.atoi(i))
        for i in list(birthday): foidlist.append(string.atoi(i))
        for i in list(code): foidlist.append(string.atoi(i))
        foidlist.append(string.atoi(No17))
        numlist = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        sum = 0
        for i in range(0, 17):
            sum = sum + foidlist[i] * numlist[i]
        finallist = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        return finallist[sum % 11]

    def create_paxs_id(self, start, birthday, sex):
        No17 = self.transform_sex(sex)
        No18 = self.calculate_last(start, birthday, '05', No17)
        foid = start + birthday + '05' + No17 + No18
        return foid

    def str_list(self, bpdict, *bpnames):

        bpId_list = []
        bpName_list = []
        for bp in bpdict:
            for bpname in bpnames:
                if bp['bpName'] == bpname:
                    bpId_list.append(str(bp['bpId']))
                    bpName_list.append(bp['bpName'])
        if bpId_list != []:
            bpIds = ','.join(bpId_list)
            bpNames = ','.join(bpName_list)
            return bpIds, bpNames

        else:
            return '未找到对应企业商户！'

    def get_dict_mes(self, list_dict, mes, key, *parms):

        L = []
        for parm in parms:
            for dict_mes in list_dict:
                if dict_mes[key] == parm:
                    L.append(dict_mes[mes])

        return L

    def rd_phone(self):
        numb = random.randint(10000, 100000)
        phone = '139388' + str(numb)
        return phone


    def rd_str(self):
        str1 = []
        for i in range(6):
            numb = random.choice(list(range(10)) + list(range(97, 122)))
            if numb > 10:
                str1.append(chr(numb))
            else:
                str1.append(str(numb))

        str1 = ''.join(str1)
        return str1

    def pinyin(self,word):
        s = ''
        for p in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(p)
        return s

    def should_contain_as_lower(self,str1,str2):

        if str2.lower() in str1.lower():
            return True
        else:
            raise ValueError('%s不包含%s'%(str1,str2))


    def search_chatid(self,chat_dict,name):
        """
        找出单聊对话窗口
        :param chat_dict:所有对话窗口字典
        :param name1: 用户1名称
        :param name2: 用户2名称
        :return:
        """
        for pic in chat_dict:
            print(pic)
            pic_list = []
            pic_dict = json.loads(pic['pic'])
            for usermes in pic_dict:
                try:
                    pic_list.append(usermes['name'])
                except Exception:
                    pass
            if name in pic_list and len(pic_dict)<=2:
                return pic['chatId']

        else:
            raise ValueError('未找到窗口！')


    def get_value(self,msg_dict,key,value):
        """
        获取字典是否有对应的key,有的话返回对应值否则返回定义的值
        :param msg_dict:
        :param key:
        :param value:
        :return:
        """
        if not msg_dict.get(key):
            return value
        else:
            return msg_dict.get(key)