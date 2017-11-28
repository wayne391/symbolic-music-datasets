import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import json

class VGMCrawler():
    BASE_URL = 'https://www.vgmusic.com/music/console/'
    archive_dir = 'archive'
    
    def __init__(self, sleep_time=0.1, log=True):
        self.sleep_time = sleep_time
        self.log = log
        self.count = 0
        
    def _request_url(self, url, doctype='html'):
        # set header
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
    
    def fetch_dirs(self, url):
        soup = self._request_url(url)
        tr_list = soup.find('table').find_all('tr')
        dir_list = []

        for i in range(3, len(tr_list)-1):
            dir_list.append(tr_list[i].find_all('td')[1].text)
        return dir_list
    
    def fetch_songs(self, url):
        soup = self._request_url(url)
        tr_list = soup.find('table').find_all('tr')
        song_list = []
        
        if len(tr_list) == 4:
            return None
        for i in range(2, len(tr_list)):
            now_tr = tr_list[i]
            if now_tr.get("class") == ['header']:
                album_name = now_tr.text.strip('\n')
            else:
                if not now_tr.td.get('colspan'):

                    # get info
                    info = now_tr.td.text.split('\n')
                    song_midi = now_tr.a['href']
                    song_name = info[0]
                    song_size = info[1]
                    song_author = info[3]
                    song_list.append({
                            'filename':song_midi, 
                            'song_name':song_name,
                            'song_size':song_size,
                            'song_author':song_author,
                            'album_name':album_name})
                    print('    |%30s |%30s |%13s |%10s |%s '%(album_name, song_name, song_size, song_author, song_midi ))
            
                    
        return song_list
    
    def crawl_songs(self, url, song_list, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        for idx, s in enumerate(song_list):
            sys.stdout.write('%d/%d - total: %d\n' % (idx, len(song_list), self.count))
            sys.stdout.flush()
            midi_url = url + s['filename']
            content = self._request_url(midi_url, doctype='content')
            fn = os.path.join(dir_path, s['filename'])
            with open(fn, "wb") as f:
                f.write(content)
                
            self.count += 1
                
    def crawl_archive(self):
        dir_list = self.fetch_dirs(self.BASE_URL)
        
        if not os.path.exists(self.archive_dir,):
            os.makedirs(self.archive_dir,)
            
        info = dict()
        for d in dir_list:
            root_dir = d.strip('/')
            print('{{%s}}' % root_dir)
            subdir_url = self.BASE_URL + d
            subdir_list = self.fetch_dirs(subdir_url)
            
            tmp_dict = dict()
            for sd in subdir_list:
                root_subdir = sd.strip('/')
                print('[%s]'%root_subdir)
                page_url = subdir_url + sd
                sl = self.fetch_songs(page_url)
                if sl:
                    self.crawl_songs(page_url, sl, os.path.join(self.archive_dir, root_dir, root_subdir))
                    tmp_dict[sd] = sl

            info[d] = tmp_dict
            
        with open(os.path.join(self.archive_dir,'archive.json'), "w") as f:
            json.dump(info, f)     
    
    def run(self): 
        s = time.time()
        self.crawl_archive()
        e = time.time()
        self._log_print(time.strftime("\nElapsed time: %H:%M:%S", time.gmtime(s-e)))
        self._log_print('Total %d Songs'&self.count)

if __name__ == '__main__':
    vc = VGMCrawler()
    vc.run()
