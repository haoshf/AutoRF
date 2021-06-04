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

    def real_log(self,instanceId,detail,receiverList,isSendPrivateChat,**kwargs):

        print('zzzzz',receiverList,isSendPrivateChat)
        real_mes ={
            "defineTitle": "",
            "defineId": "",
            "reportType": "",
            "deadline": "",
            "formBizData": {},
            "isSendPrivateChat": "0",
            "groupChatData": "",
            "optionalRecipient": "",
            "designatedRecipient": "",
            "files": [],
            "reportDate": "",
            "instanceId":"",
            "receiverList": []
        }

        for k,v in real_mes.items():
            print(k)
            for k1,v1 in detail.items():
                if k == k1 and v1:
                    real_mes[k]=v1

        for key,value in kwargs.items():
            for item in detail['formDefine']['list']:
                if key == item['label']:
                    real_mes['formBizData'][item['itemId']] = value

        real_mes['receiverList']=list(receiverList)
        real_mes['isSendPrivateChat']=isSendPrivateChat
        if instanceId != '':
            real_mes['instanceId'] = instanceId

        return json.dumps(real_mes)