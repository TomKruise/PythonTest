# -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Sun0769.items import Sun0769Item


class SunCrawlSpider(CrawlSpider):
	name = 'suncrawl'
	allowed_domains = ['wz.sun0769.com']
	start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

	pagelink = LinkExtractor(allow=('type=4'))

	formlink = LinkExtractor(allow=('/question/\d+/\d+.shtml'))

	rules = [
		Rule(pagelink, process_links="parselink", follow=True),
		Rule(formlink, callback='parseform'),
	]

	def parselink(self, links):
		for link in links:
			link.url = link.url.replace("?", "&").replace("Type&", "Type?")

		return links

	def parseform(self, response):
		item = Sun0769Item()

		item['title'] = response.xpath('//div[@class="pagecenter p3"]//strong[@class="tgray14"]/text()').extract_first()

		# print(item['title'])

		item['number'] = item['title'].split('  ')[-1].split(':')[-1]

		content = response.xpath('//div[@class="c1 text14_2"]/div[@class="contentext"]/text()').extract_first().strip()

		if len(content) == 0:
			content = response.xpath('//div[@class="content text14_2"]/div[@class="c1 text14_2"]/text()').extract_first().strip()

		item['content'] = content

		item['url'] = response.url

		yield item