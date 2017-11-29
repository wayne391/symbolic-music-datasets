import random
import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import json
import re
import random

class EPcompCrawler():
    BASE_URL = 'http://www.piano-e-competition.com'
    ROOT = 'archive'
    YEARS = ['/midi_2002.asp', '/midi_2004.asp', '/midi_2006.asp',
         '/midi_2008.asp', '/midi_2009.asp', '/midi_2011.asp']
    
    def __init__(self, sleep_time=0.1, log=True):
        self.sleep_time = sleep_time
        self.log = log
        self.mid_cnt = 0
        self.zip_cnt = 0
        
    def _request_url(self, url, doctype='html'):
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
    
    def fetch_year_songs(self, year_url):
        soup = self._request_url(year_url)
        a_list = soup.find_all('a')
        midi_list = []
        zip_list = []
        print(len(a_list))

        for idx in range(len(a_list)):
            a = a_list[idx]

            url = a.get('href')
            if  url and (('.MID' in url) or ('.mid' in url)):
                now_performer = re.search('(\D+?)(\d+?).', url.split('/')[-1]).group(1)
                song_name = re.sub( '\s+', ' ', a.text.replace('\r', '').replace('\n', '')).strip()
                try:
                    composer = a.parent.parent.td.text.strip()
                except:
                    try:
                        composer = a.parent.parent.parent.td.text.strip()
                    except:
                        composer = a.parent.parent.parent.parent.td.text.strip()
                print('%-10s |%-40s   |[%s | %s]' % (now_performer, url, song_name, composer))
                midi_list.append((now_performer, url, song_name))

            if  url and (('.ZIP' in url) or ('.zip' in url)):
                zip_fn = url.lstrip('../')
                print('%-10s %s'%(now_performer, zip_fn))
                zip_list.append((now_performer, zip_fn))
        return midi_list, zip_list
    
    def crawl_year_songs(self, midi_list, zip_list, dir_path):
        path_midi = os.path.join(dir_path, 'midi') 
        path_zip = os.path.join(dir_path, 'zip')
            
        if not os.path.exists(path_midi):
            os.makedirs(path_midi)
        if not os.path.exists(path_zip):
            os.makedirs(path_zip)
        
        print('=================midi=================')
        for idx in range(len(midi_list)):
            m_url = midi_list[idx][1]
            
            if '/ecompetition' not in m_url:
                m_url = 'http://www.piano-e-competition.com/ecompetition/' + m_url
            else:
                m_url = self.BASE_URL + m_url

            
            print(idx, m_url)
            content = self._request_url(m_url, doctype='content')
            fn = m_url.split('/')[-1]
                 
            with open(os.path.join(path_midi, fn), "wb") as f:
                f.write(content)
               
        print('=================zip=================')    
        for idx in range(len(zip_list)):
            z_url = zip_list[idx][1]
            z_url = self.BASE_URL + '/' + z_url
            print(idx, z_url)
            content = self._request_url(z_url, doctype='content')
            fn = z_url.split('/')[-1]         
            
            with open(os.path.join(path_zip, fn), "wb") as f:
                f.write(content)
    
    def crawl_archive(self):
        
        if not os.path.exists(self.ROOT):
            os.makedirs(self.ROOT)
        
        archive_dict = dict()
        
        for y in self.YEARS:
            ml, zl = self.fetch_year_songs(self.BASE_URL+y)
            year = re.search('(\d{4}).',y).group(1)
            path_year = os.path.join(self.ROOT, year)
            if not os.path.exists( path_year ):
                os.makedirs( path_year )

            print('{%s}' % year)
        
            self.mid_cnt += len(ml)
            self.zip_cnt += len(zl)
        
            tmp = {'mid':ml, 'zip':zl}
            archive_dict[year] = tmp 
        
            self.crawl_year_songs(ml, zl,  path_year)
        
        with open(os.path.join(self.ROOT, 'archive.json'), "w") as f:
            json.dump(archive_dict, f)
    
    def run(self):
        s = time.time()
        self.crawl_archive()
        e = time.time()
        
        self._log_print('Total midi files %d'%self.mid_cnt)
        self._log_print('Total zip files %d'%self.zip_cnt)
        self._log_print(time.strftime("\nElapsed time: %H:%M:%S", time.gmtime(s-e)))

        
if __name__ == '__main__':
    ec = EPcompCrawler()
    ec.run()