import re 
import json

def header_to_dict(header):
    dic = {}
    pattern = re.compile(r'(.*?):(.*?)\n')
    result = pattern.findall(header)
    for i in result:
        key = i[0].strip()
        value = i[1].strip()
        dic[key] = value
    print(json.dumps(dic,indent=1))
    return dic

if __name__ == "__main__":

    header = '''
openId=&pageNo=1&pageSize=10 HTTP/1.1
Host: gate.lagou.com
Content-Type: application/json
Connection: keep-alive
X-L-REQ-HEADER: {deviceType:10}
Accept: */*
User-Agent: Mozilla/5.0 (iPad; CPU OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN
Referer: https://servicewechat.com/wx7523c9b73699af14/240/page-frame.html
Accept-Language: zh-cn
Accept-Encoding: br, gzip, deflate
Content-Length: 2

    '''
    header_to_dict(header)