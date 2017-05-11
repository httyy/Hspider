﻿import threading
import time
from .func import *

class deamon_all_dead(threading.Thread):
    def __init__(self, name = "deamon_all_dead", master = None):
        threading.Thread.__init__(self, name = name)
        self.master = master
        self.is_stopped = True
        self.workers_all_done = False
        self.tasks_all_done = False
        self.dead_count = 0

    def run(self):
        if self.is_stopped == True:
            self.is_stopped = False
        while self.is_stopped == False:
            if self.master.url_queue.qsize() == 0:
                if self.task_is_empty == 0:
                    """Check If All Tasks Done!"""
                    if self.tasks_all_done == False:
                        self.tasks_all_done = True
                    else :
                        pass

                    """Check If All Threads Working"""
                    i = 0
                    for thread in self.master.workers:
                        if thread.is_working == True:
                            pass
                        else:
                            i = i + 1
                    if i == self.master.thread_size:
                        if self.workers_all_done == False:
                            self.workers_all_done = True
                        else :
                            pass
                    else :
                        i = 0
                        if self.workers_all_done == True:
                            self.workers_all_done = False
                        else:
                            pass
                else:
                    if self.tasks_all_done == True:
                        self.tasks_all_done = False
                    else:
                        pass
                    if self.workers_all_done == True:
                        self.workers_all_done = False
                    else:
                        pass
            else:
                if self.tasks_all_done == True:
                    self.tasks_all_done = False
                else :
                    pass
                if self.workers_all_done == True:
                    self.workers_all_done = False
                else:
                    pass


            if self.tasks_all_done == True:
                if self.workers_all_done == True:
                    self.dead_count = self.dead_count + 1
                else:
                    if self.dead_count != 0:
                        self.dead_count = 0
                    else:
                        pass
            else:
                if self.dead_count != 0:
                    self.dead_count = 0
                else:
                    pass

            if self.dead_count > 0:
                time.sleep(1.5)
            else:
                time.sleep(3)

            if self.dead_count >= 3:
                if self.master.is_all_dead == False:
                    self.master.is_all_dead = True
                else:
                    pass
            else:
                pass
    def task_is_empty(self) :
        isql = 'select * from urls order by id desc where status = 0 limit 1'
        result = get_sql(sql = isql,connect = self.master.connect)
        return (result['url'],int(result['deep']))

    def stop(self):
        if self.is_stopped == False:
            self.is_stopped = True
        else:
            pass


