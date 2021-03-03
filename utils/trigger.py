# -*- coding: utf-8 -*-

__author__ = "苦叶子"

"""

公众号: 开源优测

Email: lymking@foxmail.com

"""

import os
import xml.etree.ElementTree as ET
from apscheduler.schedulers.background import BackgroundScheduler
from flask import url_for
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.sql import func
from dateutil import tz
from repository import models

class Trigger(object):

    def __init__(self, run_job):
        self.scheduler = None
        self.run_job = run_job

    def setup(self):
        self.scheduler = BackgroundScheduler()
        return self.scheduler

    def start(self):

        self.scheduler.start()
        return self.scheduler

    def is_running(self):
        return self.scheduler.running

    def shutdown(self):
        self.scheduler.shutdown()
        return self.scheduler

    def load_job_list(self):
        trigger = models.Trigger.objects.all()

        for p in trigger:
            if p.enable:
                cron = p.Cron.replace("\n", "").strip().split(" ")
                #print(cron)
                if len(cron) < 5:
                    continue
                j = self.scheduler.add_job(func=self.run_job, trigger='cron', replace_existing=True,
                                           second=cron[0], minute=cron[1], hour=cron[2], day=cron[3], month=cron[4],
                                           day_of_week=cron[5],
                                           id="%s" % p.id, args=(p.id,p.user))

        return self.scheduler

    def add_work_job(self,id):
        p = models.Trigger.objects.filter(id=id).first()
        cron = p.Cron.replace("\n", "").strip().split(" ")
        if self.scheduler.get_job(id) is None:
            self.scheduler.add_job(func=self.run_job, trigger='cron', replace_existing=True,
                                   second=cron[0],minute=cron[1], hour=cron[2], day=cron[3], month=cron[4], day_of_week=cron[5],
                                           id="%s" % p.id, args=(p.id,p.user))
        return self.scheduler

    def update_work_job(self, id):
        p = models.Trigger.objects.filter(id=id).first()
        cron = p.Cron.replace("\n", "").strip().split(" ")
        if p.enable:
            if self.scheduler.get_job(id) is None:
                self.scheduler.add_job(func=self.run_job, trigger='cron', name=p.trigger_name, replace_existing=True,
                                               minute=cron[0], hour=cron[1], day=cron[2], month=cron[3], day_of_week=cron[4],
                                               id="%s" % p.id, args=(p.id,p.user))
            else:
                self.remove_job(id)
                self.scheduler.add_job(func=self.run_job, trigger='cron', name=p.trigger_name, replace_existing=True,
                                       second=cron[0], minute=cron[1], hour=cron[2], day=cron[3], month=cron[4],
                                       day_of_week=cron[5],
                                       id="%s" % p.id, args=(p.id,p.user))
        return self.scheduler

    def remove_job(self, id):
        if self.scheduler.get_job(id) is not None:
            self.scheduler.remove_job(id)
        return self.scheduler

    def pause_job(self, id):
        pass

    def resume_job(self, id):
        pass

    def get_jobs(self):
        return self.scheduler.get_jobs()

    def add_job(self):
        return self.scheduler.add_job()