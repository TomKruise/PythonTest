# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parentDir = scrapy.Field()
    parentUrl = scrapy.Field()

    subDir = scrapy.Field()
    subUrl = scrapy.Field()

    subDirPath = scrapy.Field()

    sonUrl = scrapy.Field()

    articalTitle = scrapy.Field()
    articalContent = scrapy.Field()
