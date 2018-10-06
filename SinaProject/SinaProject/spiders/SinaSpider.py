from SinaProject.items import SinaprojectItem

import scrapy
import os


class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://news.sina.com.cn/guide/"
    ]

    def parse(self, response):
        items = []

        parentDirs = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()
        parentUrls = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()

        subDirs = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()
        subUrls = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()

        for i in range(0, len(parentDirs)):
            dir = "./Data/" + parentDirs[i]

            if(not os.path.exists(dir)):
                os.makedirs(dir)

            for j in range(0, len(subUrls)):
                item = SinaprojectItem()

                item["parentDir"] = parentDirs[i]
                item["parentUrl"] = parentUrls[i]

                if_belong = subUrls[j].startswith(item["parentUrl"])

                if(if_belong):
                    subDir = dir + "/" + subDirs[j]

                    if(not os.path.exists(subDir)):
                        os.makedirs(subDir)

                    item["subUrl"] = subUrls[j]
                    item["subDir"] = subDirs[j]

                    item["subDirPath"] = subDir

                    items.append(item)

        for item in items:
            yield scrapy.Request(url=item["subUrl"], meta={'meta_1':item}, callback=self.sub_parse)

    def sub_parse(self, response):
        meta_1 = response.meta["meta_1"]

        subUrls = response.xpath('//a/@href').extract()

        items = []

        for i in range(0, len(subUrls)):
            if_belong = subUrls[i].endswith(".shtml") and subUrls[i].startswith(meta_1['parentUrl'])

            if(if_belong):
                item = SinaprojectItem()

                item["parentDir"] = meta_1['parentDir']
                item["parentUrl"] = meta_1['parentUrl']
                item["subUrl"] = meta_1['subUrl']
                item["subDir"] = meta_1['subDir']
                item["subDirPath"] = meta_1['subDirPath']
                item["sonUrl"] = subUrls[i]

                items.append(item)

        for item in items:
            yield scrapy.Request(url=item['sonUrl'], meta={"meta_2":item}, callback=self.article_parse)

    def article_parse(self, response):
        item = response.meta["meta_2"]

        content = ""

        title = response.xpath('//div[@class="main_content"]/h1/text()').extract()

        content_list = response.xpath('//div[@class="content"]/p/text()').extract()

        for text in content_list:
            content += text

        item["articalTitle"] = title
        item["articalContent"] = content

        yield item