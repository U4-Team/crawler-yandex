from typing import List,Dict

from core.repositories import BaseMongoRepository


class MongoRepository(BaseMongoRepository):
    def get_short_data_of_all_companies(self):
        return self._client.crawlerDataset.companies.find({}, {'COMPANY_SHORT_NAME': 1, 'INN': 1})

    def count_short_data_of_all_companies(self):
        return self._client.crawlerDataset.companies.count()

    def store_search_item(self, search_item: Dict):
        if not self._client.crawlerSearchLinks.searchItems.find_one({'URL': search_item['URL']}):
            self._client.crawlerSearchLinks.searchItems.insert_one(search_item)

    def get_random_active_company(self):
        while True:
            company = next(self._client.crawlerRegreestr.companies.aggregate([{
                '$sample': {'size': 1}
            }]))
            if not company['ACTIVE']:
                continue
            else:
                return company

    def store_dataset(self, inn, query, url, text):
        self._client.nlp.searchContext.replace_one(
            {'inn': inn, 'url': url},
            {'inn': inn, 'query': query, 'url': url, 'text': text},
            True
        )

    def get_company_by_inn(self, inn):
        return self._client.crawlerRegreestr.companies.find_one({'INN': inn})

    def trained_dataset(self):
        return self._client.nlp.searchContext.find({'innovate_cat': {'$exists': True}})
