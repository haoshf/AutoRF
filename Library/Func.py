import json
from collections import Iterable


class Func(object):
    def __init__(self):
        pass

    def get_FuncList(self, getAllFuncList, *funcNames):

        funcList = []
        self.fittler_func(funcList, getAllFuncList, *funcNames)
        def func(lst):
            for item in lst['childrens']:
                self.fittler_func(funcList, item, *funcNames)
                if isinstance(item['childrens'], Iterable):
                    func(item)

        func(getAllFuncList)
        return funcList

    def fittler_func(self, funcList, Func, *funcNames):

        for funcname in funcNames:

            if funcname == Func['funcName']:
                func_dict = {}
                func_dict['funcId'] = Func['funcId']
                func_dict['funcName'] = Func['funcName']
                funcList.append(func_dict)

        return
