import asyncio
from pyppeteer import launch
import time
import json


'''
参考前辈，模拟m.taobao登陆
采用pyppeteer模拟登陆，同样是设置webdriver值
pyppeteer输入、执行js淘宝无法检测到
pyppeteer牛p
为什么pyppeteer这么牛，有没有大佬讲解一下
'''

async def main(username, password):
    #初始化
    url = 'https://login.m.taobao.com/login.htm?loginFrom=wap_tb'
    browser = await launch({'devtools':True, 'args': ["--disable-infobars"]}) 
    page = await browser.newPage()
    await page.goto(url)
    print('注入js')
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')

    '''
    输入用户名、密码登陆
    '''
    time.sleep(1)
    await page.type('#username', username)
    time.sleep(1)
    await page.type('#password', password)
    time.sleep(1)
    await page.click('#submit-btn')
    time.sleep(2)

    ck = await get_cookie(page)
    await save_cookie(ck)
    return ck


async def get_cookie(page):  # 获取登录后cookie
    cookies_list = await page.cookies()
    cookies = {}
    for cookie in cookies_list:
        name = cookie.get('name')
        value = cookie.get('value')
        cookies[name] = value
    print(cookies)
    return cookies


async def save_cookie(cookies):  # 保存到本地
    with open(r'/taobao/mtb_cookies.json', 'w', encoding='utf-8') as f:
        json.dump(cookies, f)
        print('保存成功')

def run(username, password):

    # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop = asyncio.get_event_loop()
    m = main(username, password)
    ck = loop.run_until_complete(m)  # 将协程注册到事件循环，并启动事件循环
    return ck

def mtb_cookies(username, password):
    
    ck = run(username, password)
    if ck is not None:
        return ck



if __name__ == "__main__":
    username = 'test123'  # 输入你的账号
    password = 'test123'  # 输入你的密码
    mtb_cookies(username, password)