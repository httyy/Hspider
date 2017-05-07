import threading

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
                if self.master.url_buffer.qsize() != 0:
                    while self.master.url_queue.full() == False:
                        if self.master.url_buffer.empty() == True:
                            break
                        else:
                            ret = self.master.url_buffer.get()
                            self.master.url_queue.put(ret)
                else:
                    pass
            else:
                pass

    def stop(self):
        if self.is_stopped == False:
            self.is_stopped = True
        else:
            pass


