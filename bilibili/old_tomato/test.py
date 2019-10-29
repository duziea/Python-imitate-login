import requests

def get_fans_ids(): 
	url = 'https://api.bilibili.com/x/relation/followers'
	headers = {
 "Referer": "https://space.bilibili.com/546195/fans/fans",
 "Sec-Fetch-Mode": "no-cors",
 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
	}
	params = {
 "vmid": "546195",
 "pn": "1",
 "ps": "200",
 "order": "desc",
 "jsonp": "jsonp",
 "callback": "__jp25"
}
	res = requests.get(url,headers=headers,params=params)
	print(res.text)


if __name__ == "__main__":
	get_fans_ids()