import requests
import os
import pymongo
from utils import log
from models.movie import MovieIMDB
from pyquery import PyQuery as pq


db_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(db_url)
mongodb_name = 'spider'
db = client[mongodb_name]
log('数据库连接成功', db)


def movies_from_html(page):
    doc = pq(page)
    lister_list = doc('.lister-list')
    trs = lister_list('tr')
    movies = [movie_from_trs(tr) for tr in trs]
    return movies


def movie_from_trs(tr):
    m = MovieIMDB()
    e = pq(tr)
    from_poster_column(e, m)
    from_title_column(e, m)
    from_rating_column(e, m)
    m.save(db)
    return m


def from_poster_column(e, m):
    poster_column = e('.posterColumn')
    spans = poster_column('span')
    ranking = e(spans[0]).attr('data-value')
    reviews = e(spans[3]).attr('data-value')

    m.ranking = ranking
    m.reviews = reviews


def from_title_column(e, m):
    title_column = e('.titleColumn')
    a = title_column('a')
    href = a.attr('href')
    id_num = href.split('/')[2]
    href = 'http://www.imdb.com/title/' + id_num + '/'
    title = a.attr('title')
    director, stars = title.split(', ', 1)
    name = a.text()
    date = title_column('.secondaryInfo').text()
    date = date[1:-1]  # '(1994)' -> '1994'

    m.id, m.href, m.director, m.stars, m.name, m.date = id_num, href, director, stars, name, date


def from_rating_column(e, m):
    rating_num = e('.imdbRating').text()
    m.rating_num = rating_num


def make_header():
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64)'
                       ' AppleWebKit/537.36 (KHTML, like Gecko)'
                       ' Chrome/57.0.2987.98 Safari/537.36'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    return headers


def cached_page(url):
    folder = 'cached'
    filename = 'imdb250.html'
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
    url = 'http://www.imdb.com/chart/top'
    page = cached_page(url)
    movies = movies_from_html(page)
    log(movies)

if __name__ == '__main__':
    main()
