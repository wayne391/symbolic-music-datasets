import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import json
import random

class Crawler():
    BASE_URL = ''

    def __init__(self, sleep_time=0.1, log=True):
        self.sleep_time = sleep_time
        self.log = log

    def _get_header():
        headers = None
        return headers

    def _get_form_data():
        data = None
        return data

    def _request_url(self, url, doctype='html', is_header=False):
        # set header
        if is_header
            # requests.post(url, headers=self._get_header(),
            #                               data=self._get_form_data())
            response = requests.get(url, headers=self._get_header())
        else:
            response = requests.get(url)

        # sleep
        time.sleep(self.sleep_time)

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
        try:
            self._request_url(url)
        except Exception as e:
            self._log_print(e)

    def fetch_content(self, url, dir_= None):
        try:
            self._request_url(url, doctype='content')
        except Exception as e:
            self._log_print(e)

#         if dir_:
#             with open(dir_, "w") as f:
#                 json.dump(c, f)
#             with open(dir_, "wb") as f:
#                 f.write(c)
#             with open(dir_, "w", encoding='utf-8') as f:
#                 f.write(c)

    def crawl_(self, dir_ = None):
        if not os.path.exists(dir_):
            os.makedirs(dir_)

        count = 0


        # sys.stdout.write()
        # sys.stdout.flush()

        # self.fetch_page(url)
        # self.fetch_content(url)

    def run(self, dir_=None):
        self._log_print("=================================================")
        c = Crawler()

        s = time.time()
        self.crawl_()
        e = time.time()

        self._log_print(time.strftime("\nElapsed time: %H:%M:%S", time.gmtime(s-e)))


if __name__ == '__main__':
    c.run()


