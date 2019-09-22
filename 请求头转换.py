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
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 63
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: _ga=GA1.2.738763645.1569032623; _gid=GA1.2.2073357457.1569032623; user_trace_token=20190921102341-d3c86335-dc16-11e9-9460-525400f775ce; LGUID=20190921102341-d3c867a2-dc16-11e9-9460-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; LG_HAS_LOGIN=1; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; privacyPolicyPopup=false; X_MIDDLE_TOKEN=151060cdca00205497485e0188809644; WEBTJ-ID=20190922082616-16d565ca9172e3-00da6c0ad554e7-3c375c0f-1440000-16d565ca918525; JSESSIONID=ABAAABAAAFCAAEG4842E60936F2A78B7C2BD2E0279CAFBA; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216d51fab6bb304-0cf1c627201e7-3c375c0f-1440000-16d51fab6bc601%22%2C%22%24device_id%22%3A%2216d51fab6bb304-0cf1c627201e7-3c375c0f-1440000-16d51fab6bc601%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1569111976,1569112431,1569112597,1569112632; LGSID=20190922083710-1cfe35c1-dcd1-11e9-9494-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D9cHMMid5u33qKDvMtEk4oq6yS8B2hIafXaFmvJygACm%26wd%3D%26eqid%3De6f64c1b00582e78000000045d86c20f; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature%3D9BD5438CC8144BE0E272EE59981FFD63%26service%3Dhttps%25253A%25252F%25252Feasy.lagou.com%25252Fdashboard%25252Findex.htm%26action%3Dlogin%26serviceId%3Daccount%26ts%3D1569112629901; TG-TRACK-CODE=search_code; _gat=1; SEARCH_ID=920d9303e0e3464fb40ea6e2178b4059; LGRID=20190922084731-8f78d557-dcd2-11e9-a524-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1569113254; X_HTTP_TOKEN=74b8e484d8e68ed0128311965145ed0b2579be8d91
Host: www.lagou.com
Origin: https://www.lagou.com
Referer: https://www.lagou.com/jobs/list_python/p-city_0
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36
X-Anit-Forge-Code: 0
X-Anit-Forge-Token: None
X-Requested-With: XMLHttpRequest

    '''
    header_to_dict(header)