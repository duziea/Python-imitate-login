import requests
from fake_useragent import UserAgent
import json


def gjqy(name):
    url = 'https://app.gsxt.gov.cn/gsxt/corp-query-app-search-1.html'

    headers = {
        "Host": "app.gsxt.gov.cn",
        "Accept-Encoding": "br, gzip, deflate",
        "Accept": "application/json",
        "User-Agent": UserAgent().random,
        "Accept-Language": "zh-cn",
        "Content-Length": "229",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive"
    }

    data = {
        'conditions' : '{"excep_tab": "0", "ill_tab": "0", "area": "0","cStatus": "0", "xzxk": "0", "xzcf": "0", "dydj": "0"}',
        'searchword' : name,
        'sourceType' : 'W'
    }

    response = requests.post(url,headers=headers,data=data,verify=False)
    print(response)
    json_data = json.loads(response.text)
    data = json_data['data']
    result= data['result']
    data_list = result['data']
    for i in data_list:
        print(i['entName'])


if __name__ == "__main__":
    gjqy('小米')
