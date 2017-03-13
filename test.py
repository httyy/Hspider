import logging
import sys
import requests
import time
import pymysql.cursors
import re
import queue
import hashlib
from pyquery import PyQuery as pq

global UrlQue
global UrlBase
UrlQue = queue.Queue()

#设置初始的url
def start_url(url,connect) :
	UrlQue.put(url)
	insert_url(url,connect)
	logging.info('config start url : %s',url)

#向数据库中插入新的链接
def insert_url(url,connect) :
	GetRex = re.compile(MatchUrl)

	if not GetRex.match(url) :
		pass
	else :
		result = re.findall('^(https://movie.douban.com/subject/\d+/).*',url)
		url = result[0]

	Md = hashlib.md5(url.encode(encoding = 'utf8'))
	Md5url = Md.hexdigest()

	try :
		with connect.cursor() as cursor :
			sel = "select * from h_url where md5 = %s"
			cursor.execute(sel,(Md5url))
			row = cursor.fetchall()

			if len(row) == 0 :
				ins = "insert into h_url values(NULL,%s,%s)"
				cursor.execute(ins,(url,Md5url))
			else :
				return False

		connect.commit()
	except :
		print('insert err')
		exit()

	return True

#获取页面内容，并判断是否继续抓取
def parse_content(url,connect) :
	UrlRex = re.compile(UrlBase)
	GetRex = re.compile(MatchUrl)

	logging.info('parse url : %s',url)

	if not GetRex.match(url) :

		headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'}
		res = requests.get(url,headers = headers)
		if res.status_code != 200 :
			logging.info('requests err , status_code : %d',res.status_code)
			return

		find_a = pq(res.text)

		a_list = find_a('a')
		b_list = [str(item.attr('href')).strip() for item in a_list.items()]
		c_list = list()

		for item in b_list :
			if not re.match('^/.*',item) :
				pass
			else :
				item = 'https://movie.douban.com' + item
			c_list.append(item)

		insert_num = 0
		for item in c_list :
			if not UrlRex.match(item) :
				pass
			else :
				count = 0
				for rex in FilterList :
					if not re.match(rex,item) :
						count += 1
					else :
						pass

				if count == len(FilterList) :
					if insert_url(item,connect) :
						UrlQue.put(item)
						insert_num += 1

		logging.info("insert new url : %d ",insert_num)

	else :
		save_item(url,connect)


#保存抓取的内容
def save_item(url,connect) :

	headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'}
	res = requests.get(url,headers = headers)

	if res.status_code != 200 :
		logging.info('requests err , status_code : %d',res.status_code)
		return

	info = pq(res.text)

	#获取电影名
	title = info('title').html()
	title = title.replace('\n','')
	title = title.strip()
	result = re.findall(r'(.*)\(豆瓣\)',title)
	name = result[0]

	#获取评分
	grade = info('div.rating_self strong.rating_num').html()

	#获取评论人数
	rate = info('div.rating_sum a span').html()

	try :
		with connect.cursor() as cursor :
			ins = 'insert into items values(NULL,%s,%s,%s)'
			cursor.execute(ins,(name,grade,rate))
		connect.commit()
		logging.info('save a item')
	except :
		print('save err')
		exit()

def test(connect) :

	logging.debug('test start')
	logging.info('start')

	url = 'https://movie.douban.com/subject/6873143/'
	headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'}
	res = requests.get(url,headers = headers)

	info = pq(res.text)

	#获取电影名
	title = info('title').html()
	title = title.replace('\n','')
	title = title.strip()
	result = re.findall(r'(.*)\(豆瓣\)',title)
	name = result[0]

	#获取评分
	grade = info('div.rating_self strong.rating_num').html()

	#获取评论人数
	rate = info('div.rating_sum a span').html()

	try :
		with connect.cursor() as cursor :
			ins = 'insert into items values(NULL,%s,%s,%s)'
			cursor.execute(ins,(name,grade,rate))
		connect.commit()
	except :
		print('save err')
		exit()


if __name__ == '__main__' :

	logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='test.log',
                filemode='w')

	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)

	UrlBase = '^https://movie.douban.com/.*'
	MatchUrl = '^https://movie.douban.com/subject/\d+/[^/]*$'
	Url = 'https://movie.douban.com/'
	FilterList = ['^https://movie.douban.com/subject/\d+/cinema/.*',
					'^https://movie.douban.com/trailer/\d+/.*',
					'^https://movie.douban.com/review/\d+/.*',
					'^https://movie.douban.com/chain/.*',
					'^https://movie.douban.com/feed/.*',]

	config = {
		'host':'localhost',
		'port':3306,
		'user':'root',
		'password':'',
		'db':'spider',
		'charset':'utf8',
		'cursorclass':pymysql.cursors.DictCursor,
	}

	connection = pymysql.connect(**config)

	#测试函数
	#test(connection)
	#exit()

	start_url(Url,connection)

	while not UrlQue.empty() :
		de_url = UrlQue.get()
		parse_content(de_url,connection)
		time.sleep(5)

	print('done')






