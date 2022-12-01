# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
# from scrapy.utils.project import get_project_settings
# settings = get_project_settings()

class NewsspiderPipeline:

    # execute one time at first
    def __init__(self):
        self.file = open('NewsCrawlerFile.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf8')
        self.exporter.start_exporting()

    # processing the crawling's returns
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    # call when spider done
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
