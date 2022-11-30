# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DaumItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    Content=scrapy.Field()
    URL=scrapy.Field()
    Writer=scrapy.Field()
    Press=scrapy.Field()
    PhotoURL=scrapy.Field()
    SubCategory=scrapy.Field()
    MainCategory=scrapy.Field()
    WritedAt=scrapy.Field()
    
