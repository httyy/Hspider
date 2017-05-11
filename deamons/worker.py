import threading
import requests
import logging
import random
import time
from .func import *

class worker(threading.Thread):
    def __init__(self, master = None, name = None, handler = None):
        super(worker,self).__init__(name = name)
        self.master     = master
        self.url        = None
        self.is_stopped = True
        self.content = None

        self.is_finished = False
        self.is_working = False

    def run(self) :
        if self.is_stopped == True :
            self.is_stopped = False
        else :
            pass
        while self.is_stopped == False :
            if self.is_finished == False :
                if self.url == None :
                    if self.is_working == True :
                        self.is_working = False
                        continue
                if self.url != None :
                    if self.is_working == False :
                        self.is_working = True
                    result = self.analyze()

                    if result == 1 :
                        self.is_working = False
                        self.is_finished = True
                    else :
                        pass
                    self.url = None
                else :
                    pass
                if self.is_working == True :
                    self.is_working = False
                else :
                    pass
            else :
                pass

    def analyze(self) :
        headers = {'User-Agent':random_useragent(),
            'Connection':'keep-alive',
            'Cache-Control':'max-age=0',
            'Upgrade-Insecure-Requests':'1',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
        }
        repate = 0
        while repate < 3 :
            proxy = self.master.proxies[random.randint(0,len(self.master.proxies)-1)]
            logging.debug('[!] Proxy : %s' % proxy)
            proxies = {
                'http':'http://' + proxy
            }
            try :
                res = requests.get(self.url['url'],headers = headers,proxies = proxies,timeout = 3)
            except requests.exceptions.ConnectTimeout :
                logging.info('ConnectTimeout : %s repate : %d' % (self.url['url'],repate))
                repate += 1
                continue
            except requests.exceptions.Timeout :
                logging.info('Timeout : %s repate : %d' %(self.url['url'],repate))
                repate += 1
                continue
            except requests.exceptions.ProxyError :
                logging.info('Proxy Error : %s'%proxy)
                self.master.proxies.remove(proxy)
                continue
            except BaseException :
                logging.info('[worker]Unkown Error url : %s'%self.url['url'])
                return 0
            if res.status_code != 200 :
                logging.info('status_code : %d url : %s ip : %s repate : %d' % (res.status_code,self.url['url'],proxy,repate))
                repate += 1
            else :
                repate = 0
                break
        if repate == 3 :
            return 0
        self.content = (self.url,res.text)
        logging.info('[&] Get content : %s ' % self.url['url'])
        time.sleep(2)
        return 1

    def stop(self) :
        if self.is_stopped == False :
            self.is_stopped = True
        else :
            pass

    def reset(self) :
        self.url = None
        self.content = None
