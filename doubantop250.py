import requests
import os
import string
import random
import pymongo
from utils import log
from models.movie import Movie
from pyquery import PyQuery as pq


db_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(db_url)
mongodb_name = 'spider'
db = client[mongodb_name]
log('数据库连接成功', db)


def movies_from_html(page):
    doc = pq(page)
    # log(e)
    items = doc('.item')
    movies = [movie_from_div(div) for div in items]
    # movie_from_div(items[0])
    return movies


def movie_from_div(div):
    e = pq(div)

    m = Movie()
    m.href = e('a').attr('href')
    m.subject_id = m.href.split('/')[-2]
    m.cover_url = e('img').attr('src')
    m.name = e('.title').text()
    # m.director = ''
    m.rating_num = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.ranking = e('.pic').find('em').text()
    m.reviews = e('.star').find('span')[-1].text

    m.save(db)

    return m


def make_bid():
    s = string.ascii_letters + string.digits + '_-'
    random_list = random.sample(s, 11)
    bid = ''.join(random_list)
    return bid


def make_header():
    bid = 'bid={}'.format(make_bid())
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64)'
                       ' AppleWebKit/537.36 (KHTML, like Gecko)'
                       ' Chrome/57.0.2987.98 Safari/537.36'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': bid,
    }
    return headers


def cached_page(url):
    folder = 'cached'
    filename = url.split('=')[-1] + '.html'
    path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)

    if os.path.exists(path):
        with open(path, 'rb') as f:
            page = f.read()
            return page
    else:
        header = make_header()
        response = requests.get(url, header)
        page = response.content
        with open(path, 'wb') as f:
            f.write(page)
        return page


def main():
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        page = cached_page(url)
        movies = movies_from_html(page)
        # log(movies)

if __name__ == '__main__':
    main()
