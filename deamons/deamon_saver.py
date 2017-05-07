import threading
from .conf import *
from .func import *
from pyquery import PyQuery as pq
from collections import OrderedDict
import pymysql
import logging
import json

class deamon_saver(threading.Thread) :
	def __init__(self,name = 'deamon_saver',master = None) :
		super(deamon_saver,self).__init__(name = name)
		self.master = master
		self.is_stopped = True
		self.sql_init()

	def sql_init(self) :
		connect = pymysql.connect(**self.master.sqlconf)
		self.connect = connect

	def run(self) :
		if self.is_stopped == True :
			self.is_stopped = False
		else :
			pass

		while self.is_stopped == False :
 			if self.master.content_buffer.qsize() != 0 :
 				content = self.master.content_buffer.get()
 				self.save(content)
 			else :
 				pass

	def save(self,content) :
		info = pq(content)
		info = info('div#content')

		#电影名
		name = info('h1 span:eq(0)').html()

		#电影年份
		year = info('h1 span:eq(1)').html()
		year = re.findall('\d+',year)[0]

		#电影图片
		img = info('div#mainpic').find('img').attr('src')

		#电影信息
		message = info('div#info').html()
		dr = re.compile(r'<[^>]+>',re.S)
		message = dr.sub('',message)
		message = message.strip()
		message = message.split('\n')
		mes_list = list()
		imdb = ''

		for item in message :
			item = item.strip()

			if not re.match('官方小站',item) :
				pass
			else :
				break

			if item != '' :
				mes_list.append(item)
				if not re.match('IMDb链接',item) :
					pass
				else :
					imdb = re.findall('IMDb链接:(.*)',item)[0]
					imdb = imdb.strip()
			else :
				pass

		data = OrderedDict()
		for line in mes_list :
			item = line.split(':')

			if len(item) > 1 :
				head = item[0].strip()
				footer = item[1].strip()
				data[head] = footer
			else :
				pass

		j_data = json.dumps(data,ensure_ascii = False)

		#电影评分
		rate = info('div.rating_self strong').html()

		#评分人数
		num = info('a.rating_people span').html()

		#星级占比
		start5 = info('div.ratings-on-weight div.item:eq(0) span.rating_per').html()
		start4 = info('div.ratings-on-weight div.item:eq(1) span.rating_per').html()
		start3 = info('div.ratings-on-weight div.item:eq(2) span.rating_per').html()
		start2 = info('div.ratings-on-weight div.item:eq(3) span.rating_per').html()
		start1 = info('div.ratings-on-weight div.item:eq(4) span.rating_per').html()
		start = OrderedDict()
		start['5'] = start5
		start['4'] = start4
		start['3'] = start3
		start['2'] = start2
		start['1'] = start1

		j_start = json.dumps(start,ensure_ascii = False)

		isql = 'insert into movies values(NULL,%s,%s,%s,%s,%s,%s,%s,%s)'
		iarg = (name,year,img,imdb,j_data,j_start,rate,num)
		exec_sql(isql,iarg,self.connect)
		logging.info('[*] Save a item')

	def stop(self) :
		if self.is_stopped == False :
			self.is_stopped = True
		else :
			pass

		self.connect.close()

if __name__ == '__main__' :
	a = deamon_saver()
	a.sql_init()
