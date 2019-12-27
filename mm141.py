import time
import requests
from lxml import etree
import re
import os
# the software is writed to xialaoshi

def parse_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Referer':'https://www.mm131.com/'
    }
    html = requests.get(url, headers=headers)
    if html.status_code==200:
        html.encoding = 'gbk'
        content = etree.HTML(html.text)
        return content
    else:
        print('we can\'t link the web')


def get_title(content):
    title_xpath = '/html/body/div[4]/div[1]/dl[3]/dd/a/text()'
    t2 = content.xpath(title_xpath)
    return t2


def get_url(content):
    url_xpath = '/html/body/div[4]/div[1]/dl[3]/dd/a/@href'
    u2 = content.xpath(url_xpath)
    return u2


def sava_image(url,title,Url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Referer':'https://www.mm131.com/'
    }
    dir='D:/mm/update/'
    if not os.path.exists(dir):
        print('The directory not exists,but i will create it ...')
        os.mkdir(dir)
        print('The directory has been created')
    else:
        pass

    # mkdir
    for i in range(0, len(title)):
        # print("The update's title number of {} is : {}".format(i+1, title[i]))
        os.chdir(dir)
        pwd=os.getcwd()

        if not os.path.exists(dir+title[i]):
            os.makedirs(dir+title[i])
        os.chdir(dir + title[i])
        pwd1=os.getcwd()

        # print("the url of number is: {}".format(Url[i]))
        html3 = requests.get(Url[i], headers=headers)
        html3.encoding = 'gbk'
        regy = r'共(.*?)页'
        conn = re.findall(regy, html3.text)
        text = r'https://www.mm131.net/(.*?)/(.*?).html'
        number = re.findall(text, Url[i])
        print('Start downloading the {} ...'.format(title[i]))
        for j in range(0, int(conn[0])):
            # # print("The update's url number of {} is : {}".format(i, Url[i]))
            # text = r'https://www.mm131.net/(.*?)/(.*?).html'
            # number = re.findall(text, Url[i])
            pic_url = 'https://img1.mmmw.net/pic/' + number[0][1] + '/' + str(j + 1) + '.jpg'
            picc = requests.get(pic_url, headers=headers)
            with open(str(j+1) + '.jpg', 'wb') as f:
                f.write(picc.content)

if __name__ == '__main__':
    print('Start downloading...')
    url = 'https://www.mm131.net/xinggan/'
    start=time.time()
    print('Start parsing the url...')
    content = parse_url(url)
    print('Start get the title...')
    title = get_title(content)
    print('Start get the Url...')
    Url = get_url(content)
    print('Start sava_image...')
    sava_image(url, title,Url)
    stop=time.time()
    print('the time is {}'.format(stop-start))
