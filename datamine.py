# -*- coding:utf-8 -*-
import os.path
import re
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
base_url = 'https://image.baidu.com/search/acjson?'


def save_img(key, word):
    pn = 30
    imurls = []
    for i in range(21, pn + 1):
        print(word+str(i))
        url = (base_url + key).format(word, word, i * 30, 30)
        r = requests.get(url, headers=header)
        try:
            imurl = r.json().get('data')
        except BaseException:
            continue
        else:
            for im in imurl:
                if im:
                    imurls.append(im.get('thumbURL'))

    num = 0
    for iurl in imurls:
        if iurl:
            # print(iurl)
            num = num + 1
            ir = requests.get(iurl, headers=header)
            filename = word + '\\' + str(num) + '.jpg'
            f = open(filename, "wb")
            f.write(ir.content)
    f.close()


search_url = [
    'tn=resultjson_com&logid=10310500833835579561&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn={}&gsm=7800000000000078&1666618802653=',
    'tn=resultjson_com&logid=10455256908282817672&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn={}&gsm=3c0000000000003c&1666620677402=',
    'tn=resultjson_com&logid=11044589247836894084&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn={}&gsm=5a0000000000005a&1666620731470=',
    'tn=resultjson_com&logid=10936968036577463889&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn={}&gsm=1e0000000000001e&1666620769278='
]


def temp(url, st):
    imurls = []
    r = requests.get(url, headers=header)
    imurl = r.json().get('data')
    for im in imurl:
        if im:
            imurls.append(im.get('thumbURL'))
    i = st
    for iurl in imurls:
        if iurl:
            ir = requests.get(iurl, headers=header)
            fpath = os.getcwd() + '/p3/'  # 在当前路径下建立p2文件夹
            if not os.path.exists(fpath):
                os.mkdir(fpath)  # 创建文件夹
            with open(fpath + str(i) + '.jpg', mode='wb') as f:
                f.write(ir.content)
            i += 1
    f.close()


path = ['分子结构示意图', '机械原理示意图', '流程图', '直方图']
for i in path:
    if not os.path.exists(i):
        os.mkdir(i)

for url, idx in zip(search_url, path):
    save_img(url, idx)
