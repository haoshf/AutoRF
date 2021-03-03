#!/usr/bin/env python
# coding=utf-8
__author__ = 'haoshuaifei'
import pymysql
import re

class SqlDB(object):

    def __init__(self):pass

    def connect(self,env_database,*sqls):
        if env_database != '':
            if isinstance(env_database, dict):
                date = re.findall('(\d{4}-\d{1,2}-\d{1,2})', env_database['data']['bpInfo']['createTime'])[0].replace('-','')
                env_database = 'bop2_bp_'+date+'_'+str(env_database['data']['bpInfo']['bpId'])
                conn = pymysql.connect(
                    host='49.4.68.114',
                    user='ceshi',
                    password='Cs@123',
                    database='bop2_test_20191101',
                    charset='utf8',
                    autocommit=True
                )
            else:
                if env_database=='test':
                    env_database = 'bop2_test_20191101'
                else:
                    env_database = 'bop2_operate_test'

                conn = pymysql.connect(
                    host='rm-2zehij2qv9t17w3mrqo.mysql.rds.aliyuncs.com',
                    user='sqladmin',
                    password='iTNnjDKU23&n',
                    database=env_database,
                    charset='utf8',
                    autocommit=True
                )

        else:
            conn = ''
        cursor = conn.cursor()
        f = []
        for sql in sqls:
            print('执行sql', sql)
            try:
                cursor.execute(sql)
                if sql[:6].upper() == 'SELECT':
                    s = cursor.fetchall()
                    f.append(s)
                else:
                    f.append('执行成功！')

            except Exception:
                conn.rollback()
                f.append('执行失败！')

        cursor.close()
        conn.close()
        return f

    # def select_password(self,username,environment):
    #     """
    #     查询数据库中的password
    #     :param username:
    #     :return:
    #     """
    #     sql = "SELECT password FROM acc_user where code='%s' AND deleted='0';"%username
    #     L = self.connect(sql,environment)
    #     return L[0][0]


    def update_meetingdate(self,env_database,reserve_id,up_date):
        """
        更新会议时间
        :param env_database:
        :param reserve_id:
        :param up_date:
        :return:
        """
        sql = "update  meeting_reserve set scheduled_start_date='{0}',scheduled_end_date='{0}' where reserve_id='{1}';".format(up_date,reserve_id)
        f = self.connect(env_database,sql)
        return f

    def update_order(self,env_database,order_no,order_status,pay_time):
        """
        更新应用订单状态
        :param env_database:
        :param order_no:
        :param order_status:
        :param pay_time:
        :return:
        """
        sql = "update  bp_application_order set order_status='{0}', pay_time='{1}' where order_no='{2}';".format(order_status,pay_time,order_no)

        f = self.connect(env_database,sql)
        return f

    def update_cz_order(self,env_database,order_no,order_status):
        """
        更新充值订单状态
        :param env_database:
        :param order_no:
        :param order_status:
        :return:
        """
        sql = "update  operate_comm_recharge_log set order_status='{0}' where order_no='{1}';".format(order_status,order_no)

        f = self.connect(env_database,sql)
        return f

    def del_kq(self,env_database,id):
        """
        删除考勤记录
        :param env_database:
        :param id:
        :return:
        """
        sql = "delete from hr_att_record where id='{0}';".format(id)

        f = self.connect(env_database,sql)
        return f

    def del_kq_bk(self,env_database,id):
        """
        删除考勤记录，考勤审批记录
        :param env_database:
        :param staff_id:
        :param create_time:
        :return:
        """
        sql = "SELECT staff_id,create_time From hr_att_record where id='{0}';".format(id)
        f1 = self.connect(env_database,sql)
        sql2 = "SELECT leave_id from hr_att_record_examine where staff_id='{0}' and TO_DAYS( start_time ) = TO_DAYS('{1}');".format(f1[0][0][0],f1[0][0][1])
        f2 = self.connect(env_database,sql2)
        sql3= "SELECT inst_id from hr_att_record_examine where  leave_id = '{0}';".format(f2[0][0][0])
        f3 = self.connect(env_database,sql3)
        inst = tuple([x[0] for x in f3[0]])
        sql6 = "delete from hr_att_record where id='{0}';".format(id)
        sql5 = "delete from hr_att_record_examine where leave_id = '{0}';".format(f2[0][0][0])
        sql4 = "delete From hr_att_record_census WHERE inst_id in {0};".format(inst)
        f = self.connect(env_database,sql4,sql5,sql6)
        return f

    def up_kq_dt(self,env_database,id,schedule_on_time,schedule_off_time,attendance_date,work_hours):
        """
        更新考勤时间且正常打卡
        :param env_database:
        :param staff_id:
        :param create_time:
        :return:
        """
        sql = "UPDATE hr_att_record set schedule_on_time='{1}', schedule_off_time='{2}', attendance_date='{3}' where id='{0}';".format(id,schedule_on_time,schedule_off_time,attendance_date)
        sql2 = "UPDATE hr_att_record set register_on_time=schedule_on_time, register_off_time=schedule_off_time, register_on_status=1, register_off_status=1, fact_work_hours={1}  where id='{0}';".format(id,work_hours)
        f = self.connect(env_database,sql,sql2)
        return f

    def up_kq_zt(self,env_database,id,register_on_time,register_on_status,register_off_time,register_off_status):
        """
        更新考勤状态
        :param env_database:
        :param staff_id:
        :param create_time:
        :return:
        """
        if register_on_time=='null':
            sql = "UPDATE hr_att_record set register_off_time='{1}', register_off_status={2} where id='{0}';".format(id, register_off_time, register_off_status)
        elif register_off_time=='null':
            sql = "UPDATE hr_att_record set register_on_time='{1}', register_on_status={2} where id='{0}';".format(id, register_on_time, register_on_status)
        else:
            sql = "UPDATE hr_att_record set register_on_time='{1}', register_on_status={2}, register_off_time='{3}', register_off_status={4} where id='{0}';".format(id,register_on_time,register_on_status,register_off_time,register_off_status)
        f = self.connect(env_database,sql)
        return f

    def add_kq_yy(self,env_database,id,reason):

        sql = "SELECT bp_id,create_time From hr_att_record WHERE id='{0}';".format(id)
        f = self.connect(env_database,sql)

        sql2 = "INSERT INTO hr_att_record_census VALUES(null,{0},{1},'{2}','1.0','{3}',NULL, NULL, '0')".format(f[0][0][0],id,f[0][0][1],reason)
        f = self.connect(env_database,sql2)
        return f

    def del_kq_yy(self,env_database,id):

        sql = "delete From hr_att_record_census WHERE att_id='{0}';".format(id)
        f = self.connect(env_database,sql)
        return f
