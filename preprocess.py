import os
import re

root_path = r'G:\datasets\kitt-raw\raw'

new_path = r'G:\datasets\kitti'
dir_path = os.listdir(root_path)


def transfer(idx, pic_name, gps_name):
    file = open(pic_name, "rb")
    data = file.read()
    file.close()

    new_pic_fname = os.path.join(new_path, 'image', str(idx) + '.png')
    new_file = open(new_pic_fname, "wb")
    new_file.write(data)
    new_file.close()

    file = open(gps_name, "rb")
    data = file.read()
    file.close()

    new_gps_fname = os.path.join(new_path, 'oxts', str(idx) + '.txt')
    new_file = open(new_gps_fname, "wb")
    new_file.write(data)
    new_file.close()


num = 0
for dpath in dir_path:
    date = re.search(r'[0-9]*_[0-9]*_[0-9]*', dpath).group()
    pic_path = os.path.join(root_path, dpath, date, dpath, 'image_02', 'data')
    gps_path = os.path.join(root_path, dpath, date, dpath, 'oxts', 'data')
    pic_names = os.listdir(pic_path)

    for idx in range(0, len(pic_names), 10):
        if num % 10 == 0:
            print(num)
        num = num + 1
        pic_fname = os.path.join(pic_path, pic_names[idx])
        gps_fname = os.path.join(gps_path, pic_names[idx][:-3] + 'txt')
        # print(gps_fname)
        transfer(num, pic_fname, gps_fname)
