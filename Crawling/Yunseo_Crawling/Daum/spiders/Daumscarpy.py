import scrapy
from Daum.items import DaumItem
import re
import pandas as pd
import datetime 
import calendar
from Daum.spiders.Extractemo import header_crawl
from Daum.items import Comment_Item


class Daumspider(scrapy.Spider):
    name = "Daum"
    user_agents_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
                ]
    subTitle_name=''
    Title='IT'

    comment_df_list = []

    def start_requests(self):
        url='https://news.daum.net/breakingnews/digital/'
        yield scrapy.Request(url=url, callback=self.parse_sub)

    def parse_sub(self,response):
        urls=response.css('.tab_sub2 li a::attr(href)').getall()
        for url in urls[1:]:
            del_url=re.sub('/breakingnews/digital/','',url)
            
            self.subTitle_name=del_url
            
            conve=response.url+f'{del_url}'
            yield scrapy.Request(url=conve, callback=self.parse_date,meta={'answer':del_url})


    def parse_date(self,response):

        date_total=datetime.datetime(2022,11,1)
        future_date=datetime.datetime(2022,12,1)
        
        
        while True:
            howmany_days=calendar.monthrange(date_total.year, date_total.month)[1]
            for day_count in range(date_total.day,howmany_days+1):
                date_year=date_total.year
                date_month=date_total.month
                date_total=datetime.datetime(date_year,date_month,day_count)
                if date_total==future_date:
                    return
                date_day=date_total.day
                date_put_y=date_total.strftime('%y')
                date_put_m=date_total.strftime('%m')
                date_put_d=date_total.strftime('%d')
                url = response.url+f'?regDate={date_year}{date_put_m}{date_put_d}'
                
                yield scrapy.Request(url=url, callback=self.parse_page,meta=response.meta)
                

            if date_month==12:
                date_total=datetime.datetime(date_year+1,1,1)
            else:
                date_total=datetime.datetime(date_year,date_month+1,1)


    def parse_page(self,response):
        count_urls=response.css('.inner_paging a') 

        for count_url in range(len(count_urls)+1):
            if count_url==0:
                yield scrapy.Request(url=response.url, callback=self.parse_pre,dont_filter = True,meta=response.meta)
            else:
                url='https://news.daum.net'+count_urls[count_url-1].css('::attr(href)').get()
                Url_check=count_urls[count_url-1].css('::attr(class)').get()
              
                if Url_check=='btn_page btn_next':
                    yield scrapy.Request(url=url, callback=self.parse_page,meta=response.meta)
                    
                else:
                    yield scrapy.Request(url=url, callback=self.parse_pre,meta=response.meta)
                  
                


    def parse_pre(self,response):
        urls=response.css('.list_news2.list_allnews a::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,meta=response.meta)

    def date_cleaning(self,data):
        data=data.split('+')[0]
        data=data.replace('T',' ')
        return data

    def data_content_clean(self,data):
        return data.replace('\n','').strip()

    def parse(self, response):
        action = header_crawl()
        check='댓글'
        post_id, article_id, url = action.header_setting(response.url)

        # 본문만
        if check=='본문':
            action_dict = action.action_crawl(article_id)
            action_dict.pop('article_id')
    

            sub_dic={'internet':'인터넷','science':'과학','game':'게임','it':'휴대폰통신','device':'IT기기','mobile':'통신모바일','software':'소프트웨어','others':'Tech일반'}
            item=DaumItem()
        
            item['Title']=response.css('.box_view .tit_view::text').get()
            item['Content']="".join(response.css('.article_view p::text').getall())
            item['Writer']=response.css('.txt_info::text').get()
            item['Press']=response.css('#kakaoServiceLogo::text').get()
            item['PhotoURL']=response.css('.link_figure img::attr(src)').getall()
            item['SubCategory']=sub_dic[response.meta['answer']]
            item['MainCategory']=self.Title
            item['WritedAt']=response.css('.num_date::text').get()
            item['Stickers']=action_dict
            yield item


        else:
            #  댓글만 수정
            item2=Comment_Item()

            Comment_info=action.comment_crawl(post_id,response.url)
            if Comment_info:
                for con in Comment_info:
                    item2['UserID']=con['UserID']
                    item2['Content']=self.data_content_clean(con['Content'])
                    item2['URL']=response.url
                    item2['UserName']=con['UserName']
                    item2['WritedAt']=self.date_cleaning(con['WritedAt'])
                    yield item2


        



    