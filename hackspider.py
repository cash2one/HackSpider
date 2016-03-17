import requests
import re
import time
from tld import get_tld
from urllib.parse import urlparse
import socket
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# url = "http://icp.chinaz.com/searchs"
# data = {'urls': 'qq.com', 'btn_search': '查询'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/48.0.2564.116 Safari/537.36'}


def geticp(url):
    # url = "qq.com"
    s = requests.session()
    r = s.get('http://icp.chinaz.com/info?q=' + url, headers=headers, timeout=20)
    n = "class=\"by1\">(.*)</td>"
    b = "class=\"by1\" width=\"30%\">(.*)</td>"
    if r.text.find('错误') == -1:
        name = re.findall(n, r.text)
        num = re.findall(b, r.text)
        print(url, '公司：', name[0], "网站名：", num[1], "备案号：", name[2])
    else:
        print(url, '未备案')


def gethacker(page):
    day = time.strftime("%Y-%m-%d", time.localtime())
    url = "http://www.hac-ker.net/?page=" + str(page)
    s = requests.session()
    r = s.get(url, headers=headers)

    # p = re.compile('\s+')
    # html = re.sub(p, '', r.text)
    tm = "<td width=\"12%\"><b style=\"color:#0BA81E;\">(.*)</td>"
    url = "<td width=\"58%\" style=\"word-break:break-all\"><a href=\"(.*)\" target=\"_blank\""
    # tr = "<tr>(.*)</tr>"
    alltm = re.findall(tm, r.text)
    allurl = re.findall(url, r.text)
    i = 0
    for a in alltm:
        if a == day:
            geticp(get_tld(allurl[i]))
            getpic(allurl[i])
            ip = socket.gethostbyname(urlparse(allurl[i], scheme='', allow_fragments=True).netloc)
            print(ip)
        else:
            print('over')
            return 'over2'
        i += 1
    gethacker(int(page) + 1)


def gethackcn(page):
    day = time.strftime("%Y-%m-%d", time.localtime())
    url = "http://www.hack-cn.com/?page=" + str(page)
    s = requests.session()
    r = s.get(url, headers=headers)

    # p = re.compile('\s+')
    # html = re.sub(p, '', r.text)
    tm = "<td width=\"16%\">(.*)</td>"
    web = "<td width=\"7%\"><a href=\"(.*)\" target=\"_blank\">View</a></td>"
    alltm = re.findall(tm, r.text)
    allweb = re.findall(web, r.text)

    i = 0
    for a in alltm:
        if a == day:
            gethackcndata(allweb[i])
        else:
            print('over')
            return 'over2'
        i += 1
    gethackcn(int(page) + 1)


def gethackcndata(web):
    url = "http://www.hack-cn.com/" + str(web)
    s = requests.session()

    r = s.get(url, headers=headers)
    url = "<td colspan=\"3\" bgcolor=\"#FFFFFF\"><a href=\"(.*)</td>"
    u = "target=\"_blank\">(.*)</a>"
    allurl = re.findall(url, r.text)
    allurl = re.findall(u, allurl[0])
    geticp(get_tld(allurl[0]))
    ip = socket.gethostbyname(urlparse(allurl[0], scheme='', allow_fragments=True).netloc)
    print(ip)
    print(allurl[0])
    getpic(allurl[0])


def verify(url):
    s = requests.session()
    r = s.get(url, headers=headers, timeout=20)
    if r.status_code == 200 and r.text != '':
        return r.text
    elif r.text == '':
        return 'null'
    else:
        return r.status_code


def getpic(url):
    tm = time.strftime("%m-%d %H-%M-%S", time.localtime())
    na = str(str(tm) + ' ' + url + '.jpg').replace('http://', '').replace('https://', '').replace(':', ' ').replace('/', '_').replace('?', '%3F')
    print(na)
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(20)
    browser.implicitly_wait(20)
    try:
        browser.get(url)
        browser.save_screenshot("./img/123.jps")
        browser.quit()
    except TimeoutException:
        print('time out after 20 seconds when loading page')
        browser.execute_script('window.stop()')


gethacker(1)
# getpic('http://status.zer.moe:89/webstatus/hebei')
