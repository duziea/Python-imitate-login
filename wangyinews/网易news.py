import re
import time
import requests
import tldextract
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import tldextract
from urllib.parse import urlparse
from fake_useragent import UserAgent
import traceback
from saveUrl import urlDB
import cchardet

class wangyinews():
    def __init__(self):
        self.db = urlDB()

    def save_to_db(self, url, html,status_code):
        if status_code == 200:
            self.db.set_suc(url)

    def save_to_wait(self, url):
        self.db.set_wait(url)
        
    def get_wait_url(self):
        url = self.db.get_wait()
        return url

    def save_to_item(self,html):
        self.db.save_item(html)
        

    def get_all_urls(self,hub_url):
        # 下载新闻首页html
        # 新建set，存入解析出的urls，
        url = hub_url
        res = requests.get(url)
        html = res.text

        urls = set()
        soup = BeautifulSoup(html, 'lxml')
        a_lists = soup.find_all('a')
        for i in a_lists:
            try:
                url = i['href']
                urls.add(url)
            except KeyError:
                print('keyerror')
        print(f"get urls:{len(urls)}")
        return urls


    def filter_url(self,url):
        '''
        筛选url
        #判断url是否已http或https开头，去除非法url
        #判断path是否以.html结尾这，里假定新闻页面是以.html结尾
        #返回筛选后的url，存入redis带爬取urls

        '''
        if url.startswith('http') or url.startswith('https'):
            parseResult = urlparse(url)
            # print(parseResult)
            if parseResult.path.endswith('.html'):
                return url
            else:
                return ''
        
        else:
            return ''
    


    def download(self,url, timeout=10, debug=False):
        '''
        接收url和可选参数timeout，debug
        请求url，获取响应html，timeout为请求响应时间限制
        cchardet用于判断页面的编码，有时requests自动解析编码会不准确
        返回响应状态码和html 
        增加处理对应状态吗的响应
        debug用于打印请求失败的异常原因

        '''
        headers_ = {
            'UserAgent': UserAgent().random
        }

        try:
            response = requests.get(url, timeout=timeout, headers=headers_)
            status_code = response.status_code
            print(status_code)
            if status_code == 200:
                encoding = cchardet.detect(response.content)['encoding']
                html = response.content.decode(encoding)
                return html
            else:
                return False
        except:
            if debug:
                traceback.print_exc()
            msg = 'failed download: {}'.format(url)
            print(msg)
            html = ''
            status_code = 0

    def parse_html(self,html):
        


def run():
    '''
    创建实例
    1、爬取所有链接，返回urls
    2、对链接过滤，找出新闻链接，存入待爬取数据库
    '''

    wynews = wangyinews()
    hub_url = 'https://news.163.com/'
    urls = wynews.get_all_urls(hub_url)
    for url in urls:
        url = wynews.filter_url(url)
        if url:
            wynews.save_to_wait(url)

    url = wynews.get_wait_url()
    
    html = wynews.download(url)
    wynews.save_to_item(html)
    


if __name__ == "__main__":
    run()
