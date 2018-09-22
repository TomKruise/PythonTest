# -*- coding: utf-8 -*-
import scrapy

from Sun0769.items import Sun0769Item


class SunSpider(scrapy.Spider):
	name = "sun0769"

	url = "http://wz.sun0769.com/index.php/question/questionType?type=4&page="

	offset = 0

	start_urls = [url + str(offset)]

	def parse(self, response):
		links = response.xpath('//div[@class="greyframe"]//a[@class="news14"]/@href').extract()

		for link in links:
			# print(link)
			yield scrapy.Request(link, callback=self.parse_item)

		if offset < 900:
			offset += 30

			yield scrapy.Request(url + str(offset), callback=self.parse)

	def parse_item(self, response):
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