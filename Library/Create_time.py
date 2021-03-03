import datetime
import time
import re

class Create_time(object):


    def __init__(self):pass

    def now_time(self):
        """
        获取当前时间
        :return:
        """
        now = datetime.datetime.now()
        n_t = str(now).replace('-','').replace(':','').replace('.',' ')[:-3]
        return n_t

    def now_timestamp(self):
        t = time.time()
        print(int(t*1000))
        return int(t*1000)

    def set_date(self,delayed_days):
        '''
        Method Name:handle_date
        Method statement: The date of leaving has been selected; Input a delayed day and the date of return would decided automatically
        Method requires parameters: delayed_days
        :param delayed_days: This parameter must be the type of int
        '''
        delayed_days = int(delayed_days)
        final_date = (datetime.datetime.now() + datetime.timedelta(days=delayed_days))
        return final_date.strftime('%Y-%m-%d')

    def set_timestamp(self,delayed_days):

        st = self.set_date(delayed_days)
        timeArray = time.strptime(st, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp*1000

    def add_date(self,date,delayed_days):

        delayed_days = int(delayed_days)
        final_date = (datetime.datetime.strptime(date,'%Y-%m-%d') + datetime.timedelta(days=delayed_days))
        return final_date.strftime('%Y-%m-%d')

    def set_time(self,delta_times):
        delta_times = int(delta_times)
        final_date = (datetime.datetime.now() + datetime.timedelta(minutes=delta_times))
        times = re.split(' |\.',str(final_date))
        return times[1]

    def set_week(self,delayed_days):
        '''
        Method Name:handle_date
        Method statement: The date of leaving has been selected; Input a delayed day and the date of return would decided automatically
        Method requires parameters: delayed_days
        :param delayed_days: This parameter must be the type of int
        '''
        delayed_days = int(delayed_days)
        final_date = (datetime.datetime.now() + datetime.timedelta(days=delayed_days))
        return final_date.weekday()