import requests
from fake_useragent import UserAgent
import json
import time


class lagou():
    def __init__(self):
        self.ua = UserAgent().random

    def get_cookie(self):
        url = 'https://www.lagou.com/jobs/list_python/p-city_0?px=default&gx=&isSchoolJob=1#filterBox'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
            'user-Agent': UserAgent().random,
            'Connection':'close'
        }
        response = requests.get(url, headers=headers,verify=True)
        cookies = response.cookies.get_dict()

        print(cookies)

        return (cookies)

    def lagou(self, cookies,i):

        url = "https://www.lagou.com/jobs/positionAjax.json?city=全国&needAddtionalResult=false"
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
            'user-Agent': str(self.ua),
            'Connection':'close'
        }
        data = {
            "first": "True",
            "pn": str(i),
            "kd": "python"
        }
        response = requests.post(
            url, data=data, headers=headers, cookies=cookies)
        text = response.text
        return text

    def parse(self,text,i):
        dic_text = json.loads(text)
        if 'content' in dic_text:
            content = dic_text['content']
            print(content)
            return content
        else:
            self.ua = UserAgent().random
            cookies = self.get_cookie()
            text = self.lagou(cookies,i)
            self.parse(text,i)

             
        

if __name__ == "__main__":
    lagou = lagou()
    
    for i in range(1,30):
        cookies = lagou.get_cookie()
        time.sleep(10)
        # text = lagou.lagou(cookies,i)
        # lagou.parse(text,i)
