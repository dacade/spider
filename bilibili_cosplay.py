import os
import re
import time
from time import sleep
import pymongo
import requests
from termcolor import colored


def print_download(str):
    print(colored("[!!] " + str, "yellow"))


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Referer': 'https://h.bilibili.com/eden/picture_area'
}

dir = 'D:/bilibili_cosplay/'
if not os.path.exists(dir):
    print_download('The directory not exists,but i will create it ...')
    os.mkdir(dir)
    print_download('The directory has been created')
else:
    pass
os.chdir(dir)

client = pymongo.MongoClient('localhost', 27017)
db = client["h_bilibili"]
col = db["cosplay"]
dblist = client.list_database_names()


def save_mongodb(page):
    collections = client.h_bilibili.cosplay

    for j in range(page):
        print_download(f'The page is : {j}')
        url = f'https://api.vc.bilibili.com/link_draw/v2/Photo/list?category=cos&type=hot&page_num={j}&page_size=20'
        html = requests.get(url, headers=headers)
        sleep(1)
        res=html.json()
        data = html.text
        title_txt = r'title":"(.*?)","category'
        pre_title = re.findall(title_txt, data)

        for i in range(len(pre_title)):
            data = {}
            data['doc_id'] = (res['data']['items'][i]['item']['doc_id'])
            # print(data['doc_id'])
            myquery = {"doc_id": data['doc_id']}
            mydoc=col.find(myquery)
            ns=[]
            for x in mydoc:
                ns.append(x)
            if ns:
                print('The doc_id:【{}】 has been downloaded...'.format(data['doc_id']))
            else:
                data['user_id'] = (res['data']['items'][i]['user']['uid'])
                data['name'] = (res['data']['items'][i]['user']['name'])
                data['doc_id'] = (res['data']['items'][i]['item']['doc_id'])
                data['title'] = (res['data']['items'][i]['item']['title'])
                if ':' in data['title']:
                    data['title'] = data['title'].replace(':', '：')
                if '?' in data['title']:
                    data['title'] = data['title'].replace('?', '？')
                if '<' in data['title']:
                    data['title'] = data['title'].replace('<', '《')
                if '>' in data['title']:
                    data['title'] = data['title'].replace('>', '》')
                if '\\' in data['title']:
                    data['title'] = data['title'].replace('\\', '。')
                if '/' in data['title']:
                    data['title'] = data['title'].replace('/', '。')
                if '|' in data['title']:
                    data['title'] = data['title'].replace('|', '。')
                if '*' in data['title']:
                    data['title'] = data['title'].replace('*', '。')
                if '"' in data['title']:
                    data['title'] = data['title'].replace('"', '\'')
                data['category'] = (res['data']['items'][i]['item']['category'])
                data['upload_time'] = (res['data']['items'][i]['item']['upload_time'])
                data['already_liked'] = (res['data']['items'][i]['item']['already_liked'])
                data['already_voted'] = (res['data']['items'][i]['item']['already_voted'])

                pic_download(data['doc_id'],data['title'])
                print('{} download success,now we will pull in the mongodb...'.format(data['title']))

                collections.update_one(
                    {
                        'user_id': data['user_id'],
                        'name': data['name'],
                        'doc_id': data['doc_id'],
                        'title': data['title'],
                        'category': data['category'],
                        'upload_time': data['upload_time'],
                        'already_liked': data['already_liked'],
                        'already_voted': data['already_voted']
                    },
                    {'$set': data}, True
                )


def pic_download(av,title):
    url = f'https://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id={av}'
    html = requests.get(url, headers=headers)
    data = html.text
    sleep(1)
    img_txt = r'img_src":"(.*?)","img_width'
    img = re.findall(img_txt, data)
    for i in range(0, len(img)):
        picc = requests.get(img[i], headers=headers)
        with open(title+'-'+str(i+1) + '.jpg', 'wb') as f:
            f.write(picc.content)


if __name__ == '__main__':
    print('******************** software is designed to bilibili of cosplay****************')
    print_download("                     +-+ +-+ +-+ +-+ +-+ +-+ +-+                       ")
    print_download("                     |c| |o| |s| |p| |l| |a| |y|                       ")
    print_download("                     +-+ +-+ +-+ +-+ +-+ +-+ +-+                       ")
    print('******************** software is designed to bilibili of cosplay****************')

    start=time.time()
    page=5
    save_mongodb(page)
    stop=time.time()
    print_download(f"The software ending...spend time is:{stop-start}")
