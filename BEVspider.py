import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from PIL import ImageGrab
import numpy as np
import re

browser = webdriver.Chrome('D:\APP\日常应用\Google\Chrome\Application\chromedriver.exe')
browser.get('https://earth.google.com/web/')
time.sleep(40)
gps_path = r'G:\datasets\kitti\oxts'
gps_fnames = os.listdir(gps_path)
gps_fnames.sort(key=lambda x: int(x.split('.')[0]))
rec_bev = []
bev_cnt = 0
rec_fv = []

js = {
    "open search button": "document.evaluate('/html/body/earth-app',document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,"
                          "null).singleNodeValue.$.toolbar.shadowRoot.children['search'].click()",

    "input box": "return document.evaluate('/html/body/earth-app',document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,"
                 "null).singleNodeValue.$['drawer-panel'].children[1].children[2].shadowRoot.getElementById("
                 "'search').shadowRoot.getElementById('omnibox').shadowRoot.getElementById('omnibox-input')",

    "search button": "return document.evaluate('/html/body/earth-app',document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,"
                     "null).singleNodeValue.$['drawer-panel'].children[1].children[2].shadowRoot.getElementById("
                     "'search').shadowRoot.getElementById('omnibox').shadowRoot.getElementById('search-button') ",

    "close knowledge card": "document.evaluate('/html/body/earth-app',document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,"
                            "null).singleNodeValue.$['drawer-panel'].children[1].children[15].shadowRoot.getElementById("
                            "'top-card').shadowRoot.getElementById('close').click() ",

    "zoom-in button": "return document.evaluate('/html/body/earth-app',document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,"
                      "null).singleNodeValue.$['drawer-panel'].children[1].children[5].children[1].children["
                      "0].shadowRoot.getElementById('zoom-in') "
}


def google_earth(idx, gps):
    path = r'dataset/BEV' + str(idx) + '.png'
    if os.path.exists(path):
        return
    browser.execute_script(js["open search button"])
    time.sleep(0.5)
    ele = browser.execute_script(js["input box"])
    ele.clear()
    ele.send_keys(gps)
    time.sleep(0.5)
    ele = browser.execute_script(js["search button"])
    ele.click()
    time.sleep(12)
    browser.execute_script(js["close knowledge card"])
    time.sleep(5)
    ele = browser.execute_script(js["zoom-in button"])

    for i in range(7):
        ele.click()
        time.sleep(2)

    time.sleep(5)

    image = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    image.save(path)


def exist(lon, lat):
    idx = 0
    for bev in rec_bev:
        b_lon, b_lat = map(float, bev.split(','))
        if abs(lon - b_lon) <= 0.0001 and abs(lat - b_lat) <= 0.00015:
            return idx
        idx += 1
    return None


def convert_gps(lon, lat):
    nlon = round(lon, 4)
    nlat = round(lat, 4)
    gps = str(nlon) + ',' + str(nlat)
    return gps


for gps_fname in gps_fnames:
    fname = os.path.join(gps_path, gps_fname)
    file = open(fname, 'r')
    lon, lat = file.read().split(' ')[0:2]
    lon = float(lon)
    lat = float(lat)
    file.close()
    idx = exist(lon, lat)
    if idx is not None:
        rec_fv.append(idx)
        print("miss" + str(idx))
    else:
        google_earth(bev_cnt, convert_gps(lon, lat))
        rec_bev.append(convert_gps(lon, lat))
        rec_fv.append(bev_cnt)
        bev_cnt += 1
        # print(convert_gps(lon, lat))
    if bev_cnt % 50 == 0:
        n = np.array(rec_fv)
        np.save('rec_fv.npy', n)
        m = np.array(rec_bev)
        np.save('rec_bev.npy', m)
        print(bev_cnt)

# n = np.array(rec_fv)
# np.save('rec_fv.npy', n)
# m = np.array(rec_bev)
# np.save('rec_bev.npy', m)

rec_bev = np.load('rec_bev.npy').tolist()
rec_fv = np.load('rec_fv.npy').tolist()

# i = 0
# for gps_fname in gps_fnames:
#     fname = os.path.join(gps_path, gps_fname)
#     file = open(fname, 'r')
#     lon, lat = file.read().split(' ')[0:2]
#     lon = float(lon)
#     lat = float(lat)
#     id = exist(lon, lat)
#     rec_fv[i] = id
#     i = i + 1
# print("fv:{} , id:{}".format(gps_fname, id))


