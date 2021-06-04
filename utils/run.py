import time
import json
import subprocess
from datetime import datetime
from threading import Thread, Timer
import xml.etree.ElementTree as ET
from sqlalchemy import and_
from utils.building import Building
import platform,codecs,os

class Runner(object):
    def __init__(self):
        self._process = None
        self._error = None
        self._out_file = None
        self._out_path = None
        self._out_fd = None

    def run(self,work_dir):

        shell = False
        # if "Windows" in platform.platform():
        argfile = work_dir + "argfile.txt"
        print('work_dir',work_dir)
        print('argfile',argfile)
        command = "robot -d {0} --argumentfile {1} {0}" .format(work_dir,argfile)
        shell = True
        self._out_fd = open(work_dir + "run.log", "w")
        self._process = subprocess.Popen(command, shell=shell, stdout=self._out_fd, stderr=subprocess.STDOUT)
        print(self._process)
        return self._process

    def run_project(self,project_id):
        work_dir = Building().build_project(project_id)
        self._process = self.run(work_dir)
        return self._process

    def run_suite(self,suite_ids):
        work_dir = Building().build_suite(suite_ids)
        if work_dir:
            self._process = self.run(work_dir)
            return self._process
        else:
            return False

    def run_case(self,caseids):
        self._process = self.run(work_dir)
        return self._process

    def get_output(self, wait_until_finished=False):
        if self._error:
            self._close_outputs()
            return self._error

        if wait_until_finished:
            self._process.wait()
        output = self._out_file.read()

        if self.is_finished():
            self._close_outputs()

        return output

    def is_finish(self):
        return self._error is not None or self._process.poll() is not None

    def stop(self):
        self._process.kill()

    def wait(self):
        if self._process is not None:
            self._process.wait()

    def _close_outputs(self):
        self._out_file.close()
        os.close(self._out_fd)
        self._remove_tempfile()

    def _remove_tempfile(self, attempts=10):
        try:
            os.remove(self._out_path)
        except OSError:
            if not attempts:
                raise
            time.sleep(1)
            self._remove_tempfile(attempts - 1)