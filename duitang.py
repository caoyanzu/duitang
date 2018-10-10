# -*- coding: utf-8 -*-
import requests
import urllib.parse
import threading
#设置最大线程锁
thread_lock = threading.BoundedSemaphore(value = 5)

#获取网页
def get_url(url):
    page = requests.get(url)
    page = page.content
    page = page.decode()
    return(page)

#获取所有网页
def page_from_duitang(label):
    pages = []
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=100'
    label = urllib.parse.quote(label)
    for index in range(0,1600,100):
        u = url.format(label,index)
        print(u)
        page = get_url(u)
        pages.append(page)
    return(pages)

#图片获取模式
def find_all_pages(page,startpart,endpart):
    string = []
    end = 0
    while page.find(startpart,end) != -1:
        start = page.find(startpart,end) + len(startpart)
        end = page.find(endpart,start)
        strings = page[start:end]
        string.append(strings)
    return(string)

#获取图片url
def pic_urls_from_page(pages):
    pic_url = []
    for page in pages:
        urls = find_all_pages(page,'"path":"','"')
        pic_url.extend(urls)
    return(pic_url)

#下载图片
def download_pics(url,n):
    r = requests.get(url)
    path = '堆糖/' + str(n) + '.jpg'
    with open(path,'wb') as f:
        f.write(r.content)
    thread_lock.release()

def main(label):
    pages = page_from_duitang(label)
    pic_urls = pic_urls_from_page(pages)
    n = 0
    for url in pic_urls:
        n += 1
        print('正在下载第{}张图片',format(n))
        thread_lock.acquire()
        t = threading.Thread(target = download_pics,args = (url,n))
        t.start()

main('烈火鸟')

