import requests
import re
from pyquery import PyQuery as pq

def get_proxy_100() :
	headers = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"}
	url = 'http://api.xicidaili.com/free2016.txt'

	try :
		res = requests.get(url,headers = headers,timeout = 3)
	except requests.exceptions.ConnectTimeout :
		print('connect err')
		return None
	except requests.exceptions.Timeout :
		print('Timeout')
		return None

	if res.status_code != 200 :
		print('requests err , status_code : %d' % res.status_code)
		return None

	result = re.findall('\d+\.\d+\.\d+\.\d+:\d+',res.text)

	result = test_proxy(result)

	return result

def get_proxy_xici() :
	headers = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"}
	urls = []
	for i in range(1,11) :
		# url = 'http://www.xicidaili.com/nn/%d'%i
		url = 'http://www.xicidaili.com/wn/%d'%i
		urls.append(url)

	proxy_list = []

	for url in urls :
		try :
			res = requests.get(url,headers = headers,timeout = 3)
		except requests.exceptions.ConnectTimeout :
			print('connect err : %s'%url)
			continue
		except requests.exceptions.Timeout :
			print('Timeout : %s'%url)
			continue

		if res.status_code != 200 :
			print('status_code : %d url : %s' % (res.status_code,url))
			continue

		info = pq(res.text)
		tr_list = info('#ip_list tr:gt(0)')
		for item in tr_list.items() :
			td_ip = item('td:eq(1)')
			ip = td_ip.html()
			td_port = item('td:eq(2)')
			port = td_port.html()

			proxy ='%s:%s'%(ip,port)
			proxy_list.append(proxy)

	return proxy_list

def get_proxy() :
	# headers = {'Host':'www.kuaidaili.com',
	# 	'Connection':'keep-alive',
	# 	'Cache-Control':'max-age=0',
	# 	'Upgrade-Insecure-Requests':'1',
	# 	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	# 	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	# 	'Accept-Encoding':'gzip, deflate, sdch',
	# 	'Accept-Language':'zh-CN,zh;q=0.8',
	# 	'Cookie':'_gat=1; channelid=0; sid=1493960911982296; _ga=GA1.2.1135830323.1493960693; _gid=GA1.2.678168757.1493961443; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1493960693; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1493961443',
	# 	}
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	}
	urls = []
	for i in range(1,21) :
		# url = 'http://www.xicidaili.com/nn/%d'%i
		# url = 'http://www.kuaidaili.com/free/inha/%d/'%i
		url = 'http://www.httpsdaili.com/free.asp?page=%d'%i
		urls.append(url)

	proxy_list = []

	for url in urls :
		try :
			res = requests.get(url,headers = headers,timeout = 3)
		except requests.exceptions.ConnectTimeout :
			print('connect err : %s'%url)
			continue
		except requests.exceptions.Timeout :
			print('Timeout : %s'%url)
			continue

		if res.status_code != 200 :
			print('status_code : %d url : %s' % (res.status_code,url))
			continue

		info = pq(res.text)
		tr_list = info('table tbody tr.odd')
		for item in tr_list.items() :
			td_ip = item('td:eq(0)')
			ip = td_ip.html()
			td_port = item('td:eq(1)')
			port = td_port.html()

			proxy ='%s:%s'%(ip,port)
			proxy_list.append(proxy)

	return proxy_list


def test_proxy(proxy_list) :
	return proxy_list
	'''
	for proxy in proxy_list :
		print(proxy)
		headers = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"}
		url = 'http://ip.chinaz.com/getip.aspx'
		# url = 'http://www.baidu.com'

		proxies = {
			'http':'http://27.148.151.82:80',
		}

		res = requests.get(url,headers = headers,proxies = proxies,timeout = 3)
		# res = requests.get(url,headers = headers,timeout = 3)

		if res.status_code != 200 :
			print('requests err , status_code : %d' % res.status_code)
			break

		print(res.text)
		break
	'''

def test() :
	headers = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"}
	# url = 'http://ip.chinaz.com/getip.aspx'
	url = 'https://movie.douban.com/subject/26387939/'

	proxies = {
			'http':'http://122.237.47.150:808',
		}

	res = requests.get(url,headers = headers,proxies = proxies,timeout = 3)

	print(res.text)


if __name__ == '__main__' :
	get_proxy()

