import time
import requests,gevent
import urllib


def f(url):
    text = urllib.request.urlopen(url)
    # 解析 html文件
    #html = text.text
   #print('解析结果', html)

def f1(url):
    text = requests.get(url)

url = 'https://club.jd.com/comment/skuProductPageComments.action?productId=3938531&score=0&sortType=6&page=0d&pageSize=10&isShadowSku=0'
start = time.time()
thread = []
count = 0
while True:
      count +=1
      thread.append(gevent.spawn(f,url))
      if len(thread) == 2000:
          break

gevent.joinall(thread)
end = time.time()

print (end-start)