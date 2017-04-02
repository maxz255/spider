class Mixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{} = {}'.format(k, v) for k, v in self.__dict__.items())
        return '\n<{}:\n  {}\n>'.format(class_name, '\n  '.join(properties))


class Model(Mixin):
    collection_name = ''

    def save(self, db):
        m = self.__dict__
        self.insert(db, **m)

    def insert(self, db, **kwargs):
        db[self.collection_name].insert(kwargs)

    def find_all(self):
        ms = self.find_by()
        return ms

    def all(self, db):
        query = {
            '_deleted': False,
        }
        ms = []
        for m in db[self.collection_name].find(query):
            m.pop('_deleted')
            ms.append(u)
        return ms

    def find_by(self, db, **query):
        ms = list(db[self.collection_name].find(query))
        return ms

    def find_cond(self, db, **field):
        query = {}
        ms = list(db[self.collection_name].find(query, field))
        return ms

    def update(self, db, query=None, form=None, options=None):
        if query is None:
            query = {}
        if form is None:
            form = {}
        if options is None:
            options = {
                'multi': True,
            }
        db[self.collection_name].update(query, form, **options)

    def delete_by(self, db, **query):
        form = {
            '$set': {
                '_deleted': True,
            }
        }
        db[self.collection_name].update(query, form)
