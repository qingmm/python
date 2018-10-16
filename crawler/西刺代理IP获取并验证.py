#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
from urllib import request
import sys
import os
import re
import codecs

def getProxyIp():
    url = 'http://www.xicidaili.com/'
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response, 'lxml') # 解析获取到的html
    ip_text = soup.findAll('tr', {'class': 'odd'}) # 获取带有IP地址的表格的所有行
    ip_list = []
    for i in range(len(ip_text)):
        ip_tag = ip_text[i].findAll('td')   
        ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text() # 提取出IP地址和端口号
        is_anonymous = ip_tag[4].get_text() == u'高匿'
        if is_anonymous:
            ip_list.append(ip_port)
    print(u"共收集到了{}个高匿代理IP".format(len(ip_list)))
    # print (ip_list)
    return ip_list

def ipTest(ip):
        #访问网址
    url = 'https://www.whatismyip.com/' # 能够检测出本机ip
    proxy = {'http':ip}    
    proxy_support = request.ProxyHandler(proxy) # 创建ProxyHandler    
    opener = request.build_opener(proxy_support) # 创建Opener
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    request.install_opener(opener)
    response = request.urlopen(url) # 使用自己安装好的Opener
    html = response.read().decode("utf-8") # 读取相应信息并解码
    pattern = re.compile(ip.split(':')[0]) # 定义正则表达式，若html中查找到当前ip，则说明代理ip有效
    if pattern.findall(html):
        print (ip, ' is success!')
        with codecs.open(sys.path[0] + os.sep + 'test.html', 'w', 'utf-8') as f:
            f.write(html)

if __name__ == '__main__':
    ip_list = getProxyIp()
    for ip in ip_list:
        ipTest(ip)
