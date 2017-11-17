import requests
from bs4 import BeautifulSoup
import os
import time
import json
import string
import random
from lxml import etree

class HymnCrawler():
    BASE_URL = 'https://www.hymnal.net'
    
    def __init__(self, sleep_time = 0.1, log=True):
        self.sleep_time =sleep_time
        self.meta_category = {'classic': self.BASE_URL + '/en/song-index/h', 
            'new_tunes': self.BASE_URL + '/en/song-index/nt', 
            'new_songs': self.BASE_URL + '/en/song-index/ns', 
            'children': self.BASE_URL + '/en/song-index/c'}
        
        self.log = log
        self.metadata = None           

    def _request_url(self, url, doctype='html'):
        response = requests.get(url)
        time.sleep(self.sleep_time)
        if doctype =='html':
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        elif  doctype =='content':
            return response.content
        else:
            pass

    def _log_print(self, log):
        print(log)
        if self.log:
            with open("log.txt", "a") as f:
                print(log, file=f)

    def fetch_page_list(self, url):
        soup = self._request_url(url)
        tag_list = soup.find_all('div', {'class':'list-group'})[0].find_all('a', {'class':'list-group-item'})
        return [t['href'] for t in tag_list]

    def fetch_category_list(self, url):
        song_list = []
        soup = self._request_url(url)
        try:
            tag_list = soup.find_all('div', {'class':'letters'})[0].findAll('a')
            alphabet_list = [t.text for t in tag_list]
            for ch in alphabet_list:
                page_url = url+ '/' + ch
                self._log_print(page_url)
                song_list.extend(self.fetch_page_list(page_url))
        except:
            self._log_print(url)
            song_list.extend(self.fetch_page_list(url))
        return song_list

    def fetch_song(self, url, song_dir):

        soup = self._request_url(url)
        
        # (url, extension, filename)
        data_list = [('/f=mid', '.mid', 'all'), ('/f=mp3', '.mp3', 'audio'), ('/f=tune', '.mid', 'melody'),
                     ('/f=ppdf', '.pdf', 'ls_paino'), ('/f=pdf', '.pdf','ls_guitar'), ('/f=gtpdf', '.pdf', 'ls_text')]

        # save download files
        for d in data_list:
            r = requests.get(url+ d[0])

            if song_dir:
                with open(os.path.join(song_dir,d[2] + d[1]), 'wb') as f:
                    f.write(r.content)

        # metadata
        content_list = []    
        tag_list = soup.find_all('div', {'class':'row common-panel'})[0].find_all('div', {'class':'col-xs-7 col-sm-8 no-padding'})

        for t in tag_list:
            content_list.append(t.text.strip())
        label_list = []
        tag_list = soup.find_all('div', {'class':'row common-panel'})[0].find_all('label', {'class':'col-xs-5 col-sm-4'})
        for t in tag_list:
            label_list.append(t.text.replace(':',''))
        metadata = dict(zip(label_list, content_list))
    
        # title
        title = soup.find('h1', {'class':"text-center"}).text.strip()
        metadata['title'] = title
        
        # lyric table
        lyric_xml = soup.find_all('div', {'class':'col-xs-12 lyrics'})[0].find('table')

        if song_dir:
            with open( os.path.join(song_dir, 'song_metadata.json'), "w") as f:
                    json.dump(metadata , f)

            with open( os.path.join(song_dir, 'lyric.xml'), "w", encoding='utf-8') as f:
                f.write(str(lyric_xml))

        return lyric_xml, metadata

    def craw_archive(self, archive_dir='archive'):
        metadata = dict()
        for k in self.meta_category.keys():
            category_url = self.meta_category[k]
            metadata[k] = self.fetch_category_list(category_url)

        # saving
        if archive_dir:
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)

            with open(os.path.join(archive_dir, 'archive_metadata.json'), "w") as f:
                json.dump(metadata , f)

        return metadata

    def craw_songs(self, metadata, archive_dir='archive'):
        count = 0
        count_success = 0
        for k in list(metadata):
            self._log_print('> %s'%k)
            category_dir = os.path.join(archive_dir, k)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)

            song_list = metadata[k]

            numOfSongs = len(song_list)
            for i in range(numOfSongs):
                song_url = self.BASE_URL + song_list[i]
                song_id = song_url.split('/')[-1]
                self._log_print('    (%d/%d) %s'%(i+1, numOfSongs,  song_url))
                song_dir = os.path.join(category_dir, song_id)

                if not os.path.exists(song_dir):
                    os.makedirs(song_dir)
                
                try:
                    self.fetch_song(song_url, song_dir)
                    metadata['err'] = False
                    count_success += 1
                except:
                    self._log_print('error!!')
                    metadata['err'] = True
                    
                count += 1
        self._log_print('total: %d songs'%count)
        
        return metadata
    
    def reload(self, archive_dir='archive'):
        with open(os.path.join(archive_dir, 'archive_metadata.json'), "r") as f:
            self.metadata =json.load(f)
        
    def run(self, archive_dir='archive', reload=False):   
        
        self._log_print("=================================================")
        
        if not reload:
            self.metadata = self.craw_archive(archive_dir=archive_dir)
        else:
            self.reload(archive_dir=archive_dir)

        self.metadata = self.craw_songs(self.metadata, archive_dir=archive_dir)
        
        with open(os.path.join(archive_dir, 'archive_metadata.json'), "w") as f:
            json.dump(self.metadata, f)

if __name__ == '__main__':
    
    hc = HymnCrawler()
    s = time.time()
    hc.run()
    e = time.time()
    time.strftime("\nElapsed time: %H:%M:%S", time.gmtime(s-e))
    
