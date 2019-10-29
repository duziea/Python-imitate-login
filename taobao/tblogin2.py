import asyncio
from pyppeteer import launch
import time
import json

count = 1

async def main(username, password, url):  # 主函数
    # headless设置无界面模式
    browser = await launch({'devtools': True, 'args': ["--disable-infobars"]})
    page = await browser.newPage()
    await page.goto(url)
    print('注入js')
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')

    await page.click('a.forget-pwd.J_Quick2Static')
    print('切换到密码登录页面')
    cookie = await login(page, username, password)
    return cookie


async def login(page, username, password):  # 登录动作
    time.sleep(1)
    print('输入账号和密码')
    await page.type('input#TPL_username_1', username)
    time.sleep(1)
    await page.type('input#TPL_password_1', password)
    time.sleep(1)
    # 点击搜索按钮
    await page.click('button#J_SubmitStatic')
    time.sleep(2)
    print('点击登录')
    # 在while循环里强行查询某元素进行等待
    # while not await page.waitForXPath('//li[@id="J_SiteNavLogin"]'):
    #     return None
    print('登录成功！')

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
    with open(r'taobao/login2_cookies.json', 'w', encoding='utf-8') as f:
        json.dump(cookies, f)
        print('保存成功')



def run():
    username = 'test123'  # 输入你的账号
    password = 'test123'  # 输入你的密码
    url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/'
    # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop = asyncio.get_event_loop()
    m = main(username, password, url)
    ck = loop.run_until_complete(m)  # 将协程注册到事件循环，并启动事件循环
    return ck


def tb_cookies():
    ck = run()
    if ck is not None:
        return ck


if __name__ == '__main__':
    tb_cookies()
