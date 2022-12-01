# execute crawling
# 1) cd .\venv\Studying\NEWS_TEAM_4\NEWS_TEAM_4\Crawling\Jaemoon_Crawling\newsSpider
# 2) scrapy crawl newsspider
import scrapy
import datetime
import requests
from bs4 import BeautifulSoup
import re

# agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
base_url = 'https://news.daum.net/breakingnews/'


class NewsspiderSpider(scrapy.Spider):
    name = 'newsspider'
    allowed_domains = ['news.daum.net', 'v.daum.net']
    max_page = 0

    def start_requests(self):
        date = datetime.date.today()
        target_date = date - datetime.timedelta(days=1)  # 크롤링 기간
        main_categories = ['foreign']  # 'digital'  # 국제뉴스 : foreign , IT : digital
        sub_categories = ['america', 'asia', 'europe', 'africa', 'others', 'englishnews', 'topic', 'japan', 'china']
        page_number = 1

        for main_category in main_categories:
            while target_date != date:  # 현재로부터 얼마나 과거의 날들을 크롤링할지
                for sub_category in sub_categories:
                    try:
                        date_str = date.strftime('%Y%m%d')

                        result = requests.get(
                            f'{base_url}{main_category}/{sub_category}?page={page_number}&regDate={date_str}')
                        source = BeautifulSoup(result.text, 'html.parser')
                        pages = source.find('span', class_='inner_paging').text.split()

                        response = scrapy.Request(f'{base_url}{main_category}?page={page_number}&regDate={date_str}',
                                                  self.parse_url, meta={'sub_category': sub_category})
                        yield response

                        pages_size = len(pages)
                        if pages[pages_size - 1] != '다음':
                            number = re.sub(r'[^0-9]', '', pages[pages_size - 1])
                            print("for test : ", '현재' in pages[pages_size - 2].strip(), int(page_number) == int(number),
                                  page_number, number, pages[pages_size - 2], pages[pages_size - 1])
                            if '현재' in pages[pages_size - 2].strip() and int(
                                    page_number) >= number and sub_categories.index(sub_category) == 8:
                                date -= datetime.timedelta(days=1)
                                page_number = 1
                                # print('날짜 변경!')
                                pass

                        page_number += 1

                    except Exception as e:
                        print("Exception : ", e)
                        date -= datetime.timedelta(days=1)
                        page_number = 1

    def parse_url(self, response):
        try:
            for news_data in response.css('.list_news2.list_allnews li a::attr(href)').getall():
                url = news_data
                yield scrapy.Request(url=url, callback=self.parse_news, meta=response.meta)
        except Exception as e:
            print(f'exception in parse_url : {e}')

    def parse_news(self, response):
        title = response.css('.head_view h3::text').get()
        contents = "".join(response.css('.article_view p::text').getall())

        scrawl_info = {
            # 'ID': 'id',
            'DomainID': '0',  # daum : 0 / naver : 1
            'MainCategory': 'main_categories',
            'SubCategory': response.meta['sub_category'],
            'WritedAt': 'writed_at',
            'Title': title,
            'Content': contents,
            'URL': response.url,
            'PhotoURL': 'photo_url',
            'Writer': 'writer',
            'Press': 'press',
            'Stickers': 'stickers'
        }
        # print("scrawl_info here : ", scrawl_info)
        yield scrawl_info
