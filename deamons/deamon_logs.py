import threading
import time
import logging

class deamon_logs(threading.Thread) :
	def __init__(self,name = 'deamon_logs',master = None) :
		super(deamon_logs,self).__init__(name = name)
		self.master = master
		self.is_stopped = True

	def run(self) :
		if self.is_stopped == True :
			self.is_stopped = False
		else :
			pass

		while self.is_stopped == False :
			self.status()
			time.sleep(1)

	def status(self) :
		logging.info('[$] Parser : %d Save : %d'%(self.master.deamon_parser_url.is_stopped,self.master.deamon_saver.is_stopped))
		logging.info('[$] url_queue : %d url_buffer : %d content_buffer : %d'%(self.master.url_queue.qsize(),self.master.url_buffer.qsize(),self.master.content_buffer.qsize()))

	def stop(self) :
		if self.is_stopped == False :
			self.is_stopped = True
		else :
			pass
