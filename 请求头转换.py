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
g_tk: 5381
loginUin: 0
hostUin: 0
format: json
inCharset: utf8
outCharset: GB2312
notice: 0
platform: yqq.json
needNewCode: 0
cid: 205360772
reqtype: 2
biztype: 1
topid: 237773700
cmd: 6
needmusiccrit: 0
pagenum: 1
pagesize: 15
lasthotcommentid: song_237773700_2546934840_1568395549
domain: qq.com
ct: 24
cv: 10101010
    '''
    header_to_dict(header)