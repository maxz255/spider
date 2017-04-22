from models import Model


class MovieBase(Model):
    collection_name = 'movie'

    def __init__(self):
        self.id = ''
        self.date = ''
        self.href = ''
        self.cover_url = ''
        self.name = ''
        self.director = ''
        self.stars = ''
        self.rating_num = ''
        self.ranking = ''
        self.reviews = ''


class MovieDouban(MovieBase):
    collection_name = 'top250douban'

    def __init__(self):
        super().__init__()
        self.quote = ''


class MovieIMDB(MovieBase):
    collection_name = 'imdb250'

    def __init__(self):
        super().__init__()
        self.writers = ''


class MovieMtime(MovieBase):
    collection_name = 'top100mtime'

    def __init__(self):
        super().__init__()
        self.quote = ''


if __name__ == '__main__':
    m = MovieDouban()
    print(m)
