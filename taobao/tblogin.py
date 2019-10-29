from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import json


'''
selenium模拟登陆
即使按网上教程设置开发者模式，window.navigator.webdriver=undefined
也会被淘宝检测，出现验证码
测试1：
通过selenium打开登陆页，手动输入账号密码或在网页console执行js代码，均可以成功登陆.
测试2：
通过selenium打开登陆页，selenium自动化输入，或执行js，跳出验证码。

猜测:
selenium输入、执行js时会留下痕迹，被淘宝检测到

'''
class taobao():
    def __init__(self, username, password):
        '''
        初始化
        '''
        
        options = webdriver.ChromeOptions()
        # 设置为开发者模式，避免被识别
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.url = 'https://login.m.taobao.com/login.htm?loginFrom=wap_tb'
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 8, 1)
        self.username = username
        self.password = str(password)

    def input_info(self):
        '''
        输入用户名、密码登陆
        判断是否弹出验证框
        若弹出验证框，验证，重输密码，登陆
        '''
        username_input_JS = f'document.getElementById("username").value={self.username}'
        self.browser.execute_script(username_input_JS)
        password_input = self.browser.find_element_by_id('password')
        password_input.send_keys(self.password)

        denglu_btn = self.browser.find_element_by_id('submit-btn')
        denglu_btn.click()
       
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'km-dialog-buttons')))
        ok_JS = f'return document.getElementsByClassName("km-dialog-btn")[0].click()'
        self.browser.execute_script(ok_JS)

if __name__ == "__main__":
    username = 'test123'
    password = 'test123'
    tb = taobao(username, password)
    tb.input_info()