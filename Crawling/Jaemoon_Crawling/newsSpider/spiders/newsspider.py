# execute crawling
# 1) cd .\venv\Studying\NEWS_TEAM_4\NEWS_TEAM_4\Crawling\Jaemoon_Crawling\newsSpider
# 2) scrapy crawl newsspider
import scrapy
import datetime
import requests
from bs4 import BeautifulSoup
import re
from Studying.NEWS_TEAM_4.NEWS_TEAM_4.Crawling.comment.comment_crawling import header_crawl

# agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
base_url = 'https://news.daum.net/breakingnews/'


class NewsspiderSpider(scrapy.Spider):
    name = 'newsspider'
    allowed_domains = ['news.daum.net', 'v.daum.net']
    max_page = 0

    def start_requests(self):
        main_categories = ['foreign']  # 'digital'  # 국제뉴스 : foreign , IT : digital
        sub_categories = ['asia', 'america', 'europe', 'africa', 'others', 'englishnews', 'topic', 'japan', 'china']
        sub_categories_kor = ['아시아/대양주', '미국/아메리카', '유럽', '중동/아프리카', '국제일반', '영어뉴스', '해외화제', '일본', '중국']
        page_number = 0

        for main_category in main_categories:
            for sub_category in sub_categories: # 카테고리별 수집위한 구분
                date = datetime.date.today()
                date -= datetime.timedelta(days=1)  # 크롤링 특정 일자 설정
                target_date = date - datetime.timedelta(days=2)  # 크롤링 기간 설정
                while target_date != date:

                    try:
                        page_number += 1

                        date_str = date.strftime('%Y%m%d')
                        
                        # 현재 및 최종 페이지 확인을 위한 크롤링
                        result = requests.get(
                            f'{base_url}{main_category}/{sub_category}?page={page_number}&regDate={date_str}')
                        source = BeautifulSoup(result.text, 'html.parser')
                        pages = source.find('span', class_='inner_paging').text.split()

                        print(
                            f'pages for test:{base_url}{main_category}/{sub_category}?page={page_number}&regDate={date_str}')

                        # meta 요소에 sub_category 로 한글 서브카테고리를 함께 callback 함수에 보냄
                        response = scrapy.Request(
                            f'{base_url}{main_category}/{sub_category}?page={page_number}&regDate={date_str}',
                            self.parse_url,
                            meta={'sub_category': sub_categories_kor[
                                sub_categories.index(sub_category)]})
                        yield response

                        # 최종 페이지 식별 위한 파트: 크롤링 데이타를 split() 하여 마지막 배열에  '다음', 마지막에서 두번째 배열에
                        # '현재' 란 단어가 있으며, 현재 페이지 숫자와 마지막 배열의 숫자가 동일할 경우 최종 페이지 확정
                        # 페이지 초기화(1페이지) 및 날짜를 하루 전날로 이동후 다시 데이타 크롤링
                        pages_size = len(pages)
                        if pages[pages_size - 1] != '다음':
                            number = re.sub(r'[^0-9]', '', pages[pages_size - 1])
                            # print("for test : ", '현재' in pages[pages_size - 2].strip(), int(page_number) == int(number),
                            #       page_number, number, pages[pages_size - 2], pages[pages_size - 1])
                            if '현재' in pages[pages_size - 2].strip() and int(page_number) >= int(number):
                                date -= datetime.timedelta(days=1)
                                page_number = 1


                    except Exception as e:
                        print("start_requests Exception : ", e)
                        date -= datetime.timedelta(days=1)
                        page_number = 1

    def parse_url(self, response):
        try:
            # 호출된 페이지 기사 링크 리스트로 한번 callback
            for news_data in response.css('.list_news2.list_allnews li a::attr(href)').getall():
                url = news_data
                yield scrapy.Request(url=url, callback=self.parse_news, meta=response.meta)
        except Exception as e:
            print(f'exception in parse_url : {e}')

    # 날짜 클렌징 함수
    def date_cleaning(self, data):
        data = data.split('+')[0]
        data = data.replace('T', ' ')
        return data

    def parse_news(self, response):
        # 코멘트 및 스티커 데이타 크롤링 파트
        action = header_crawl()
        post_id, article_id, url = action.header_setting(response.url)
        action_dict = action.action_crawl(article_id)
        # action_dict.pop('article_id')
        Comment_info = action.comment_crawl(post_id, response.url)
        writedat_list = list(Comment_info.WritedAt.apply(self.date_cleaning))
        print("parse_news here! ", writedat_list,  post_id, article_id, url, action_dict, Comment_info)

        # 최종 크롤링 데이타를 csv 로 저장할 구조
        scrawl_info = {
            # 'ID': 'id',
            'DomainID': '0',  # daum : 0 / naver : 1
            'MainCategory': '국제',
            'SubCategory': response.meta['sub_category'],
            'WritedAt': response.css('.num_date::text').get(),
            'Title': response.css('.head_view h3::text').get(),
            'Content': "".join(response.css('.article_view p::text').getall()),
            'URL': response.url,
            'PhotoURL': response.css('.link_figure img::attr(src)').getall(),
            'Writer': response.css('.txt_info::text').get(),
            'Press': response.css('#kakaoServiceLogo::text').get(),
            'Stickers': action_dict,
            'UserID': list(Comment_info.UserID),
            'Comment_content': list(Comment_info.Content),
            'Comment_WritedAt': writedat_list,
            'UserName': list(Comment_info.UserName)
        }
        # print("scrawl_info here : ", scrawl_info)
        yield scrawl_info
