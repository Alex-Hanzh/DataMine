# DataMine

using kitti-sementic dataset & its GPS data, generate 1:10 scale aerial images that are one-to-one with the on-board camera view image

preprocess.py process the gps data and the kitti raw data to a new dataset
BEVspider.py is main process to crawl BEV image from Google-earth 
tailor.py is using to tailor the origin image to the correct size
