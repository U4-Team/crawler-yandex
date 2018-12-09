import logging
from urllib import parse

import click
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawler_yandex_search.crawler import GoogleSearchSpider
from crawler_yandex_search.repositories import MongoRepository

logger = logging.getLogger(__name__)

@click.group()
def cli() -> None:  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(process)-5s] %(name)-24s %(levelname)s %(message)s',
        datefmt='%d.%m.%Y[%H:%M:%S]',
    )
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    logging.getLogger('scrapy').propagate = False

@cli.command()
@click.option('--search-url', type=str)
def run(search_url: str) -> None:
    logger.info('=== START ===')
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'DOWNLOAD_DELAY': 0.1,
        'DEPTH_LIMIT': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ITEM_PIPELINES': {
            'crawler_yandex_search.pipelines.MongoPipeline': 300
        },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        #     'scrapy_rotated_proxy.downloadmiddlewares.proxy.RotatedProxyMiddleware': 750,
        # },
        # 'ROTATED_PROXY_ENABLED': False,
        # 'HTTP_PROXIES': [
        #     'http://68.15.42.194:31743',
        #     'http://91.222.167.213:38057',
        #     'http://165.90.90.10:46006',
        #     'http://122.50.6.186:80',
        #     'http://96.9.79.173:59667',
        #     'http://138.68.136.245:3128',
        #     'http://185.44.231.70:60550',
        #     'http://78.47.157.159:80',
        #     'http://41.90.103.102:8888',
        #     'http://212.72.150.51:8081',
        #     'http://189.7.97.54:8080',
        #     'http://94.240.46.195:23500',
        #     'http://207.180.240.103:3128',
        #     'http://183.182.103.98:8080',
        #     'http://113.11.131.123:59769'
        # ]
     })
    repo = MongoRepository()
    start_urls = []
    for index, document in enumerate(repo.get_short_data_of_all_companies()):
        inn = document["INN"]
        queries = [f'ИНН {inn}']
        if 'COMPANY_SHORT_NAME' in document and document['COMPANY_SHORT_NAME']:
            queries.append(f'ИНН {inn} {document["COMPANY_SHORT_NAME"]}')
        for query in queries:
            qs = parse.urlencode({'q': query})
            start_urls.append(f'https://duckduckgo.com/html/?{qs}#{inn}')
    
    start_urls = list(sorted(start_urls))
    process.crawl(GoogleSearchSpider, start_urls=start_urls[5100:])
    process.start()
    
    logger.info('done')
