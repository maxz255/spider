from models import Model


class RecommendItem(Model):
    collection_name = 'recommend_item'

    def __init__(self):
        self.title = ''
        self.cover_url = ''
        self.abstract = ''
        self.link = ''
