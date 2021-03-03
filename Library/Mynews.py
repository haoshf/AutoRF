import json

class Mynews(object):


    def __init__(self):
        pass

    def Mynews(self,receiverId):
        """
        我的会议
        :param timestamp:
        :param startTime:
        :param endTime:
        :return:
        """
        news_mes ={
                "pageNum": 1,
                "pageSize": 3,
                "paramMap": {
                    "title": {
                        "name": "title",
                        "value": ""
                    },
                    "receiverId": {
                        "name": "receiverId",
                        "value": receiverId
                    },
                    "isReaded": {
                        "name": "isReaded",
                        "value": ""
                    },
                    "status": {
                        "name": "status",
                        "value": 2
                    }
                }
            }
        return json.dumps(news_mes)