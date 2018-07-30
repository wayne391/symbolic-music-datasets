# 5 track pianoroll dataset

Improved training data for MuseGAN. Featuring:

* reduce time resolution from **96** to **48**
* increase number of bars in one phrase from **4** to **8**
* select segments with higher qulity instead of segmentation algorithm
* 34126 phrases in total. Therefore, the shape of the new tensor is **34126 x 8 x 48 x 84 x 5**
