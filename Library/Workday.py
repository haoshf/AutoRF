import datetime
import time
import calendar


class Workday(object):

    def __init__(self):pass

    def date_days(self,date):
        dates = time.strptime(date, "%Y-%m-%d")
        dates = datetime.datetime(dates[0], dates[1], dates[2])
        return dates

    def Calworkday(self,start_date1,end_date1,start_date2,end_date2):

        date1 = self.date_days(start_date1)#假期开始
        date2 = self.date_days(end_date1)#假期结束
        date3 = self.date_days(start_date2)#考勤起始
        date4 = self.date_days(end_date2)#考勤结束
        days1 = (date3-date1).days
        days2 = (date4-date2).days
        days3 = (date3-date2).days
        days4 = (date4-date1).days
        #范围外
        days = 0
        if days3>0 or days4<0:
            days = 0

        #假期始终都在考勤内
        elif days1 <= 0 and days2 >= 0:
            days = (date2-date1).days+1

        #假期开始在考勤外，结束在考勤内
        elif days1 >= 0 and days2 >= 0:
            days = (date2-date3).days+1

        #假期开始在考勤内，结束在考勤外
        elif days1 <= 0 and days2 <= 0:
            days = (date4-date1).days+1

        return days

    def holi_work(self,datelist,year_month):

        start_date2=year_month+'01'
        end_date2=year_month+str(calendar.monthrange(int(year_month[:4]),int(year_month[5:7]))[1])
        holi_days = 0
        for date in datelist['pageData']['list']:
            start_date1 = date['startTime']
            end_date1 = date['endTime']

            holi_day = self.Calworkday(start_date1,end_date1,start_date2,end_date2)
            if holi_day>holi_days:
                holi_days = holi_day
        return holi_days

    def work_days(self,year_month):
        cal = calendar.monthrange(int(year_month[:4]), int(year_month[5:7]))
        yu_s = cal[1] % 7
        if 6>= cal[0] + yu_s >= 5 and cal[0]<5:
            days = cal[1]-8-1
        elif cal[0] + yu_s>6 and cal[0]<5:
            days = cal[1] - 8 - 2
        elif cal[0] + yu_s>6 and 6>cal[0]>=5:
            days = cal[1] - 8 - 2
        elif cal[0] + yu_s>6 and cal[0] > 5:
            days = cal[1] - 8 - 1
        else:
            days = cal[1] - 8
        return days

    def mondays(self,year_month):

        return calendar.monthrange(int(year_month[:4]), int(year_month[5:7]))[1]


    def week_se(self,date):
        if date == '':
            nowdate = datetime.datetime.now()
        else:
            nowdate = datetime.datetime.strptime(date,'%Y-%m-%d')
        startdate = nowdate - datetime.timedelta(days=nowdate.weekday())
        enddate = startdate + datetime.timedelta(days=6)
        return startdate.strftime('%Y-%m-%d'),enddate.strftime('%Y-%m-%d')

    def month_alldays(self,date):

        if date == '':
            date = datetime.datetime.now().strftime('%Y-%m-%d')

        start_date = datetime.datetime.strptime(date[:8]+'01','%Y-%m-%d')
        end_date = datetime.datetime.strptime(date[:8] + str(calendar.monthrange(int(date[:4]), int(date[5:7]))[1]),'%Y-%m-%d')
        print('???????????')
        if end_date.weekday() == 6:
            startdate = start_date
            enddate = end_date + datetime.timedelta(days=5)
        else:
            startdate = start_date - datetime.timedelta(days=start_date.weekday() - 1)
            enddate = end_date + datetime.timedelta(days=5-end_date.weekday())

        return startdate.strftime('%Y-%m-%d'),enddate.strftime('%Y-%m-%d')
