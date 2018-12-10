import logging
from urllib import parse

import click
from crawler_yandex_search.app import DuckduckApplication


logger = logging.getLogger(__name__)

@click.group()
def cli() -> None:  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(process)-5s] %(name)-24s %(levelname)s %(message)s',
        datefmt='%d.%m.%Y[%H:%M:%S]',
    )
    logging.getLogger('scrapy').setLevel(logging.DEBUG)
    # logging.getLogger('scrapy').propagate = False


@cli.command()
@click.option('--query', type=str)
def run(query: str) -> None:
    logger.info('=== START ===')
    try:
        app = DuckduckApplication()
        app.search(query)
    finally:
        app.driver.quit()

    logger.info('done')
