import os
import pymongo
from selenium import webdriver
from pyquery import PyQuery as pq
from models.recommenditem import RecommendItem
from utils import log


driver = webdriver.PhantomJS()

db_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(db_url)
mongodb_name = 'spider'
db = client[mongodb_name]
log('数据库连接成功', db)


def cached_url(url):
    folder = 'cached_zhizhizhi'
    filename = url.split('/')[-2] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)

        driver.get(url)
        with open(path, 'wb') as f:
            f.write(driver.page_source.encode())
        content = driver.page_source
        return content


def item_from_div(div):
    e = pq(div)

    m = RecommendItem()
    m.abstract = e(".post_box_main .text").text()
    m.name = e(".title_box a").text()
    m.cover_url = e('.post_box_img img').attr('src')
    m.link = e('.post_box_go a').attr('href')
    m.save(db)
    return m


def item_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e(".post_box")
    return [item_from_div(i) for i in items]


def main():
    for i in range(0, 10):
        items = item_from_url("http://zhizhizhi.com/gn/{}/".format(i))
    driver.close()


if __name__ == '__main__':
    main()
