from typing import List,Dict

from core.repositories import BaseMongoRepository


class MongoRepository(BaseMongoRepository):
    def get_short_data_of_all_companies(self):
        return self._client.crawlerDataset.companies.find({}, {'COMPANY_SHORT_NAME': 1, 'INN': 1})

    def count_short_data_of_all_companies(self):
        return self._client.crawlerDataset.companies.count()

    def store_search_item(self, search_item: Dict):
        if not self._client.crawlerSearchLinks.searchItems.find_one(search_item):
            self._client.crawlerSearchLinks.searchItems.insert_one(search_item)