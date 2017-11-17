import requests
from bs4 import BeautifulSoup
import os
import time
import json
import random

class Crawler():
    BASE_URL = ''
    
    def __init__(self, sleep_time=0.1, log=True):
        self.sleep_time = sleep_time
        self.log = log 
        
    def _get_header():
        headersList = [
                {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
                {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'},
                {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
                {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
                {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
                {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
            ]
        idx = random.randint(0,len(headersList)-1)
        return headersList[idx]
    
    def _request_url(self, url, doctype='html', is_header=False):
        # set header
        if is_header
            response = requests.get(url, headers=self._get_header())
        else:
            response = requests.get(url)
        
        # sleep
        time.sleep(self.leep_time)
        
        # return
        if doctype =='html':
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        elif  doctype =='content':
            return response.content
        else:
            return response

    def _log_print(self, log, quite=False):
        if not quite:
            print(log)
            
        if self.log:
            with open("log.txt", "a") as f:
                print(log, file=f)

    def fetch_page(self, url):
        self._request_url(url)
        
    def fetch_content(self, url, dir_= None):
        self._request_url(url, doctype='content')
        
#         if dir_:
#             with open(dir_, "w") as f:
#                 json.dump()
#             with open(dir_, "wb") as f:
#                 f.write()
#             with open(dir_, "w", encoding='utf-8') as f:
#                 f.write()

    def crawl_(self, dir_ = None):
        if not os.path.exists(dir_):
            os.makedirs(dir_)

        count = 0

#         self.fetch_page(url)
#         self.fetch_content(url)

    def run(self, dir_=None):           
        self._log_print("=================================================")
        self.crawl_()

if __name__ == '__main__':
    
    c = Crawler()
    s = time.time()
    c.run()
    e = time.time()
    
    time.strftime("\nElapsed time: %H:%M:%S", time.gmtime(s-e))