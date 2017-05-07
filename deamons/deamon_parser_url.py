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
						deep = 1
					else :
						pass

					content = _worker.content[1]
					url = url_trip(url)

					if self.master.bitmap.is_exit(url) == False :
						self.master.bitmap.insert(url)
						self.addurl(url,deep,content)
					else :
						pass
					_worker.reset()
					_worker.is_finished = False
				else :
					pass

	def addurl(self,url,deep,content) :
		logging.info('[*] Add url : %s ' % url)

		if deep < self.master.max_deep or self.master.max_deep == 0 :
			a_list = get_all_match_a(content)
			for item in a_list :
				self.master.url_buffer.put({'url':item,'deep':deep + 1})
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

	def stop(self) :
		if self.is_stopped == False :
			self.is_stopped = True
		else :
			pass



