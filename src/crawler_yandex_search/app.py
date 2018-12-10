import re
from core.mixins import LoggerMixin
from selenium import webdriver
from furl import furl
import spacy
import requests
import json
from collections import defaultdict

from crawler_yandex_search.repositories import MongoRepository


class DuckduckApplication(LoggerMixin):
    stop_domains = [
        # 'rusprofile.ru',
        # 'www.rusprofile.ru',
        # 'www.k-agent.ru',
        # 'egrulinfo.com',
        # 'moskva.regreestr.com', # subdomain
        # 'yandex.ru',
        # 'www.yandex.ru',
        # 'www.list-org.com',
        # 'info.1cont.ru',
        # 'allinfo24.ru',
        # 'synapsenet.ru',
        # 'zachestnyibiznes.ru',
        # 'commfy.ru',
        # 'www.prima-inform.ru',
        # 'sbis.ru',
        # 'russia-opt.com',  # stupid site (block with subdomains!!)
        # 'moscow.flamp.ru',
        # 'www.slideshare.net',
        # 'slideshare.net',
        # 'www.spark-interfax.ru',
        # 'spark-interfax.ru',
        # 'egrulbox.ru',
        # '7fa.ru',
        # 'pro.fira.ru',
        # 'impulsee.ru',
        # 'www.egripegrul.ru',
        # 'alavi.ru',
        # 'moscow.rusbport.ru',
        # 'ruscifra.ru',
        # '2gis.ru',
        # 'egrinf.com',
        # 'notecom.biz',
        # 'egrul-egrip.ru',
        # 'unfall.ru',
        # 'findercom.ru',
        # 'госреестр.рф',
        # 'neotorg.com',
        # 'whokpo.com',
        # 'novosibirsk7m.ru',
        # 'business-rating.company',
        # 'www.job-mo.ru',
        # 'www.find-org.com',
        # 'professionali.ru',
        # 'eqbiz.ru',
        # 'yecom.ru',
        # 'pro-ooo.ru',
        # 'www.b2b-project.ru',
        # 'vologda7m.ru',
        # 'focus.kontur.ru',
        # 'moscow-obl7m.ru',
        # 'dolgi.ru',
        # 'tver7m.ru',
        # 'addresscom.ru',
        # 'vladimir.tizu.ru',  # subdomain
        # 'tizu.ru',
        # 'comreport.ru',
        # 'moskva-region.lexot.ru', # subdomain,
        # 'emocom.ru',
        # 'znaybiznes.ru',
        # '66-екатеринбург.рф',
        # 'egrul.com',
        # 'regreestr.com',
        # 'krasnodar7m.ru', # block all 7m? !!!!! yes!!!
        # 'runet-id.com',
        # 'www.world-factory.ru',
        # 'b2bpoisk.ru',
        # 'pravda-sotrudnikov.ru',
        # 'contragents.ru',
        # 'www.b2bsky.ru',
        # 'querycom.ru',
        # 'actez.ru',
        # 'yelcom.ru',
        # 'ekaterinburgreg.rebic.ru', # subdomain,
        # 'lexot.ru',
        # 'tula.yellmarket.ru', #subdomain,
        # 'www.kartoteka.ru',
        # 'рубиз.рф',
        # 'e-ecolog.ru',
        # 'ulanude.yellmarket.ru', # subdomain
        # 'basis.myseldon.com',
        # 'moscow-yel.ru',
        # 'reviewscompanies.com',
        # 'zhaloba-online.ru',
        # 'foundus.biz',
        # 'moskva.okato.net', # subdomain
        # 'moscow7m.ru',
        # 'xeff.ru',
        # 'ogrn.ru',
        # 'yoshkar-ola7m.ru',
        # 'pravda-obman.com',
        # 'www.bankovskie.ru',
        # '77.ogrninfo.ru', # subdomain,
        # 'msk.tizu.ru', # subdomain
        # 'web-cache.tpu.ru',
        # 'secorp.ru',
        # 'exacom.ru',
        # 'menfo.biz',
        # 'moskva-reg.lexot.ru', # subdomain,
        # 'bizprofiles.ru',
        # 'moscow.zely.ru', # subdomain
        # 'enspe.com',
        # 'okatocom.ru',
        # 'caddress.ru',
        # 'citynfo.ru',
        # 'dazzy.ru',
        # 'moscow.yellmarket.ru',
        # 'tyumen7m.ru',
        # 'огрн.онлайн',
        # 'sankt-peterburg.bizly.ru',
        # 'kontragent.skrin.ru',
        # 'ogrn.net',
        # 'iskalko.ru',
        # 'petersburg-yel.ru',
        # 'iskalko.ru',
        # 'inndex.ru',
        # 'reputation.ru',
        # 'angarsk.cataloxy.ru',
        # 'barnaul7m.ru',
        # 'nizhny-novgorod7m.ru',
        # 'spb.tizu.ru',
        # 'reabiz.ru',
        # 'globalstat.ru',
        # 'sotrydnik.com',
        # 'glees.ru',
        # 'kazanobl.ajeo.ru',
        # 'rosbankmc.ru',
        # 'www.yell.ru',
        # 'sudbiz.ru',
        # 'ogrn.org',
        # 'issuu.com',
        # 'sudact.ru',
        # 'www.novosibirskspravka.ru',
        # 'logistpro.su',
        # 'gloriya.belorussia.su',
        # 'birank.com',
        # 'volgograd7m.ru',
        # 'makhachkala7m.ru',
        # 'retwork.com',
        # 'firmy-ufa.ru',
        # 'tvoyproduct.ru',
        # 'orabote.top',
        # 'vladivostok.tizu.ru',
        # 'employmentcenter.ru',
        # 'moskva.rosfirm.ru'
    ]
    driver = None
    nlp = spacy.load('/Users/zerion/Workspace/Tmp/spacy-ru/ru2')
    mongo_repo = MongoRepository()

    stats = defaultdict(lambda: None)
    data = defaultdict(lambda: None)

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        options.add_argument('lang=ru')

        self.driver = webdriver.Chrome(chrome_options=options)

    def search(self, query, pages=8):
        # ОКБ «АТМ грузовые дроны»
        stats = defaultdict(lambda: None)
        data = defaultdict(lambda: None)
        self._open_search_page(query)
        self._load_all_pages(pages)
        links = self._get_archived_links(self._get_links())
        self._dive(query, links)
        self._result()

    # def _tarin_cat(self):
    #     self.logger.info('Do Train')
    #     trained = self.mongo_repo.trained_dataset()
    #     train_data = []
    #     for item in trained:
    #         sent = u' '.join(item['text'].split('\n')).strip()
    #         if not sent:
    #             continue
    #         data = (
    #             sent, {'cats': {'INNOVATION': item['innovate_cat']}}
    #         )
    #         train_data.append(data)

    #     textcat = self.nlp.create_pipe('textcat')
    #     self.nlp.add_pipe(textcat, last=True)
    #     textcat.add_label('INNOVATION')
    #     optimizer = self.nlp.begin_training()
    #     for itn in range(100):
    #         for doc, gold in train_data:
    #             self.nlp.update([doc], [gold], sgd=optimizer)

    #     self.logger.info('Trained')

    # def _get_query(self, inn):
    #     company = self.mongo_repo.get_company_by_inn(inn)
    #     if not company:
    #         return f'ИНН+{inn}'
        
    #     return f'"{company["COMPANY_SHORT_NAME"]}"'

    def _open_search_page(self, query):
        self.logger.info('Open search page: %s', query)
        self.driver.get("https://duckduckgo.com/")
        self.driver.find_element_by_id('search_form_input_homepage').send_keys(query)
        self.driver.find_element_by_id("search_button_homepage").click()
        self.driver.implicitly_wait(2)
        self.logger.info('Done.')
    
    def _load_all_pages(self, pages):
        self.logger.info('Load all required pages: %s', pages)
        for page in range(pages):
            self.logger.info('Load page: %s...', page)
            next_button = self.driver.find_elements_by_xpath("//a[contains(@class, 'result--more__btn')]")
            if not next_button:
                self.logger.info('End of pages reached')
                return

            next_button[0].click()
            self.driver.implicitly_wait(2)

    def _get_links(self):
        links = []
        for a in self.driver.find_elements_by_xpath("//a[contains(@class, 'result__a')]"):
            href = furl(a.get_attribute('href'))
            if href.host in self.stop_domains:
                continue

            if href.url.endswith('.pdf'):
                continue

            if href.host[-3:] in ['.by', '.kz', '.ua', '.uz', '.az']:
                continue
            
            links.append(str(href.url))
        
        return links[:15]

    def _get_archived_links(self, links):
        self.logger.info('Getting web archive links')
        archived = []
        for link in links:
            pattern = f'https://archive.org/wayback/available?url={link}'
            resp = requests.get(pattern).json()
            if ('archived_snapshots' not in resp) or ('closest' not in resp['archived_snapshots']):
                continue

            archived.append(resp['archived_snapshots']['closest']['url'])
        
        self.logger.info('Done')
        return archived

    def _dive(self, query, links):
        for link in links:
            self.logger.info('Perform: %s', link)
            self.driver.get(link)
            content = self.driver.find_element_by_tag_name('body').text
            print(100*'-')
            print(content)
            self._parse_sites(link, content)
            print(100*'-')
            self._result()
            # # self.mongo_repo.store_dataset(inn, query, link, content)
            # print(doc.cats)
            self.driver.execute_script("window.history.go(-1)")


    
    def _parse_sites(self, url, content):
        reg1 = r'''((http|https)://)?[a-z0-9.-]+[a-z0-9]{1}\.[a-z]{2,5}'''
        result = re.search(reg1, content, flags=re.IGNORECASE)
        if not result:
            return

        if not self.data['sites']:
            self.data['sites'] = []
        self.data['sites'].append(result.group())
        
        if not self.stats[url]:
            self.stats[url] = {}
        self.stats[url]['sites'] = [result.group()]

    def _result(self):
        self.logger.info('Result:')
        self.logger.info('Data: %s', self.data)
        self.logger.info('Stats: %s', self.stats)
