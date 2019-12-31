import time
import requests
import json
import re
import os
from termcolor import colored

def print_download(str):
    print(colored("[!!] " + str, "yellow"))

if __name__ == '__main__':
    # print(" +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+")
    # print(" |b| |i| |l| |i| |b| |i| |l| |i|")
    # print(" +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+")
    print_download('******************** software is designed to bilibili of dance order by update****************')
    #input the number of update pages
    number = input("Gentleman,please enter the number of pages:")
    try:
        a=int(number)
    except:
        print_download('Fuck you!Enter the number,for example:250.Are you understand? If you can\'t understand,please kill the software!!!!')
        exit()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Referer': 'https://www.bilibili.com/v/dance/otaku/?spm_id_from=333.5.b_7375626e6176.2'
    }
    start=time.time()
    dir = 'D:/bilibili_dance/'

    if not os.path.exists(dir):
        print_download('The directory not exists,but i will create it ...')
        os.mkdir(dir)
        print_download('The directory has been created')
    else:
        pass
    os.chdir(dir)

    for j in range(int(number)):

        url = f"https://api.bilibili.com/x/web-interface/newlist?rid=20&type=0&pn={j}&ps=20&jsonp=jsonp"
        print_download(f"Starting downloading the page of {j+1}")
        res = requests.get(url, headers=headers)
        time.sleep(2)
        html = res.text
        # print(html)
        txt = r'pic":"(.*?)","title'
        txt2 = r'title":"(.*?)","pubdate'
        content = re.findall(txt, html)
        title = re.findall(txt2, html)
        for i in range(0, len(content)):
            pic_url = content[i]
            # trans=str.maketrans('\/:*?<>|','。。：。？《》。')
            # title[i]=title[i].trans
            # print(title[i])
            if ':' in title[i]:
                title[i] = title[i].replace(':', '：')
            if '?' in title[i]:
                title[i] = title[i].replace('?', '？')
            if '<' in title[i]:
                title[i] = title[i].replace('<', '《')
            if '>' in title[i]:
                title[i] = title[i].replace('>', '》')
            if '\\' in title[i]:
                title[i] = title[i].replace('\\', '。')
            if '/' in title[i]:
                title[i] = title[i].replace('/', '。')
            if '|' in title[i]:
                title[i] = title[i].replace('|', '。')
            if '*' in title[i]:
                title[i] = title[i].replace('*', '。')

            print(f"The 【第 {j + 1} 页,排名 {i + 1} 名】 title is: {title[i]}")
            picc = requests.get(pic_url, headers=headers)
            with open('【第' + str(j + 1) + '页,排名第' + str(i + 1) + '名】' + str(title[i]) + '.jpg', 'wb') as f:
                # print_download(title[i].replace(':','：'))
                xiaojiejie = picc.content
                f.write(xiaojiejie)
        print_download(f"The picture of {j+1} has been downloaded...")

    stop=time.time()
    print_download(f"The software ending...spend time is:{stop-start}")
