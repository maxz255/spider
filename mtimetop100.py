import pymongo
from utils import log
from utils import cached_page
from models.movie import MovieMtime
from pyquery import PyQuery as pq


db_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(db_url)
mongodb_name = 'spider'
db = client[mongodb_name]
log('数据库连接成功', db)


def movies_from_html(page):
    doc = pq(page)
    lst = doc('#asyncRatingRegion li')
    movies = [movie_from_li(li) for li in lst]
    return movies


def movie_from_li(li):
    e = pq(li)
    m = MovieMtime()

    m.ranking = e('.number').text()
    m.href = e('.mov_pic a').attr('href')
    m.id = m.href.split('/')[-2]
    m.name = e('.mov_pic a ').attr('title')
    m.cover_url = e('.mov_pic img').attr('src')

    date = e('.mov_con .px14 a').text().split('(')[-1]
    m.date = date[:-1]

    p = e('.mov_con p')
    m.director = pq(p[0])('a').text()
    m.stars = pq(p[1])('a').text()
    m.type = pq(p[2])('a').text()
    m.quote = e('.mov_con .mt3').text()

    rn = list(e('.mov_point b').text())
    rn.remove(' ')
    m.rating_num = ''.join(rn)

    m.reviews = e('.mov_point p').text()

    m.save(db)
    return m


def main():
    url1 = 'http://www.mtime.com/top/movie/top100/'
    s = 'http://www.mtime.com/top/movie/top100/index-{}.html'
    urls = [url1] + [s.format(i) for i in range(2, 11)]
    for url in urls:
        filename = url.split('/')[-1]
        if filename == '':
            filename = 'index-1.html'
        page = cached_page(url, filename, folder='cached/mtime/top100')
        movies = movies_from_html(page)
        log(movies)


if __name__ == '__main__':
    main()
