import scrapy
import json

from douyu_project.items import DouyuProjectItem

class DouyuSpider(scrapy.Spider):
	name = "douyu"
	offset = 0
	url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
	start_urls = [url + str(offset)]

	def parse(self, response):
		data = json.loads(response.text)["data"]

		for each in data:
			item = DouyuProjectItem()

			item['name'] = each['nickname']
			item['imagesUrls'] = each['vertical_src']

			yield item

		self.offset += 20

		yield scrapy.Request(self.url + str(offset), callback=self.parse)