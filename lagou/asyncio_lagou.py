import json
import asyncio
import aiohttp
from fake_useragent import UserAgent
import random


async def exceptJob(positionType,job=None,salary=None,positionFirstType=None,city=None,
                    positionSecondType=None,salaryLower=1,salaryUpper=100):
    '''
    input params
        "city": "",
        "positionType": "Python",
        "job": "",
        "salary": ""
        "positionFirstType": "",
        "positionSecondType": "",
        "salaryLower": 1,
        "salaryUpper": 100,
        "openId": "随意"后面查询职位要用到

    return openID 用于之后爬取positionID
    '''

    url = 'https://gate.lagou.com/v1/entry/expcetJob/saveExceptJob'

    headers = {
        "Host": "gate.lagou.com",
        "Content-Type": "application/json",
        "Accept-Encoding": "br, gzip, deflate",
        "Connection": "keep-alive",
        "X-L-REQ-HEADER": "{deviceType:10}",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN",
        "Referer": "https://servicewechat.com/wx7523c9b73699af04/240/page-frame.html",
        "Accept-Language": "zh-cn",
        "Content-Length": "149"
    }
    openId = positionType + str(random.randint(1000,9999))

    data = {
        "city": '',
        "positionType": 'python',
        "job": job,
        "salary": salary,
        "positionFirstType": positionFirstType,
        "positionSecondType": positionSecondType,
        "salaryLower": 1,
        "salaryUpper": 100,
        "openId": openId
    }


    
    print(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(url,formdata=data,headers=headers) as resp:
            print(resp.status)
            print(await resp.text())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [exceptJob(positionType='python')]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

