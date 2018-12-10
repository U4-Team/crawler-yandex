import os

ITEM_PIPELINES = {
    'crawler_yandex_search.pipelines.MongoStorePipeline': 300
}
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
COOKIES_ENABLED = False