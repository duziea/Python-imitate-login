import requests
import json
import time
from fake_useragent import UserAgent

class lagou():
    def __init__(self):
        self.get_session_url = 'https://www.lagou.com/jobs/list_python/p-city_0?px=default&gx=&isSchoolJob=1#filterBox'
        self.get_positon_url = "https://www.lagou.com/jobs/positionAjax.json?city=全国&needAddtionalResult=false"
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
            'user-Agent': str(UserAgent().random)
        }
        self.dic_position=[]
    
    def get_session(self):
        '''
        获取session，用与之后的模拟ajax请求
        '''
        s = requests.Session()
        s.get(self.get_session_url,headers=self.headers,verify=False)

        return s

    def get_positon(self,s,data,params):
        '''
        模拟ajax请求获取职业信息
        '''
        response = s.post(self.get_positon_url, headers=self.headers,
                                data=data, params=params, verify=True)
        print(response)
        text = response.text
        return text


    def parse_jobinfo(self,text):
        '''
        解析职业信息
        '''
        dic_text = json.loads(text)
        content = dic_text['content']
        showId = content['showId']         #用与组成detail_url
        positionResult = content['positionResult']
        result = positionResult['result']

        for i in result:
            info = {}
            positionId = i['positionId']  #职位id，用于组成detail_url

            info['positionName'] = i['positionName']   #职位名
            info['salary'] = i['salary']                #薪水   
            info['workYear'] = i['workYear']            #工作经验
            info['education'] = i['education']          #教育经历
            info['createTime'] = i['createTime']        #发布时间
            info['jobNature'] = i['jobNature']          #工作类型
            info['companyfullname'] = i['companyFullName']      #公司名
            info['skillLables'] = i['skillLables']      #技能标签
            info['detail_url'] = f'https://www.lagou.com/jobs/{positionId}.html?show={showId}'       #职位详情url
            info['city'] = i['city']
            self.dic_position.append(info)

        print('suc')
        return 'suc'    
    
    def save_as_josn(self):
        '''
        保存为json文件
        '''
        with open(r'lagou\pythonjobinfo.json', 'a+', encoding='utf-8') as f:
            json.dump(self.dic_position, f, ensure_ascii=False)
        
        print('save suc')


if __name__ == "__main__":

    data = {
        "first": "True",
        "pn": '',
        "kd": "python"                  
    }
    params = {
        "needAddtionalResult": "false",
        "isSchoolJob": "1"
    }   

    lg = lagou()
    s = lg.get_session()
    for i in range(1,11):
        data['pn'] = str(i)
        text = lg.get_positon(s,data=data,params=params)
        lg.parse_jobinfo(text)
        print(f'爬取第{i}页')
    
    lg.save_as_josn()