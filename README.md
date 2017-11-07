# Theorytab Crawler

The dataset is crawled from [Theorytab] - a collection of melodies and chord progressions. It contains 4623 artists and 10148 songs in toal. The information of each song is stored as a XML file. In addition, we also crawled the corresponding video and useful information from YouTube.

## Getting Started

* [Archive](#Archive)
* [Codes](#Codes)
* [Utils](#Utils)

## Archive

The dataset is organized according to artists and each artist contains their list of songs. The sturcture of the dataset is stored in "archive_artist.json". For each song, their the fowllowing files to record information:
 
 - "*.xml"：lead sheet of the section
 - "video.mp4"：YouTtube video
 - "song_info.jon"：metadata of songs
 - "video_info.json"：information from YouTtube

## Codes

&nbsp;&nbsp;&nbsp;[python files]

 - requirements.py  
 - theorytab_crawler.py
 - youtube_crawler.py

&nbsp;&nbsp;&nbsp;[IPython Notebook]

 - theorytab_parser.ipynb

## Utils

comming soon...

[Theorytab]: https://www.hooktheory.com/theorytab