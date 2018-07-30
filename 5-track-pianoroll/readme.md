# 5 track pianoroll dataset

Improved training data for MuseGAN. Featuring:

* reduce time resolution from **96** to **48**
* increase number of bars in one phrase from **4** to **8**
* select segments with higher qulity instead of segmentation algorithm
* **34126** phrases in total. Therefore, the shape of the new tensor is **34126 x 8 x 48 x 84 x 5**

![image](https://github.com/wayne391/List-of-Symbolic-Musical-Datasets/blob/master/docs/5-track_pianoroll.PNG)

#### sample result on MuseGAN
![image](https://github.com/wayne391/List-of-Symbolic-Musical-Datasets/blob/master/5-track-pianoroll/musegan/51901.png =250x)