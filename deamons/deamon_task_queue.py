import threading
from .func import *

class deamon_task_queue(threading.Thread):
    def __init__(self, master = None, name = "deamon_task_queue"):
        threading.Thread.__init__(self)
        self.master = master
        self.is_stopped = True

    def run(self):
        if self.is_stopped != False:
            self.is_stopped = False

        while self.is_stopped == False:
            if self.master.url_queue.qsize() <= self.master.task_size / 2:
                #print "[^] Prepare to fill the task_queue!"
                while self.master.url_queue.full() == False:
                    if self.task_is_empty() == True:
                        break
                    else:
                        url = self.get_task()
                        self.master.url_queue.put(url)
                        status = 1
                        isql = 'update urls set status = %s where url = %s'
                        iarg = (status,url['url'])
                        self.master.lock.acquire()
                        exec_sql(sql = isql,arg = iarg,connect = self.master.connect)
                        self.master.lock.release()
            else:
                pass

    def task_is_empty(self) :
        isql =  "select count(*) from urls where status = 0"
        self.master.lock.acquire()
        result = get_count_sql(sql = isql,connect = self.master.connect)
        self.master.lock.release()


        if result == 0 :
            return True
        else :
            return False

    def get_task(self) :
        isql = 'select * from urls where status = 0 order by id desc limit 1'
        self.master.lock.acquire()
        result = get_sql(sql = isql,connect = self.master.connect)
        self.master.lock.release()

        return {'url':result['url'],'deep':int(result['deep'])}

    def stop(self):
        if self.is_stopped == False:
            self.is_stopped = True
        else:
            pass

if __name__ == '__main__' :
    pass

