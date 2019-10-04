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

class wangyinews():
    def __init__(self):
        self.db = urlDB()

    def save_to_db(self, url, html,status_code):
        if status_code == 200:
            self.db.set_suc(url)
        
        


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


    def filter_urls(self,url):
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
            encoding = cchardet.detect(response.content)['encoding']
            html = response.content.decode(encoding)
            if status_code == 302 or 301:
                html = '302 or 301'
            elif status_code == 40:
                html = '404'
            elif status_code == 502:
                html = '502'
        except:
            if debug:
                traceback.print_exc()
            msg = 'failed download: {}'.format(url)
            print(msg)
            html = ''
            status_code = 0

        return status_code, html


if __name__ == "__main__":

