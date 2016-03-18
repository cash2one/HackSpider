import requests
import re
import time
import os
import IP
from urllib.parse import urlparse
import socket
from tld import get_tld
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import platform


def isLINUX():
    """
    取系统是否为LINUX
    """
    global LINUX
    if 'Windows' in platform.system():
        LINUX = False
    elif 'Linux' in platform.system():
        LINUX = True
    else:
        print('系统无法识别可能无法截图.')


# 判断是否为LINUX
isLINUX()
# Get Post以及截图的超时时间
TIMEOUT = 20
# 获取时间和url的规则
hackertime = "<td width=\"12%\"><b style=\"color:#0BA81E;\">(.*)</td>"
hackerurl = "<td width=\"58%\" style=\"word-break:break-all\"><a href=\"(.*)\" target=\"_blank\""
hackcntime = "<td width=\"16%\">(.*)</td>"
hackcnweb = "<td width=\"7%\"><a href=\"(.*)\" target=\"_blank\">View</a></td>"
hackcnu = "<td colspan=\"3\" bgcolor=\"#FFFFFF\"><a href=\"(.*)</td>"
hackcnurl = "target=\"_blank\">(.*)</a>"
# User-Agent
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/48.0.2564.116 Safari/537.36'}


def getIcp(url):
    """
    # 获取网站备案
    :param url: String
    :return: Array
    Arr[单位名称,网站名称,备案号,备案性质]

    # url = "http://icp.chinaz.com/searchs"
    # data = {'urls': 'qq.com', 'btn_search': '查询'}

    """
    url = get_tld(url)
    arr = []
    s = requests.session()
    r = s.get('http://icp.chinaz.com/info?q=' + url, headers=HEADER, timeout=TIMEOUT)
    n = "class=\"by1\">(.*)</td>"
    b = "class=\"by1\" width=\"30%\">(.*)</td>"
    by = "<td align=\"left\" class=\"by2\">(.*)</td>"
    if r.text.find('错误') == -1:
        name = re.findall(n, r.text)
        num = re.findall(b, r.text)
        by = re.findall(by, r.text)
        arr = [name[0], num[1], name[2], by[0]]
        return arr
    else:
        return arr


def getHack(hack):
    """
    # 获取今日被黑网页
    :param hack: Int
        1->www.hac-ker.net
        2->www.hack-cn.com
    :return: Array
        UrlArray
    """
    global RUN
    global COUNT
    RUN = True
    COUNT = 1  # 页
    urlArr = []
    day = time.strftime("%Y-%m-%d", time.localtime())
    while RUN:
        if hack == 1:
            print(time.strftime("%H:%M:%S", time.localtime()), "第" + str(COUNT) + "页读取开始请稍候...")
            url = "http://www.hac-ker.net/?page=" + str(COUNT)
            s = requests.session()
            r = s.get(url, headers=HEADER, timeout=TIMEOUT)
            print(time.strftime("%H:%M:%S", time.localtime()), "hacker读取完毕,开始处理.")
            alltm = re.findall(hackertime, r.text)
            allurl = re.findall(hackerurl, r.text)
            i = 0
            for a in alltm:
                if a == day:
                    urlArr.append(allurl[i])
                else:
                    RUN = False
                    print(time.strftime("%H:%M:%S", time.localtime()), "Url读取完毕")
                    return urlArr
                    # return 'over2'
                i += 1
            COUNT += 1
        elif hack == 2:
            print(time.strftime("%H:%M:%S", time.localtime()), "第" + str(COUNT) + "页读取开始请稍候...")
            url = "http://www.hack-cn.com/?page=" + str(COUNT)
            s = requests.session()
            r = s.get(url, headers=HEADER)
            print(time.strftime("%H:%M:%S", time.localtime()), "hackcn列表读取完毕,开始读取Url.")
            alltm = re.findall(hackcntime, r.text)
            allurl = re.findall(hackcnweb, r.text)
            i = 0
            for a in alltm:
                if a == day:
                    url = "http://www.hack-cn.com/" + str(allurl[i])
                    s = requests.session()
                    r = s.get(url, headers=HEADER, timeout=TIMEOUT)
                    blackurl = re.findall(hackcnu, r.text)
                    blackurl = re.findall(hackcnurl, blackurl[0])
                    urlArr.append(blackurl[0])
                else:
                    RUN = False
                    print(time.strftime("%H:%M:%S", time.localtime()), "Url读取完毕")
                    return urlArr
                i += 1
            COUNT += 1
        else:
            RUN = False
            break

    return urlArr



def getPic(url):
    """
    # 获取网站截图
    Windows调用chromedriver.exe截图
    Linux调用CutyCapt截图 (需预先安装)(Ubuntu14.04下测试正常)
    :param url: http://google.com
    """
    tm = time.strftime("%m-%d %H-%M-%S", time.localtime())
    dire = time.strftime("%m-%d", time.localtime())
    if os.path.exists("./img/"):
        if not os.path.exists("./img/" + dire + "/"):
            os.mkdir("./img/" + dire + "/")
    else:
        os.mkdir("./img/")
        if not os.path.exists("./img/" + dire + "/"):
            os.mkdir("./img/" + dire + "/")

    na = str(str(tm) + ' ' + url + '.png').replace('http://', '').replace('https://', '').replace(':', ' ') \
        .replace('/', '_').replace('?', '%3F')
    na = "./img/" + dire + "/" + na

    if not LINUX:
        browser = webdriver.Chrome()
        browser.set_page_load_timeout(TIMEOUT)
        browser.implicitly_wait(TIMEOUT)
        try:
            browser.get(url)
            browser.save_screenshot(na)
            browser.quit()
        except TimeoutException:
            print('time out after 20 seconds when loading page')
            browser.save_screenshot(na)
            browser.quit()
            # browser.execute_script('window.stop()')
        return na
    else:
        wait = str(TIMEOUT * 1000)
        ret = os.system('xvfb-run --server-args="-screen 0, 1280x1200x24" cutycapt --max-wait=' + wait +
                        ' --url=\'' + url + '\' --out=\'' + na + '\'')
        if ret == 0:
            return na
        else:
            return False


def echo(urlArr):
    """
    # 获取Url的IP 响应码 备案 以及截图
    :type urlArr: Url数组
    """
    for a in urlArr:
        print(a, "查询状态...")
        ser = Verify(a)
        if ser:
            print(a, "查询备案...")
            icp = getIcp(a)
            print(a, "获取截图...")
            pic = getPic(a)
            if not icp:
                print(a, "Ip:", ser[0], "city:", ser[1], "没有备案", "Screenshot:", pic)
            else:
                print(a, "Ip:", ser[0], "city:", ser[1], "Com:", icp[0], "Name:", icp[1], "Number:", icp[2],
                      "Property:", icp[3], "Screenshot:", pic)
        else:
            print(a, "无法访问，跳过...")
    print('done')


def Verify(url):
    """
    # 验证网站
    :param url:
    :return:
    """
    doom = isCHINA(url)
    if doom:
        try:
            s = requests.session()
            r = str(s.head(url, headers=HEADER, timeout=TIMEOUT))
            print(r)
            if r.find("200") != -1 or r.find("301") != -1 or r.find("302") != -1:
                return doom
            else:
                return False
        except Exception:
            return False
    else:
        return False


def getDomain(url):
    return urlparse(url, scheme='', allow_fragments=True).netloc


def isCHINA(url):
    """
    # 获取IP 并判断是否为国内网站 返回IP和归属地
    :param url:
    :return:
    """
    ret = []
    try:
        ip = socket.gethostbyname(getDomain(url))
        ser = IP.find(ip)
        if not ser:
            return
        else:
            if ser.find('中国') != -1 or ser.find('香港') != -1:
                ret.append(ip)
                ret.append(ser)
                return ret
            else:
                return
    except Exception:
        return

echo(getHack(1))
echo(getHack(2))
