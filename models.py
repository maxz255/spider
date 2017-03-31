class Mixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{} = {}'.format(k, v) for k, v in self.__dict__.items())
        return '\n<{}:\n  {}\n>'.format(class_name, '\n  '.join(properties))


class Movie(Mixin):

    def __init__(self):
        self.href = ''
        self.subject_id = ''
        self.name = ''
        self.director = ''
        self.lead_act = ''
        self.rating_num = ''
        self.quote = ''
        self.cover_url = ''
        self.ranking = ''
        self.reviews = ''


if __name__ == '__main__':
    m = Movie()
    print(m, m, m)