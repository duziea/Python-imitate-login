import re
import time
import requests
import tldextract
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import tldextract
from urllib.parse import urlparse


def save_to_db(url,html):
    # 保存网页到数据库，这里暂时用打印代替
    print(f'url:{url},html:{len(html)}')

def get_all_links():
    # 下载网易新闻首页html
    # 新建set，存入解析出的links，
    url = 'https://news.163.com/'
    res = requests.get(url)
    html = res.text

    links = set()
    soup = BeautifulSoup(html,'lxml')
    a_lists = soup.find_all('a')
    for i in a_lists:
        try:
            link = i['href']
            links.add(link)
        except KeyError:
            print('keyerror')
    print(f"get links:{len(links)}")
    return links

def filter_links(link):
    '''
    筛选link
    #判断link是否已http或https开头，去除非法link
    #判断path是否以.html结尾这，里假定新闻页面是以.html结尾
    #返回筛选后的link

    '''
    if link.startswith('http') or link.startswith('https'):
        parseResult = urlparse(link)
        # print(parseResult)
        if parseResult.path.endswith('.html'):
            return link
        
def download(link):
    '''
    下载页面内容 
    '''
    response = requests.get(link)
    html = response.text
    return html

if __name__ == "__main__":
    
    links = get_all_links()
    for i in links:
        link = filter_links(i)
        if link != None:
            # print(link)
            html = download(link)
            save_to_db(link,html)

    