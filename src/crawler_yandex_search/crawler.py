import scrapy
from furl import furl
import phonenumbers
from urllib import parse
from scrapy.spiders import Rule, CrawlSpider, Spider
from scrapy.linkextractors import LinkExtractor
import pandas
import numpy
from bs4 import BeautifulSoup

# class TMCrawler(CrawlSpider):
#     name = 'technomoscow_crawler'
#     start_urls = [
#         'https://technomoscow.ru/residents/nano',
#     ]

h = html2text.HTML2Text()

class SkolkovoCrawler(Spider):
    name = "skolkovo_crawler"
    start_urls = []
    _soup = BeautifulSoup(html)


    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'COOKIES_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'scrapy_proxies.RandomProxy': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
        'PROXY_MODE': 1,
        'PROXY_LIST': './proxy.list',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept-Language': 'ru-RU'
        }
    }

    def start_requests(self):
        dataframe = pandas.read_excel('./skolkovo.xlsx')
        urls = dataframe['Ссылка на  сайт Сколково'].tolist()
        urls = list(
            filter(
                lambda u: u.startswith('http://sk.ru/net/'), 
                (set(urls) - set([numpy.nan]))
            )
        )
        urls = ['http://sk.ru/net/1121569/']
        for url in urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        data = {}
        company_name = response.css('div.sk-pd-projectcard div.well > div.row-fluid > div.span9 > div.row-fluid > h3::text').extract_first()
        if not company_name:
            self.logger.warning('Unable to parse company name from: %s', response.url)
        
        data['COMPANY_SHORT_NAME'] = company_name.strip()

        content = response.css('div.sk-pd-projectcard > div.content-fragment-content div.sk-pd-overview-block').extract()
        print(self._soup(content).get_text())
        yield data

        # company_links = response.css('div.sk-pd-projectcard a::attr(href)').extract()
        # company_links = [s for s in company_links if not s.startswith('https://sk.ru')]
        # data['COMPANY_LINKS'] = list(set(company_links))
        # print(data)

        # descr = response.css('div.sk-pd-overview-block::text').extract()
        # print(descr)


# class _WebWideSearchCrawler(CrawlSpider):
#     name = "web_wide_search_crawler"
#     start_urls = [
#         'http://www.tpstrogino.ru/residents/',
#         'http://www.technopark-slava.ru/residents/residents_info/',
#         'http://www.sciencepark.ru/ru/companies',
#         'https://tptisnum.wordpress.com/%D1%80%D0%B5%D0%B7%D0%B8%D0%B4%D0%B5%D0%BD%D1%82%D1%8B/'
#         'http://sipower.ru/tekhnopark.html',
#         'https://www.polyus.info/technopark/residents/'
#         'https://duckduckgo.com/html/?q=%D0%9E%D0%9E%D0%9E+site%3Ahttp%3A%2F%2Fsk.ru',
#         'https://duckduckgo.com/html/?q=%D0%90%D0%9E+site%3Ahttp%3A%2F%2Fsk.ru'
#     ]

#     def parse(self, response: scrapy.http.HtmlResponse):
#         requested_url = response.request.url
#         _, inn = requested_url.split('#')
#         total = len(self.start_urls)
#         index = self.start_urls.index(requested_url)
#         progress = round(index/total * 100, 5)
#         print(index, progress, inn, response.url)
#         if progress*100 == int(progress*100):
#             self.logger.info('Progress: %s (%s)', progress, response.url)
        
#         for search_item in response.css('div#links div.result.results_links.results_links_deep.web-result'):
#             title = ''.join(search_item.css('h2.result__title > a.result__a ::text').extract())
#             snippet = ''.join(search_item.css('a.result__snippet ::text').extract())
#             url = ''.join(search_item.css('a.result__url::attr(href)').extract())
#             yield {
#                 'TITLE': title,
#                 'SNIPPET': snippet,
#                 'URL': url,
#                 'INN': inn
#             }
