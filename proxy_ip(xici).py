import requests
from lxml import etree
import re
import time


# get the procol,ip,port
def parse_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    ip_lists = []

    try:
        res = requests.get(url, headers=headers)
    except:
        print('We can\'t link the web')

    html = res.text

    content = etree.HTML(html)
    ip_xpath = '//*[@id="ip_list"]//tr/td[2]/text()'
    port_xpath = '//*[@id="ip_list"]//tr/td[3]/text()'
    procol_xpath = '//*[@id="ip_list"]//tr/td[6]/text()'

    ip = content.xpath(ip_xpath)
    port = content.xpath(port_xpath)
    procol = content.xpath(procol_xpath)
    prs = []
    for i in procol:
        pr = i.lower()
        prs.append(pr)

    data = list(zip(ip, port))

    for ip, port in data:
        ip_list = f"{ip}:{port}"
        ip_lists.append(ip_list)

    return prs, ip_lists


# test the ip is userful
def test_ip(prs, ip_lists):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    url = 'https://www.lstazl.com/'

    for pr, ip_list in zip(prs, ip_lists):
        proxy = {pr: ip_list}
        try:
            res = requests.get(url, headers=headers, proxies=proxy, timeout=5)
            time.sleep(2)
            if res.status_code == 200:
                print('Congratulations,wo get a userful ip!!!')
                with open('good.txt', 'a') as f:
                    f.write(pr + '://' + ip_list + '\n')

        except Exception as e:
            print('The ip has go die...')


if __name__ == '__main__':
    # the page number
    num = 2
    print('Now,let\'s get some free ip proxy...')
    start=time.time()
    print('The soft has be working...')
    for i in range(num):
        url = 'https://www.xicidaili.com/nn/' + str(i + 1)
        pr, ip = parse_url(url)
        test_ip(pr, ip)
    stop=time.time()
    print('the time is {}'.format(stop-start))