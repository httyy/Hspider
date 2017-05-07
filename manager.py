import threading
import deamons
import logging
import time
import pymysql
from queue import Queue

class Manager(threading.Thread) :
	def __init__(self,thread_size = 1,task_size = 10,max_deep = 0,setting = {},sqlconf = {}) :
		super(Manager,self).__init__()
		self.thread_size = thread_size
		self.task_size = task_size
		self.max_deep = max_deep

		self.sqlconf = sqlconf

		self.bitmap = deamons.BloomFilter()

		self.url_buffer = Queue()
		self.content_buffer = Queue()
		self.url_queue = Queue(task_size)

		self.is_stopped = True
		self.is_all_dead = False

		self.__init_logs()

		self.workers = []
		self.__init_workers()

		self.proxy_list = []
		self.__init_proxy()

		self.deamon_task_queue = deamons.deamon_task_queue(master = self)
		self.deamon_all_dead = deamons.deamon_all_dead(master = self)
		self.deamon_parser_url = deamons.deamon_parser_url(master = self)
		self.deamon_saver = deamons.deamon_saver(master = self)
		# self.deamon_logs = deamons.deamon_logs(master = self)

	def __init_workers(self) :
		if self.workers == [] :
			for i in range(self.thread_size) :
				_worker = deamons.worker(name = "M-%d" % i,master = self)
				_worker.start()
				self.workers.append(_worker)
			logging.debug('[*] Create %d workers' % self.thread_size)
		else :
			logging.debug('[!] Init the workers failed')

	def __init_proxy(self) :
		self.proxies = deamons.get_proxy_xici()
		logging.debug('[!] Get prxoy : %s'%len(self.proxies))

	def __init_logs(self) :
		logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s : %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='logs.txt',
        filemode='w')

		console = logging.StreamHandler()
		console.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)

	def run(self) :
		if self.is_stopped == True :
			self.is_stopped = False
		else :
			pass

		logging.info('[!] Spider is starting')

		self.deamon_parser_url.start()
		self.deamon_saver.start()
		self.deamon_task_queue.start()
		self.deamon_all_dead.start()
		# self.deamon_logs.start()

		while  self.is_stopped == False :
			for _worker in self.workers :
				if _worker.url == None :
					if  _worker.is_finished == False :
						if self.url_queue.qsize() != 0 :
							_worker.url = self.url_queue.get()
					else :
						pass
				else :
					pass

			if self.is_all_dead == True :
				break

		self.deamon_parser_url.stop()
		self.deamon_saver.stop()
		self.deamon_task_queue.stop()
		self.deamon_all_dead.stop()
		# self.deamon_logs.stop()

		for worker in self.workers :
			worker.stop()

		logging.info('[!] All done')

	def execute(self,urls) :
		for url in urls :
			self.url_queue.put({'url':url,'deep':0})

		self.start()

if __name__ == '__main__' :

	sqlconf = {
        'host':'localhost',
        'port':3306,
        'user':'root',
        'password':'',
        'db':'spider',
        'charset':'utf8',
        'cursorclass':pymysql.cursors.DictCursor,
	}

	start_urls = ['https://movie.douban.com/tag/',
	]

	spider = Manager(sqlconf = sqlconf,thread_size = 2,max_deep = 4)
	spider.execute(start_urls)
