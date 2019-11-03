import random
import cv2
import requests

# url = 'https://www.baidu.com'
get_url = 'http://httpbin.org/get'
post_url = 'http://httpbin.org/post'
my_loal_url = 'http://58.87.122.42:1214/ZhangChunbo/uploading/'
# my_loal_url = 'http://127.0.0.1:8000/ZhangChunbo/uploading/'

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
UA = random.choice(user_agent_list)
headers = {'User-Agent': UA,
            'Referer': my_loal_url
            }

s = requests.Session()
r1 = s.get(my_loal_url, headers=headers)
csrf_token = r1.cookies['csrftoken']
print(csrf_token)
print(r1.headers)
# post file test
# 修改图片路径即可
files = {'img': ('jng.png', open('jng.png', 'rb'), 'image/png')}
print(files)
r = s.post(my_loal_url, files=files, data={'csrfmiddlewaretoken': csrf_token}, headers=headers)
print(r.status_code)

# r = requests.get(get_url)
# r2 = requests.get(my_url+'/polls/add/?a=3&b=4')
# print(r.text)
# print(r2.text)
