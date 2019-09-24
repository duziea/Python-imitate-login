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
Host: app.gsxt.gov.cn
Accept-Encoding: br, gzip, deflate
Accept: application/json
User-Agent: Mozilla/5.0 (iPad; CPU OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN
Accept-Language: zh-cn
Content-Length: 229
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive

    '''
    header_to_dict(header)