import requests
import re
import time
import os
from tld import get_tld
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

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
    Arr[单位名称,网站名称,备案号,备案性质]

    # url = "http://icp.chinaz.com/searchs"
    # data = {'urls': 'qq.com', 'btn_search': '查询'}

    """
    url = get_tld(url)
    arr = []
    s = requests.session()
    r = s.get('http://icp.chinaz.com/info?q=' + url, headers=headers, timeout=20)
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
                    blackurl = re.findall(hackcnu, r.text)
                    blackurl = re.findall(hackcnurl, blackurl[0])
                    urlArr.append(blackurl[0])
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
        for ser in ret:  #########
            return ser
    else:
        ser = []
        return ser


def getPic(url):
    return url
    tm = time.strftime("%m-%d %H-%M-%S", time.localtime())
    dire = time.strftime("%m-%d", time.localtime())
    if os.path.exists("./img/"):
        if not os.path.exists("./img/" + dire + "/"):
            os.mkdir("./img/" + dire + "/")
    else:
        os.mkdir("./img/")
        if not os.path.exists("./img/" + dire + "/"):
            os.mkdir("./img/" + dire + "/")

    na = str(str(tm) + ' ' + url + '.jpg').replace('http://', '').replace('https://', '').replace(':', ' ') \
        .replace('/', '_').replace('?', '%3F')
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(20)
    browser.implicitly_wait(20)
    try:
        browser.get(url)
        browser.save_screenshot("./img/" + dire + "/" + na)
        browser.quit()
    except TimeoutException:
        print('time out after 20 seconds when loading page')
        browser.save_screenshot("./img/" + dire + "/" + na)
        browser.quit()
        browser.execute_script('window.stop()')
    return na


def echo(urlArr):
    for a in urlArr:
        print(a, "查询状态...")
        ser = Verify(a)
        if not ser:
            if ser[1] != '404':
                print(a, "查询备案...")
                icp = getIcp(a)
                print(a, "获取截图...")
                pic = getPic(a)
                if not icp:
                    print(a, "Ip:", ser[0], "Status:", ser[1], "没有备案", "Screenshot:", pic)
                else:
                    print(a, "Ip:", ser[0], "Status:", ser[1], "Com:", icp[0], "Name:", icp[1], "Number:", icp[2],
                          "Property:", icp[3], "Screenshot:", pic)
            else:
                print(a, "地址404,跳过...")
        else:
            print(a, "无法解析或访问,跳过...")

    print('done')


# echo(getHack(1))
echo(getHack(2))
