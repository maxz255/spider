import pymongo
from utils import log
from utils import cached_page
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


def main():
    url = 'http://www.imdb.com/chart/top'
    page = cached_page(url, filename='imdb250.html')
    movies = movies_from_html(page)
    log(movies)


if __name__ == '__main__':
    main()
