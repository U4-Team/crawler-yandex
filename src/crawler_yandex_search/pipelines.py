from crawler_yandex_search.repositories import MongoRepository


class MongoPipeline(object):
    mongo_repo: MongoRepository
    def __init__(self):
        self.mongo_repo = MongoRepository()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        self.mongo_repo.store_search_item(item)
