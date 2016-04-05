import requests
import re
import time
from time import sleep
import os
import IP
from urllib.parse import urlparse
import socket
from tld import get_tld
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import platform
from sqlalchemy import Column, create_engine
from sqlalchemy.types import Integer, String
from sqlalchemy.dialects.mysql import MEDIUMTEXT
# BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
# DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
# LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
# NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
# TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pycurl
from io import BytesIO
import base64

# import chardet

Base = declarative_base()


class Hack_spider(Base):  # 分组表
    __tablename__ = 'hack_spider'
    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(500), unique=True)  # 域名
    hackweb = Column(String(500))  # 黑页
    ip = Column(String(500))  # IP
    icp = Column(String(500), default="")  # ICP
    icp_name = Column(String(500), default=None)  # 备案单位
    icp_webname = Column(String(500), default=None)  # 备案网站名
    icp_st = Column(String(500), default=None)  # 备案类型
    city = Column(String(500))  # 归属地
    time = Column(Integer)  # 时间
    pic = Column(String(500))  # 快照路径
    html = Column(MEDIUMTEXT)  # 黑页源码
    origin = Column(String(20))  # 采集来源
    locate = Column(String(500))  # 定位


class hackspider:
    def __init__(self):
        # 判断是否为LINUX
        if 'Windows' in platform.system():
            self.LINUX = False
        elif 'Linux' in platform.system():
            self.LINUX = True
        else:
            print('系统无法识别可能无法截图.')
            self.LINUX = False

        self.SAVE_SQL = True
        self.DEBUG_MODE = False
        self.DEBUG_TIME = "2016-03-28"
        self.PRTSC = True

        # --------------------------------------------
        if self.SAVE_SQL:
            self.SQL_HOST = '127.0.0.1'
            self.SQL_USER = 'app'
            self.SQL_PASS = 'joEDygcT5JWIKnpS'
            self.SQL_DB = 'app_webstatus'
            self.SQL_PORT = 3306
            self.SQL_CHAR = 'utf8'
            engine = create_engine(
                "mysql+pymysql://" + self.SQL_USER + ":" + self.SQL_PASS + "@" + self.SQL_HOST + "/" + self.SQL_DB +
                "?charset=utf8", echo=False)

            self.DBSession = sessionmaker(bind=engine)

        # Get Post以及截图的超时时间
        self.TIMEOUT = 20
        # User-Agent
        self.HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/48.0.2564.116 Safari/537.36'}
        # 获取时间和url的规则
        # self.hackertime = "<td width=\"12%\"><b style=\"color:#0BA81E;\">(.*)</td>"
        self.hackerurl = "<td width=\"58%\" style=\"word-break:break-all\"><a href=\"(.*)\" target=\"_blank\""
        # self.hackcntime = "<td width=\"16%\">(.*)</td>"
        self.hackcnweb = "<td width=\"7%\"><a href=\"(.*)\" target=\"_blank\">View</a></td>"
        self.hackcnu = "<td colspan=\"3\" bgcolor=\"#FFFFFF\"><a href=\"(.*)</td>"
        self.hackcnurl = "target=\"_blank\">(.*)</a>"

    def getIcp(self, url):
        """
        # 获取网站备案
        :param url: String
        :return: Array
        Arr[单位名称,网站名称,备案号,备案性质]

        # url = "http://icp.chinaz.com/searchs"
        # data = {'urls': 'qq.com', 'btn_search': '查询'}

        """
        try:
            url = get_tld(url)
        except Exception as e:
            print(e)
        arr = []
        try:
            s = requests.session()
            r = s.get('http://icp.chinaz.com/info?q=' + url, headers=self.HEADER, timeout=self.TIMEOUT)
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
        except Exception as e:
            print(e)
            return arr

    def getHack(self, hack, last):
        """
        # 获取今日被黑网页
        :param hack: Int
            1->www.hac-ker.net
            2->www.hack-cn.com
               last:上次获取到的最后一条信息(采集到这条为止)
        :return: Array
            UrlArray
        """
        global RUN
        global COUNT
        RUN = True
        COUNT = 1  # 页
        urlArr = []
        s = requests.session()
        while RUN:
            if hack == 1:
                print(time.strftime("%H:%M:%S", time.localtime()), "第" + str(COUNT) + "页读取开始请稍候...")
                url = "http://www.hac-ker.net/?page=" + str(COUNT)
                try:
                    r = s.get(url, headers=self.HEADER, timeout=self.TIMEOUT)
                except Exception as e:
                    print(e)
                    urlArr.clear()
                    return urlArr
                print(time.strftime("%H:%M:%S", time.localtime()), "hacker读取完毕,开始处理.")
                allurl = re.findall(self.hackerurl, r.text)
                i = 0

                for a in allurl:
                    if a != last:
                        urlArr.append([a, a])
                    else:
                        RUN = False
                        print(time.strftime("%H:%M:%S", time.localtime()), "Url读取完毕")
                        urlArr.reverse()
                        return urlArr
                    i += 1
                COUNT += 1
            elif hack == 2:
                print(time.strftime("%H:%M:%S", time.localtime()), "第" + str(COUNT) + "页读取开始请稍候...")
                url = "http://www.hack-cn.com/?page=" + str(COUNT)
                try:
                    r = s.get(url, headers=self.HEADER)
                except Exception as e:
                    print(e)
                print(time.strftime("%H:%M:%S", time.localtime()), "hackcn列表读取完毕,开始读取Url.")
                allurl = re.findall(self.hackcnweb, r.text)
                i = 0
                print(allurl)
                for a in allurl:
                    try:
                        m = re.findall('(\w*[0-9]+)\w*', a)
                        if m[0] != last:
                            url = "http://www.hack-cn.com/" + str(a)
                            r = s.get(url, headers=self.HEADER, timeout=self.TIMEOUT)
                            blackurl = re.findall(self.hackcnu, r.text)
                            blackurl = re.findall(self.hackcnurl, blackurl[0])
                            urlArr.append([blackurl[0], m[0]])
                        else:
                            RUN = False
                            print(time.strftime("%H:%M:%S", time.localtime()), "Url读取完毕")
                            urlArr.reverse()
                            return urlArr
                    except Exception as e:
                        print(e)
                    i += 1
                COUNT += 1
            else:
                RUN = False
                break
        urlArr.reverse()
        return urlArr

    def getPageHack(self, hack, page):
        """
        # 按页面数获取被黑页面 用于初始化
        :param hack: Int
            1->www.hac-ker.net
            2->www.hack-cn.com
               page:采集指定的页面数量
        :return: Array
            UrlArray
        """
        global RUN
        global COUNT
        RUN = True
        COUNT = 1  # 页
        urlArr = []
        s = requests.session()
        while RUN:
            if hack == 1:
                print(time.strftime("%H:%M:%S", time.localtime()), "第" + str(COUNT) + "页读取开始请稍候...")
                url = "http://www.hac-ker.net/?page=" + str(COUNT)
                try:
                    r = s.get(url, headers=self.HEADER, timeout=self.TIMEOUT)
                except Exception as e:
                    print(e)
                print(time.strftime("%H:%M:%S", time.localtime()), "hacker读取完毕,开始处理.")
                allurl = re.findall(self.hackerurl, r.text)
                for a in allurl:
                    urlArr.append([a, a])

                COUNT += 1

                if COUNT > page:
                    RUN = False
                    print(time.strftime("%H:%M:%S", time.localtime()), "Url读取完毕")
                    urlArr.reverse()
                    return urlArr

            elif hack == 2:
                print(time.strftime("%H:%M:%S", time.localtime()), "第" + str(COUNT) + "页读取开始请稍候...")
                url = "http://www.hack-cn.com/?page=" + str(COUNT)
                try:
                    r = s.get(url, headers=self.HEADER, timeout=self.TIMEOUT)
                except Exception as e:
                    print(e)
                print(time.strftime("%H:%M:%S", time.localtime()), "hackcn列表读取完毕,开始读取Url.")
                allurl = re.findall(self.hackcnweb, r.text)

                for a in allurl:
                    try:
                        m = re.findall('(\w*[0-9]+)\w*', a)
                        url = "http://www.hack-cn.com/" + str(a)
                        r = s.get(url, headers=self.HEADER, timeout=self.TIMEOUT)
                        blackurl = re.findall(self.hackcnu, r.text)
                        blackurl = re.findall(self.hackcnurl, blackurl[0])
                        urlArr.append([blackurl[0], m[0]])
                    except Exception as e:
                        print(e)
                COUNT += 1

                if COUNT > page:
                    RUN = False
                    print(time.strftime("%H:%M:%S", time.localtime()), "Url读取完毕")
                    urlArr.reverse()
                    return urlArr
            else:
                RUN = False
                break
        urlArr.reverse()
        return urlArr

    def getPic(self, url):
        """
        # 获取网站截图
        Windows调用chromedriver.exe截图
        Linux调用CutyCapt截图 (需预先安装)(Ubuntu14.04下测试正常)
                Imagemagick处理图像生成缩略图
        :param url: http://google.com
        """
        # tm = time.strftime("%m-%d %H-%M-%S", time.localtime())
        tm = time.strftime("%H-%M-%S", time.localtime())
        dire = time.strftime("%m-%d", time.localtime())
        if os.path.exists("./hackimg/"):
            if not os.path.exists("./hackimg/" + dire + "/"):
                os.mkdir("./hackimg/" + dire + "/")
        else:
            os.mkdir("./hackimg/")
            if not os.path.exists("./hackimg/" + dire + "/"):
                os.mkdir("./hackimg/" + dire + "/")

        # na = str(str(tm) + ' ' + url + '.png').replace('http://', '').replace('https://', '').replace(':', ' ') \
        #     .replace('/', '_').replace('?', '%3F')
        na = tm + ' ' + self.getDomain(url)
        na = "./hackimg/" + dire + "/" + na

        if not self.LINUX:
            browser = webdriver.Chrome()
            browser.set_page_load_timeout(self.TIMEOUT)
            browser.implicitly_wait(self.TIMEOUT)
            try:
                browser.get(url)
                print(browser.title)
                browser.save_screenshot(na + '.jpg')
                browser.quit()
            except TimeoutException:
                print('time out after 20 seconds when loading page')
                browser.save_screenshot(na + '.jpg')
                browser.quit()
                # browser.execute_script('window.stop()')
            return na
        else:
            wait = str(self.TIMEOUT * 1000)
            ret = os.system('xvfb-run --server-args="-screen 0, 1000x700x24" cutycapt --max-wait=' + wait +
                            ' --url=\'' + url + '\' --out=\'' + na + '.png\'')
            os.system('convert -quality 100 \'' + na + '.png\' \'' + na + '.jpg\'')
            os.system('rm \'' + na + '\'.png')
            os.system('convert -quality 100 -crop 1000x700+0+0 \'' + na + '.jpg\' \'' + na + '.jpg\'')
            os.system('convert -quality 100 -resize 40%x40% \'' + na + '.jpg\' \'' + na + '.small.jpg\'')

            if ret == 0:
                return na
            else:
                return False

    def echo(self, urlArr, hackOrigin):
        """
        # 获取Url的IP 响应码 备案 以及截图
        :type urlArr: Url数组
        """
        for a in urlArr:
            print(a[0], "查询状态...")
            ser = self.Verify(a[0])
            if ser:
                print(a[0], "获取特征...")
                html = self.curl(a[0])
                print(a[0], "查询备案...")
                icp = self.getIcp(a[0])
                if self.PRTSC:
                    print(a[0], "获取截图...")
                    pic = self.getPic(a[0])
                else:
                    pic = ""
                if not icp:
                    if self.SAVE_SQL:
                        self.addsql(self.getDomain(a[0]), a[0], ser[0], "无", "", "", "", ser[1], time.time(), pic,
                                    html, hackOrigin, a[1])
                        print(a[0], "Domain:", self.getDomain(a[0]), "Ip:", ser[0], "city:", ser[1], "没有备案",
                              "Screenshot:", pic)
                    else:
                        print(a[0], "Domain:", self.getDomain(a[0]), "Ip:", ser[0], "city:", ser[1], "没有备案",
                              "Screenshot:", pic)
                else:
                    if self.SAVE_SQL:
                        # domain, hackweb, ip, icp, icp_name, icp_webname, icp_st, city, time, pic, origin
                        self.addsql(self.getDomain(a[0]), a[0], ser[0], icp[2], icp[0], icp[1], icp[3], ser[1],
                                    time.time(), pic, html, hackOrigin, a[1])
                        print(a[0], "Domain:", self.getDomain(a[0]), "Ip:", ser[0], "city:", ser[1], "Com:", icp[0],
                              "Name:", icp[1], "Number:", icp[2], "Property:", icp[3], "Screenshot:", pic)
                    else:
                        print(a[0], "Domain:", self.getDomain(a[0]), "Ip:", ser[0], "city:", ser[1], "Com:", icp[0],
                              "Name:", icp[1], "Number:", icp[2], "Property:", icp[3], "Screenshot:", pic)
            else:
                print(a[0], "无法访问或者不是国内网站,跳过...")
        print('done')

    def Verify(self, url):
        """
        # 验证网站
        :param url:
        :return:
        """
        doom = self.isCHINA(url)
        if doom:
            try:
                s = requests.session()
                r = s.head(url, headers=self.HEADER, timeout=self.TIMEOUT)
                if r.status_code == 200:
                    return doom
                else:
                    return False
            except Exception:
                return False
        else:
            return False

    def getDomain(self, url):
        return urlparse(url, scheme='', allow_fragments=True).netloc

    def isCHINA(self, url):
        """
        # 获取IP 并判断是否为国内网站 返回IP和归属地
        :param url:
        :return:
        """
        ret = []
        try:
            ip = socket.gethostbyname(self.getDomain(url))
            ser = IP.find(ip)
            if not ser:
                return
            else:
                if ser.find('中国') != -1:
                    ret.append(ip)
                    if ser.count("\t") == 2:
                        ret.append(str(re.findall("\t(.*)\t", ser)[0]))
                    else:
                        ret.append(str(re.findall("\t(.*)", ser)[0]))
                    return ret
                else:
                    return
        except Exception as e:
            print(e)
            return

    def addsql(self, domain, hackweb, ip, icp, icp_name, icp_webname, icp_st, city, time, pic, html, origin, locate):
        """
        # 存入数据库
        """
        try:
            session = self.DBSession()
            sql = Hack_spider(domain=domain, hackweb=hackweb, ip=ip, icp=icp, icp_name=icp_name,
                              icp_webname=icp_webname,
                              icp_st=icp_st, city=city, time=int(time), pic=pic, html=html, origin=origin,
                              locate=locate)
            session.add(sql)
            session.commit()
            session.close()
        except Exception as e:
            print(e)

    def getlastsql(self, origin):
        """
        获取最后一次入库的记录
        """
        session = self.DBSession()
        query = session.query(Hack_spider)
        ret = query.filter(Hack_spider.origin == origin).order_by(Hack_spider.id.desc()).first()
        return ret.locate

    def curl(self, url):
        """
            Curl获取页面源码等信息
            :param url:
            :return:
            """
        b = BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.CONNECTTIMEOUT, 15)
        c.setopt(pycurl.TIMEOUT, 20)
        c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
        c.setopt(pycurl.ENCODING, 'gzip')
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        # c.setopt(pycurl.NOPROGRESS, 1)
        c.setopt(pycurl.FORBID_REUSE, 1)
        c.setopt(pycurl.MAXREDIRS, 10)  # 最大重定向
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.URL, url)
        c.setopt(c.HTTPHEADER, ['Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                'Accept-Charset: UTF-8', 'Connection:keep-alive',
                                'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/49.0.2623.87 Safari/537.36'])
        try:
            c.perform()
            html = b.getvalue()
            b.flush()
            return base64.b64encode(html)

        except Exception as err:
            print(err)
            b.flush()
            return 'error'


if __name__ == '__main__':
    sp = hackspider()
    while True:
        sp.echo(sp.getHack(1, sp.getlastsql("1")), "1")
        sp.echo(sp.getHack(2, sp.getlastsql("2")), "2")
        print(time.strftime("%m-%d %H:%M:%S", time.localtime()))
        sleep(1200)


    # sp.SAVE_SQL = False
    # sp.PRTSC = False
    # sp.echo(sp.getPageHack(1, 10), "1")
    # sp.echo(sp.getPageHack(2, 10), "2")
    # print(sp.getlastsql("1"))
    # print(sp.getlastsql("2"))
