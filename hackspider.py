import requests
import re
import time
import os
from tld import get_tld
from urllib.parse import urlparse
import socket
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# url = "http://icp.chinaz.com/searchs"
# data = {'urls': 'qq.com', 'btn_search': '查询'}
hackertime = "<td width=\"12%\"><b style=\"color:#0BA81E;\">(.*)</td>"
hackerurl = "<td width=\"58%\" style=\"word-break:break-all\"><a href=\"(.*)\" target=\"_blank\""
hackcntime = "<td width=\"16%\">(.*)</td>"
hackcnweb = "<td width=\"7%\"><a href=\"(.*)\" target=\"_blank\">View</a></td>"
hackcnu = "<td colspan=\"3\" bgcolor=\"#FFFFFF\"><a href=\"(.*)</td>"
hackcnurl = "target=\"_blank\">(.*)</a>"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/48.0.2564.116 Safari/537.36'}


def getIcp(url):
    """
    :param url: String
    :return: Array

    """
    url = get_tld(url)
    arr = []
    s = requests.session()
    r = s.get('http://icp.chinaz.com/info?q=' + url, headers=headers, timeout=20)
    n = "class=\"by1\">(.*)</td>"
    b = "class=\"by1\" width=\"30%\">(.*)</td>"
    if r.text.find('错误') == -1:
        name = re.findall(n, r.text)
        num = re.findall(b, r.text)
        arr = [name[0], num[1], name[2]]
        return arr
    else:
        return arr


def getHack(hack):
    """
    :param hack: Int
        1->www.hac-ker.net
        2->www.hack-cn.com
    :return: Array
        UrlArray
    """
    global RUN
    global COUNT
    RUN = True
    COUNT = 1
    urlArr = []
    day = time.strftime("%Y-%m-%d", time.localtime())
    while RUN:
        if hack == 1:
            print(time.strftime("%H:%M:%S", time.localtime()), "第" + str(COUNT) + "页读取开始请稍候...")
            url = "http://www.hac-ker.net/?page=" + str(COUNT)
            s = requests.session()
            r = s.get(url, headers=headers, timeout=20)
            print(time.strftime("%H:%M:%S", time.localtime()), "读取完毕,开始处理.")
            alltm = re.findall(hackertime, r.text)
            allurl = re.findall(hackerurl, r.text)
            i = 0
            for a in alltm:
                if a == day:
                    urlArr.append(allurl[i])
                else:
                    RUN = False
                    print(time.strftime("%H:%M:%S", time.localtime()), "Over")
                    return urlArr
                    # return 'over2'
                i += 1
            COUNT += 1
        elif hack == 2:
            print(time.strftime("%H:%M:%S", time.localtime()), "第" + str(COUNT) + "页读取开始请稍候...")
            url = "http://www.hack-cn.com/?page=" + str(COUNT)
            s = requests.session()
            r = s.get(url, headers=headers)
            print(time.strftime("%H:%M:%S", time.localtime()), "读取完毕,开始处理.")
            alltm = re.findall(hackcntime, r.text)
            allurl = re.findall(hackcnweb, r.text)
            i = 0
            for a in alltm:
                if a == day:
                    url = "http://www.hack-cn.com/" + str(allurl[i])
                    s = requests.session()
                    r = s.get(url, headers=headers, timeout=20)
                    allurl = re.findall(hackcnu, r.text)
                    allurl = re.findall(hackcnurl, allurl[0])
                    urlArr.append(allurl[0])
                else:
                    RUN = False
                    print(time.strftime("%H:%M:%S", time.localtime()), "Over")
                    return urlArr
                i += 1
            COUNT += 1
        else:
            RUN = False
            break

    return urlArr


def Verify(url):
    s = requests.session()
    data = {'url': url}
    fi = "<div class=\"fr zTContrig\"><span>(.*)</span></div></li><li class=\"bor-b1s bg-list clearfix\">" \
         "<div class=\"fl zTContleft\">返回状态码</div><div class=\"fr zTContrig\"><span>(.*)</span></div></li>"
    r = s.get("http://tool.chinaz.com/pagestatus/", data=data, headers=headers, timeout=20)
    if r.text.find("检测结果") != -1:
        ret = re.findall(fi, r.text)
        for ser in ret:
            return ser


def getPic(url):
    tm = time.strftime("%m-%d %H-%M-%S", time.localtime())
    dir = time.strftime("%m-%d", time.localtime())
    if os.path.exists("./img/"):
        if os.path.exists("./img/" + dir + "/"):
            print("dir")
        else:
            os.mkdir("./img/" + dir + "/")
    else:
        os.mkdir("./img/")
        if os.path.exists("./img/" + dir + "/"):
            print("dir")
        else:
            os.mkdir("./img/" + dir + "/")

    na = str(str(tm) + ' ' + url + '.jpg').replace('http://', '').replace('https://', '').replace(':', ' ') \
        .replace('/', '_').replace('?', '%3F')
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(20)
    browser.implicitly_wait(20)
    try:
        browser.get(url)
        browser.save_screenshot("./img/" + dir + "/" + na)
        browser.quit()
    except TimeoutException:
        print('time out after 20 seconds when loading page')
        browser.save_screenshot("./img/" + dir + "/" + na)
        browser.quit()
        browser.execute_script('window.stop()')


urlArr = getHack(1)
for a in urlArr:
    ser = Verify(a)
    icp = getIcp(a)
    print(icp)
    print(a, "ip:", ser[0], "status:", ser[1])
# getpic('http://status.zer.moe:89/webstatus/hebei')
