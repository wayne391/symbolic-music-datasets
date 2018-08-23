# N-track pianoroll dataset

This repository contains pre-processing codes and processed datasets of [LPD](https://github.com/salu133445/lakh-pianoroll-dataset) dataset.

## Source Codes for Pre-processing

1. Download 'lpd_cleansed' from [here](https://github.com/salu133445/lakh-pianoroll-dataset)

2. run *parse.py*
3. run *compile.py*

You can change the setting to customize your own piano-roll dataset.

## Processed 5-track Piano-roll Datasets

#### Latest Versoin (ver.2)

* num of tracks: **5**
* *Bass, Drum, Guitar, String and Piano*
* time resolution: **48**
* pitch range: **84**
* num of bar: **8**
* num of phrases: **34126**
* the shape of the tensor is **34126 x 8 x 48 x 84 x 5**
* 5.12 GB
* select segments with higher qulity. One instrument for one track.
* [Download](https://drive.google.com/file/d/17FBw7c_vrK33_mEgsA919GTSlHoJ7M6T/view?usp=sharing)

#### Old Version for MuseGAN (ver.1)

* num of tracks: **5**
* *Bass, Drum, Guitar, String and Piano*
* time resolution: **96**
* pitch range: **84**
* num of bar: **4**
* num of phrases: **50266**
* the shape of the tensor is **50266 x 384 x 84 x 5**
* 7.54 GB
* Compress instruments in the same midi family into one track. See [here](https://github.com/salu133445/musegan/tree/master/v1/training)
* [Download](https://drive.google.com/file/d/1yj-5CsAwSoj1LHk4QwEQ09VB5fS69Vnq/view?usp=sharing)

Generally, version 2 has richer but clear textures.

--------------
Sample image of 5-track Piano-roll Datasets (ver.2):

![image](https://github.com/wayne391/List-of-Symbolic-Musical-Datasets/blob/master/docs/5-track_pianoroll.PNG)

The generated samples of version 2 on MuseGAN is [here]().