import json

class WriteLog(object):


    def __init__(self):
        pass

    def WriteLog(self,FormRecord,**kwargs):

        Form_mes = {
                "formId": FormRecord["formRecord"]["formId"],
                "recordId": "",
                "actionId": "",
                "itemList":FormRecord["formRecord"]["itemList"],
                # "groupList": FormRecord["data"]["formRecord"]["groupList"],
                "type": 0
            }


        for key, value in kwargs.items():
            for i in range(len(Form_mes["itemList"])):
                if key == Form_mes["itemList"][i]["itemTitle"]:
                    if key == "日志接收人":
                        L = []
                        for v in value:
                            p = {}
                            p["id"] = v["id"]
                            p["name"] = v["name"]
                            L.append(p)
                        value = json.dumps(L)
                    elif key in ["图片","附件"]:
                        L = []
                        for v in value:
                            p = {}
                            p["fileName"] = v["fileName"]
                            p["orgFileName"] = v["orgFileName"]
                            L.append(p)
                        value = json.dumps(L)
                    elif key == "工作内容类别":
                        L = []
                        L2 = []
                        for v in Form_mes["itemList"][i]["props"]["options"]:
                            options = {}
                            p = {}
                            p["id"] = v["optionId"]
                            p["values"] = v["optionName"]
                            options["value"] = p
                            options["label"] = v["optionName"]
                            if v["optionName"] != "其他":
                                options["children"] = v["children"]
                            options["__label"] = v["optionName"]
                            options["__value"] = p
                            L.append(options)
                            if value == v["optionName"]:
                                L2.append(p)
                        Form_mes["itemList"][i]["props"]["options"] = L
                        value = json.dumps(L2)

                    Form_mes["itemList"][i]["values"] = value
                    Form_mes["itemList"][i]["values"] = value

        return json.dumps(Form_mes)