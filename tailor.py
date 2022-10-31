import os

import numpy as np
import cv2

left_up_y = 340
left_down_y = 815
left_up_x = 726
right_up_x = 1192


def tailor(img_path, save_path):
    img = cv2.imread(img_path)
    crop = img[int(left_up_y):int(left_down_y), int(left_up_x):int(right_up_x)]
    cv2.imwrite(save_path, crop)


data_path = r'D:\Work\Code\Python\DataMine\dataset'
tailored_path = r'D:\Work\Code\Python\DataMine\tailored_data'
pic_fnames = os.listdir(data_path)
if not os.path.exists(tailored_path):
    os.mkdir(tailored_path)

for pic in pic_fnames:
    img_path = os.path.join(data_path, pic)
    save_path = os.path.join(tailored_path, pic)
    tailor(img_path, save_path)
