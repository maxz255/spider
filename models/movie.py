from models import Mixin


class Movie(Mixin):

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


if __name__ == '__main__':
    m = Movie()
    print(m)
