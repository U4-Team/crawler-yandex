import scrapy
from furl import furl
import phonenumbers
from urllib import parse



class GoogleSearchSpider(scrapy.Spider):
    name = "google_search"

    def parse(self, response: scrapy.http.HtmlResponse):
        self.logger.info('Crawl url: %s', response.url)
        for search_item in response.css('div#links div.result.results_links.results_links_deep.web-result'):
            title = ''.join(search_item.css('h2.result__title > a.result__a ::text').extract())
            snippet = ''.join(search_item.css('a.result__snippet ::text').extract())
            url = ''.join(search_item.css('a.result__url::attr(href)').extract())
            yield {
                'title': title,
                'snippet': snippet,
                'url': url
            }
