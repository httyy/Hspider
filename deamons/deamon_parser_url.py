import threading
from .func import *
import logging

class deamon_parser_url(threading.Thread) :
	def __init__(self,name = 'deamon_parser_url',master = None) :
		super(deamon_parser_url,self).__init__(name = name)
		self.master = master
		self.is_stopped = True

	def run(self) :
		if self.is_stopped == True :
			self.is_stopped = False
		else :
			pass

		while self.is_stopped == False :
			for _worker in self.master.workers :
				if _worker.is_finished == True :
					url = _worker.content[0]['url']
					deep = _worker.content[0]['deep']

					if self.deep_trip(url) :
						deep = 2
					else :
						pass

					content = _worker.content[1]
					self.add_url(url,deep,content)

					_worker.reset()
					_worker.is_finished = False
				else :
					pass

	def add_url(self,url,deep,content) :
		if deep < self.master.max_deep or self.master.max_deep == 0 :
			a_list = get_all_match_a(content)

			b_list = list()
			for item in a_list :
				if self.master.bitmap.is_exit(item) == False :
					self.master.bitmap.insert(item)
					b_list.append(item)
				else :
					pass

			self.save_url(b_list,deep)
			logging.info('[@] Add url from %s : %d' %(url,len(b_list)))
		else :
			pass

		if is_match(url) :
			logging.info('[*] Match url : %s ' % url)
			self.master.content_buffer.put(content)

	def deep_trip(self,url) :
		if not re.match(SETTING['deep'],url) :
			return False
		else :
			return True

	def save_url(self,url_list,deep) :
		for url in url_list :
			url = url_trip(url)
			isql = 'insert into urls values(NULL,%s,%s,0)'
			iarg = (url,deep+1)
			self.master.lock.acquire()
			exec_sql(sql = isql,arg = iarg,connect = self.master.connect)
			self.master.lock.release()

	def stop(self) :
		if self.is_stopped == False :
			self.is_stopped = True
		else :
			pass
