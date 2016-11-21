# -*- coding: utf-8 -*-

"""
Created on 2016年11月13日

@author: kerry
"""

from analysis.base.threadpool import ThreadPool,NoResultsPending,makeRequests
from analysis.base.mlog import mlog

class ThreadPoolManager:

    """
    classdocs
    """
    def __init__(self, num):
        self.pool = ThreadPool(num)

    def create_task(self, content, task_run, stop_run, except_run):
        requests = makeRequests(task_run, content, stop_run, except_run)
        for req in requests:
            self.pool.putRequest(req)

    def run(self):
        while True:
            try:
                self.pool.poll()
            except KeyboardInterrupt:
                mlog.log().error("**** Interrupted!")
                break
            except NoResultsPending:
                mlog.log().error("**** No pending results.")
                break

        if self.pool.dismissedWorkers:
            mlog.log().info("Joining all dismissed worker threads...")
            self.pool.joinAllDismissedWorkers()