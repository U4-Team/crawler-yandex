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
        'DOWNLOAD_DELAY': 1,
        'DEPTH_LIMIT': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 3,
        'ITEM_PIPELINES': {
            'crawler_yandex_search.pipelines.MongoPipeline': 300
        }
    })
    repo = MongoRepository()
    start_urls = []
    for index, document in enumerate(repo.get_short_data_of_all_companies()):
        queries = []
        if 'COMPANY_SHORT_NAME' in document and document['COMPANY_SHORT_NAME']:
            queries.append(document['COMPANY_SHORT_NAME'])
        if 'COMPANY_SHORT_NAME' in document and document['COMPANY_SHORT_NAME'] and 'INN' in document and document['INN']:
            queries.append(document['COMPANY_SHORT_NAME']+' ИНН '+document['INN'])
        for query in queries:
            start_urls.append(f'https://duckduckgo.com/html/?q={query}')
    process.crawl(GoogleSearchSpider, start_urls=start_urls)
    process.start()
    
    logger.info('done')
