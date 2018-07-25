import pafy
import ffmpy
from time import gmtime, strftime
import json
import os

def video_crawler(y_id, filepath=''):

    try:
        video = pafy.new(y_id)

        video_info = dict()
        video_info['YouTubeID'] = y_id
        video_info['title'] = video.title
        video_info['rating'] = video.rating
        video_info['viewcount'] = video.viewcount
        video_info['author'] = video.author
        video_info['length'] = video.length
        video_info['duration'] = video.duration
        video_info['likes'] = video.likes
        video_info['dislikes'] = video.dislikes
        video_info['crawl_time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        video_info['description'] = video.description

        with open(os.path.join(filepath,'video_info.json'), 'w') as f:
            json.dump(video_info, f)

        best = video.getbest(preftype="mp4")
        best.download(quiet=True, filepath=os.path.join(filepath,'video.mp4'))

        return True
    except:
        print('Download Failed: %s ' % y_id)
        return False



if __name__ == '__main__':
    y_id = 'n1BtExxkP0M'
    video_crawler(y_id, '')
    video_crawler(y_id, '')