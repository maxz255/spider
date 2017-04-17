from models import Model


class Movie(Model):
    collection_name = 'top250movie'

    def __init__(self):
        self.href = ''
        self.subject_id = ''
        self.cover_url = ''
        self.name = ''
        self.director = ''
        self.lead_act = ''
        self.rating_num = ''
        self.quote = ''
        self.ranking = ''
        self.reviews = ''


class MovieIMDB(Model):
    collection_name = 'imdb250'

    def __init__(self):
        self.href = ''
        self.id = ''
        self.cover_url = ''
        self.name = ''
        self.director = ''
        self.writers = ''
        self.stars = ''
        self.rating_num = ''
        self.ranking = ''
        self.reviews = ''
        self.date = ''


if __name__ == '__main__':
    m = Movie()
    print(m)
