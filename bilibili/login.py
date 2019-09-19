from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import base64
from PIL import Image
import json


class bili():
    def __init__(self, username, password):
        '''
        初始化
        '''
        options = webdriver.ChromeOptions()
        # 设置为开发者模式，避免被识别
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.url = 'https://passport.bilibili.com/login'
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 8, 1)
        self.username = username
        self.password = password

    def input_info(self):
        #输入账号密码
        username_input = self.browser.find_element_by_css_selector(
            '#login-username')
        username_input.send_keys(username)
        password_input = self.browser.find_element_by_css_selector(
            '#login-passwd')
        password_input.send_keys(password)
        #登陆
        denglu_JS = 'return document.getElementsByClassName("btn btn-login")[0].click()'
        self.browser.execute_script(denglu_JS)

    def get_image(self):
        '''
        获取图片
        fullbg：完整背景图
        bg：缺口背景图      
        slice：滑块图
        默认存储在当前路径img文件夹下

        '''
        fullbg_JS = 'return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png");'
        fullbg_info = self.browser.execute_script(fullbg_JS)
        fullbg_base64 = fullbg_info.split(',')[1]
        fullbg = base64.b64decode(fullbg_base64)
        with open('bilibili/img/fullbg.png', 'wb') as f:
            f.write(fullbg)

        slice_JS = 'return document.getElementsByClassName("geetest_canvas_slice geetest_absolute")[0].toDataURL("image/png");'
        slice_info = self.browser.execute_script(slice_JS)
        slice_base64 = slice_info.split(',')[1]
        slice = base64.b64decode(slice_base64)
        with open('bilibili/img/slice.png', 'wb') as f:
            f.write(slice)

        bg_JS = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
        bg_info = self.browser.execute_script(bg_JS)
        bg_base64 = bg_info.split(',')[1]
        bg = base64.b64decode(bg_base64)
        with open('bilibili/img/bg.png', 'wb') as f:
            f.write(bg)

    def get_end(self):
        '''
        两层for循环,做差比对x轴上每个y的rgb值，
        当差值大于阀值则返回end = x轴坐标
        end即为滑动的终点
        '''
        bg_path = 'bilibili/img/bg.png'
        fullbg_path = 'bilibili/img/fullbg.png'
        bg = Image.open(bg_path)
        fullbg = Image.open(fullbg_path)
        threhold = 60
        for i in range(bg.size[0]):
            for j in range(bg.size[1]):
                rgb1 = bg.load()[i, j]
                rgb2 = fullbg.load()[i, j]
                res1 = abs(rgb1[0] - rgb2[0])
                res2 = abs(rgb1[1] - rgb2[1])
                res3 = abs(rgb1[2] - rgb2[2])
                if not (res1 < threhold and res2 < threhold
                        and res3 < threhold):
                    end = i
                    print(end)
                    return end

    def get_start(self):
        '''
        判断滑块图的rgb值，
        若透明度大于阀值，
        返回start = x的横坐标
        start即为滑动的起点
        
        '''
        slice_path = 'bilibili/img/slice.png'
        slice = Image.open(slice_path)
        for i in range(slice.size[0]):
            for j in range(slice.size[1]):
                rgb = slice.load()[i, j]
                if rgb[3] >= 125:
                    start = i
                    print(start)
                    return start

    def get_track(self, distance):
        '''
        输入要滑动距离distance = end-start
        模拟滑动距离,
        先加速滑动后减速，滑过了，再滑回
        输出每次滑动的轨迹track
        '''
        v = 10
        a = 0
        t = 1
        track = []
        s = 0
        mid = distance / 2
        while s < distance:
            if s < mid:
                a = 6 * random.random()
            else:
                a = -3 * random.random()
            v0 = v
            v = v0 + a * t
            s0 = v0 * t + 1 / 2 * a * t * t
            s += abs(s0)
            track.append(s0)
        d = distance - s
        track.append(d)
        print(track)
        return track

    def move_slider(self, track):
        '''
        输入：滑动轨迹track
        定位滑块单击并保持按住，for循环track，滑动
        sleep 1 秒，释放
        '''
        slider_btn = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_slider.geetest_ready > div.geetest_slider_button'
            )))
        ActionChains(self.browser).click_and_hold(slider_btn).perform()
        for i in track:
            ActionChains(self.browser).move_by_offset(xoffset=i,
                                                      yoffset=0).perform()
        time.sleep(1)
        ActionChains(self.browser).release(slider_btn).perform()

    def get_cookie(self):
        '''
        获取登陆后cookie值，保存
        '''
        cookie = self.browser.get_cookies()
        with open('bilibili/cookie.json', 'w') as f:
            json.dump(cookie, f)

    def test(self,n=0):
        '''
        输入n，
        尝试定位登陆成功后的消息元素，
        若定位成功，返回suc
        定位失败，重新尝试登陆，n+=1
        当n>3，返回登陆失败
        '''
        if n < 3:
            try:
                self.wait.until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        '#app > div.bili-header-m.report-wrap-module > div.nav-menu > div.nav-wrapper.clearfix.bili-wrapper > div.nav-con.fr > ul > li:nth-child(3) > a'
                    )))
                print('suc')
                result = 'suc'
                return result
            except TimeoutException:
                print('fail',n)
                time.sleep(3)
                self.get_image()
                distance = self.get_end() - self.get_start()
                track = self.get_track(distance)
                self.move_slider(track)
                n += 1
                self.test(n)
        else:
            result = 'fail'
            return result

    def close(self):
        self.browser.close()
        

    def start_project(self):
        '''
        self.input_info()：登陆，
        self.wait.until：等待画布元素出现
        self.get_image()：获取图片
        distance：计算滑动距离
        track：生成滑动轨迹
        self.move_slider(track)：模拟滑动
        self.test()：尝试3次
        self.get_cookie()：获取cookie

        '''
        self.input_info()
        self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div'
            )))
        self.get_image()
        distance = self.get_end() - self.get_start()
        print(distance)
        track = self.get_track(distance)
        self.move_slider(track)
        self.test()
        self.get_cookie()
        self.close()
        print('finish')


if __name__ == "__main__":
    username = 'test123'
    password = 'test123'
    b = bili(username, password)
    b.start_project()