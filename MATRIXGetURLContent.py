import requests
import bs4
import urllib
import urllib.request

from tqdm import tqdm

import os

import re
import csv
import chardet
from urllib.parse import urljoin
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from selenium import webdriver
import socket
import time
from lxml import etree


def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    """
    print(urlopen(url).info())
    # output
    Server: AliyunOSS
    Date: Tue, 19 Dec 2017 06:55:41 GMT
    Content-Type: application/octet-stream
    Content-Length: 29771146
    Connection: close
    x-oss-request-id: 5A38B7EDCE2B804FFB1FD51C
    Accept-Ranges: bytes
    ETag: "9AA9C1783224A1536D3F1E222C9C791B-6"
    Last-Modified: Wed, 15 Nov 2017 10:38:33 GMT
    x-oss-object-type: Multipart
    x-oss-hash-crc64ecma: 14897370096125855628
    x-oss-storage-class: Standard
    x-oss-server-time: 4
    """
    filename = dst
    # filename = "/home/mydir/test.txt"

    # 将文件路径分割出来

    file_dir = os.path.split(filename)[0]

    # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        print(f"Download Program Will create directory {file_dir}")
        os.makedirs(file_dir)

    # 然后再判断文件是否存在，如果不存在，则创建
    if not os.path.exists(filename):
        os.system(r'touch %s' % filename)

    # 断点续传
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


def findAllLink(url):
    '''
    提取网页中的超链接
    '''

    # url = "http://blog.csdn.net"
    # 2.根据需求构建好链接提取的正则表达式
    pattern1 = '<.*?(href=".*?").*?'
    # 3.模拟成浏览器并爬取对应的网页 谷歌浏览器
    headers = {'User-Agent',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    data = opener.open(url).read().decode('utf8')
    # 4.根据2中规则提取出该网页中包含的链接
    content_href = re.findall(pattern1, data, re.I)
    # print(content_href)
    # 5.过滤掉重复的链接
    #    # 列表转集合(去重) list1 = [6, 7, 7, 8, 8, 9] set(list1) {6, 7, 8, 9}
    set1 = set(content_href)
    # print(set1)

    # 6.后续操作，比如打印出来或者保存到文件中。
    file_new = "./href.txt"
    with open(file_new, 'w') as f:
        for i in set1:
            f.write(i)
            f.write("\n")
    f.close()

    print(f"已经生成文件{file_new}")

    return set1


def findAllLink1(url):
    headers = ("User-Agent",
               "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    file = urllib.request.urlopen(url).read()
    file = file.decode('utf-8')
    pattern = '(https?://[^\s)";]+(\.(\w|/)*))'
    links = re.compile(pattern).findall(file)
    # 去重
    links = list(set(links))

    # print(links)
    return links


def findAllLink2(url):
    file = open('result.csv', 'w', encoding='utf-8', newline='')
    cw = csv.writer(file)
    cw.writerow(['URL', 'Anchor'])

    resp = requests.get(url)
    encoding = chardet.detect(resp.content)["encoding"]
    # print(encoding)
    resp.encoding = encoding
    links = re.findall(r'<a.*?href="(.*?)".*?>(.*?)</a>', resp.text, re.S | re.I)
    for link in links:
        a = urljoin(url, link[0]), link[1]
        print(a)
        cw.writerow(a)

    file.close()

    links = list(set(links))  # 标准去重

    return links


def findAllLink3(url):
    # 获取请求
    req = urllib.request.Request(url)
    # 打开页面
    webpage = urllib.request.urlopen(req)
    # 读取页面内容
    html = webpage.read()
    # 解析成文档对象
    soup = bs4.BeautifulSoup(html, 'html.parser')  # 文档对象
    # 非法URL 1
    invalidLink1 = '#'
    # 非法URL 2
    invalidLink2 = 'javascript:void(0)'
    # 集合
    links = set()
    # 计数器
    mycount = 0
    # 查找文档中所有a标签
    for k in soup.find_all('a'):
        # print(k)
        # 查找href标签
        link = k.get('href')
        # 过滤没找到的
        if (link is not None):
            # 过滤非法链接
            if link == invalidLink1:
                pass
            elif link == invalidLink2:
                pass
            elif link.find("javascript:") != -1:
                pass
            else:
                mycount = mycount + 1
                # print(mycount,link)
                links.add(link)
    # print("打印超链接个数:",mycount)
    # print("打印超链接列表",result)

    f = open(r'result.txt', 'w', encoding='utf-8')  # 文件路径、操作模式、编码  # r''
    for a in links:
        f.write(a + "\n")
    f.close()
    print("\r\n扫描结果已写入到result.txt文件中\r\n")

    links = list(set(links))  # 标准去重
    return links


def findAllLink4(url):
    # 获取请求
    html = urlopen(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')  # 文档对象
    links = []
    t1 = soup.find_all('a')
    for t2 in t1:
        t3 = t2.get('href')
        links.append(t3)

    links = list(set(links))  # 标准去重
    return links


def findAllLink5(url):
    r = requests.get(url)
    status_code = r.status_code
    content = bs4.BeautifulSoup(r.content.decode("utf-8"), "lxml")

    element = content.find_all('a')
    # element[26].get('href')

    atag = content.find_all('a')
    hrefs = [item.get('href') for item in atag if item.get('href')]

    t = content.find('a', atrrs={'download': 'gman'})

    links = hrefs
    links = list(set(links))  # 标准去重

    return links


def findAllLink6(url, verbose=False):
    r = requests.get(url)
    status_code = r.status_code
    content = bs4.BeautifulSoup(r.content.decode("utf-8"), "lxml")
    links = set()
    for link in content.findAll('a'):
        if link.has_attr('href'):
            href = str(link.get('href'))
            if href.startswith('http'):
                links.add(href)
                if verbose:
                    print(link.get('href'))

    links = list(set(links))  # 标准去重

    return links


def findAllLink7(url):
    page = requests.get(url)
    a = BeautifulSoup(page.text, "lxml").findAll('a')
    links = dict(map(lambda i: {i.text.strip(), i.attrs['href']}, a))

    for item in links:
        if ".zip" in links[item] and "www.matrix.io" in links[item]:
            pzip_r = requests.get(links[item])
            with open(item + ".zip", "wb") as zip_file:
                zip_file.write(pzip_r.content)

    links = list(set(links))  # 标准去重

    return links


def findAllLink8(url):
    r = requests.get(url)
    r.encoding = 'gb2312'

    print("\n Happy open.....1!")
    # 利用 re （太黄太暴力！）
    links1 = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", r.text)
    for link in links1:
        print(link)

    print("\n Happy open.....2!")
    # 利用 BeautifulSoup4 （DOM树）
    links2 = set()
    soup = BeautifulSoup(r.text, 'lxml')
    for a in soup.find_all('a'):
        link = a['href']
        links2.add(link)
        print(link)

    print("\n Happy open.....3!")

    # 利用 lxml.etree （XPath）
    links3 = set()
    tree = etree.HTML(r.text)
    for link in tree.xpath("//@href"):
        links3.add(link)
        print(link)

    print("\n Happy open.....4!")

    links4 = set()
    soup = BeautifulSoup(r.text, 'lxml')
    for iframe in soup.find_all('iframe'):
        url_ifr = iframe['src']  # 取得当前iframe的src属性值

        rr = requests.get(url_ifr)
        rr.encoding = 'gb2312'

        soup_ifr = BeautifulSoup(rr.text, 'lxml')

        for a in soup_ifr.find_all('a'):
            link = a['href']
            m = re.match(r'http:\/\/.*?(?=\/)', link)
            # print(link)
            if m:
                links4.add(m.group(0))

    # 利用selenium（要开浏览器！）
    # driver = webdriver.Chrome()
    # driver.get(url)
    # for link in driver.find_elements_by_tag_name("a"):
    #     print(link.get_attribute("href"))
    # driver.close()
    print("\n Finish Display....!")

    links = links1
    links = list(set(links))  # 标准去重
    return links

def get_static_url_content(url, encoding='utf-8', timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    '''
    获取静态网页内容
    :param url:         网页url
    :param encoding:    网页编码
    :param timeout:     设置超时
    :return:
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url, headers=headers)
    html = urlopen(req, timeout=timeout)
    bsObj = BeautifulSoup(html.read(), "html.parser", from_encoding=encoding)
    return bsObj


def get_driver_url_content(url, encoding='utf-8', timeout=3):
    '''
    使用浏览器获取动态内容
    :param url:         网页url
    :param encoding:    网页编码
    :param timeout:     设置超时
    :return:
    '''
    chromedriver_path = '/path/to/chromedriver'
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    # 也可以使用phantomJS
    # driver =webdriver.Phantomjs(executable_path="/path/to/phantomjs")
    driver.get(url)
    time.sleep(timeout)
    bsObj = BeautifulSoup(driver.page_source, 'html.parser', from_encoding=encoding)
    driver.close()
    return bsObj


def load_appendix(url, filename):
    '''
    下载附件, 将URL下载到filname里面
    :param url:         附件 url(附件文档和图片均可)
    :param filename:    保存的文件名
    :return:
    '''
    urlretrieve(url, filename)


def filterlink(links, filename):

    filterlinks=set()
    for item in links:
        for singlefile in filename:
            if singlefile in links[item]:
                filterlinks.add(item)

    filterlinks = list(set(filterlinks))  # 标准去重

    return filterlinks

def filterlink1(links, filename):

    return map(lambda x: filename in x,links)

if __name__ == '__main__':
    # url = "https://www.matrix.io/uploads/file/gman(mac).zip"
    # download_from_url(url, "./Download/gman.zip")
    url = 'https://www.matrix.io/downloads/'
    links=findAllLink8(url)
    for i in links:
        print(i)

    # load_appendix(url,"a.txt")
    result=filterlink1(links,["pdf",".zip"])
    print(result)