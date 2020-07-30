from bs4 import BeautifulSoup
import re
import requests
import threading
#请求头
Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36',
        'Referer': 'http://konachan.wjcodes.com/index.php?tag=%20width:%3E=1920%20height:%3E=1080&p=10',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
          }

Furl = 'http://konachan.wjcodes.com/index.php?tag=%20width:%3E=1920%20height:%3E=1080'
#最大线程数量
threadMax = threading.BoundedSemaphore(8)
"""
函数说明：
创建线程执行下载任务
"""
class ThreadDL(threading.Thread):
    def __init__(self,Durl,title,t):
        threading.Thread.__init__(self)
        self.title = title
        self.t = t
        self.Durl = Durl
    def run(self) :
        Download_pic(Durl,title,t)
"""
函数说明：
    获取当前页面图片下载链接
"""
def get_url(Surl):
    DurlList = []
    url_req = requests.get(Surl,Headers)
    bf = BeautifulSoup(url_req.text)
    button = bf.find_all('button', class_='am-btn am-btn-secondary am-btn-xs')
    for it in button:
        print(it)
        res = it["onclick"]
        Durl = re.findall('\(\'(.*)\',', res)
        DurlList.append(Durl[0])
    return DurlList
"""
函数说明：
    下载并保存图片
"""
def Download_pic(Durl,title,t):
    title = title+'.jpg'
    try:
        pic_req = requests.get(Durl,Headers).content
    except requests.exceptions.ConnectionError as e:
        print("连接超时")
        return
    print("正在下载第%d张图片"%t)
    with open(title,'wb') as f:
        f.write(pic_req)
        f.close()
        threadMax.release()
    print(title,'下载成功')
"""
函数说明：
    获取页面链接
"""
def get_Surl(Furl,index):
    Surl = Furl+'&p='+str(index)
    return Surl
if __name__ == '__main__':
    t = 0
    for i in range(2,3):
        Surl = get_Surl(Furl,i)
        DurlList = get_url(Surl)
        print('连接成功')
        for Durl in DurlList:
            threadMax.acquire()
            title = str(t)+'__'+'pic'
            print("创建新线程：%d"%t)
            sta = ThreadDL(Durl,title,t)
            sta.start()
            t = t+1
