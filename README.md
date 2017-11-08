# Lead Sheet Collection

The collection is crawled from [Theorytab] - a database for melodies and chord progressions. It contains **4623** artists and **10148** songs in toal. The information of each song is stored as a XML file. In addition, we also crawled the corresponding video and useful information from YouTube.

## Getting Started

* [Archive](#Archive)
* [Codes](#Codes)
* [Utils](#Utils)

## Archive

The dataset is organized according to artists and each artist contains their list of songs. The sturcture of the dataset is stored in **archive_artist.json**. For each song, it contains the following files:

 - ***.xml**：lead sheets of the section
 - **video.mp4**：YouTtube video
 - **song_info.jon**：metadata of songs
    - *wikiid*
    - *pk* - a list of sections primary key
    - *section* - a list of sections name
    - *genres*
    - *song_url*


 - **video_info.json**：information from YouTtube
    - *crawl_time* - refernce for updating in the future
    - *rating*
    - *viewcount*
    - *likes*
    - *YouTubeID*
    - *length*
    - *description*
    - *author*
    - *title*
    - *duration*
    - *dislikes*


Due to the copyright consideration, the full crawled data would not be included in this repository. Hence, only few sample files are exhibited.

## Codes

 - requirements.txt
 - theorytab_crawler.py
 - youtube_crawler.py
 - theorytab_crawler.ipynb



## Utils

TBI

[Theorytab]: https://www.hooktheory.com/theorytab