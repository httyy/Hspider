import random
from .conf import *
import re
from pyquery import PyQuery as pq
import pymysql

def random_useragent() :
	return CONF_USERAGENT[random.randint(0,len(CONF_USERAGENT)-1)]

def url_trip(item) :
	if SETTING['trip'] != [] :
		for order in SETTING['trip'] :
			if not re.match(order['old'],item) :
				pass
			else :
				res = re.findall(order['new'],item)
				return res[0]

	return item


#获得一个网页中所有a标签中的链接地址
def get_all_a(content) :
	info = pq(content)
	a_list = info('a')
	a_list = [str(item.attr('href')).strip() for item in a_list.items()]

	temp_list = list()
	for item in a_list :
		if not re.match('^/.*',item) :
			pass
		else :
			item = SETTING['baseurl'] + item
		temp_list.append(item)

	result_list = list()
	for item in temp_list :
		if not re.match('^(http|https)://.*',item) :
			pass
		else :
			result_list.append(item)

	return result_list

#获得一个网页中所有a标签中的符合规则的链接地址
def get_all_match_a(content) :
	a_list = get_all_a(content)

	temp_list = list()

	if SETTING['white'] != [] :
		for item in a_list :
			for url in SETTING['white'] :
				if not re.match(url,item) :
					pass
				else :
					temp_list.append(item)
					break
	else :
		temp_list = a_list

	result_list = list()
	if SETTING['black'] != [] :
		for item in temp_list :
			count = 0
			for url in SETTING['black'] :
				if not re.match(url,item) :
					count += 1
				else :
					pass
			if count == len(SETTING['black']) :
				result_list.append(item)
	else :
		result_list = temp_list

	return result_list

def is_match(item) :
	if SETTING['match'] != [] :
		for url in SETTING['match'] :
			if not re.match(url,item) :
				pass
			else :
				return True

	return False

def exec_sql(sql,connect,arg = None) :
	try :
		with connect.cursor() as cursor :
			result = cursor.execute(sql,arg)
		connect.commit()
	except :
		print('sql err')
		raise

	return result

def get_sql(sql,connect,arg = None) :
	try :
		with connect.cursor() as cursor :
			cursor.execute(sql,arg)
			result = cursor.fetchone()
		connect.commit()
		return result
	except :
		print('sql err')
		raise

def get_count_sql(sql,connect,arg = None) :
	try :
		with connect.cursor() as cursor :
			cursor.execute(sql,arg)
			result = cursor.fetchone()
		connect.commit()
		return int(result['count(*)'])
	except :
		print('sql err')

if __name__ == '__main__' :
	# print(is_match('https://movie.douban.com/subject/25937854/?from=showing'))
	print(url_trip('https://movie.www.b'))