import os
from time import sleep
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}
dir = 'D:/mmkk/'
if not os.path.exists(dir):
    print('The directory not exists,but i will create it ...')
    os.mkdir(dir)
    print('The directory has been created')
else:
    pass


def get_one(url):
    # switch to the root path
    os.chdir(dir)
    pwd = os.getcwd()

    res=requests.get(url,headers=headers)
    sleep(2)
    html=res.text
    content = etree.HTML(html)
    img_xpath='//*[@id="masonry"]/div/img/@data-original'
    title_xpath='//*[@id="masonry"]/div/img/@title'
    img = content.xpath(img_xpath)
    title = content.xpath(title_xpath)
    imgs=[]
    titles=[]
    for i in range(len(img)):
        imgs.append(img[i])
        titles.append(title[i])

    titles2=titles[0][:-4]

    # swtich the path
    if not os.path.exists(dir + titles2):
        os.makedirs(dir + titles2)
    os.chdir(dir + titles2)
    pwd1 = os.getcwd()
    print(pwd1)

    for i in range(len(imgs)):
        picc = requests.get(imgs[i], headers=headers)
        with open(titles[i]+'.jpg', 'wb') as f:
            f.write(picc.content)


if __name__ == '__main__':
    for i in range(1,4):
        url=f'https://www.mmkk.me/cosplay/630{i}.html'
        get_one(url)
