from urllib import request
from urllib.request import urlopen
from lxml import etree

import time
import random
import json


class qiushi(object):
	def __init__(self):
		self.switch = True
		self.page = 1
		self.url = "https://www.qiushibaike.com"
		self.headers = {
			"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
			"Accept-Language" : "zh-CN,zh;q=0.8",
		}
		self.counter = 0

	def pause(self):
		second = random.randint(1, 3)

		time.sleep(second)

	def write2json(self, list):
		print("Writing")

		print("\n")

		data = json.dumps(list, ensure_ascii=False)

		with open("qiushibaike.json", "w") as f:
			f.write(data)

		print("Writing completed")
		print("\n")


	def parseHtml(self, text):
		print("Parsing text")

		print("\n")

		text = etree.HTML(text)

		list = text.xpath('//div[contains(@id, "qiushi_tag")]')

		# print(type(list))

		# print(list)
		data_list = []

		for each in list:
			data = {}

			username = each.xpath('.//h2/text()')[0].strip()

			content = each.xpath('.//div[@class="content"]/span/text()')[0].strip().replace('&#39;', '')

			vote_num = each.xpath('.//span/i[@class="number"]/text()')[0]

			comment_num = each.xpath('.//a/i[@class="number"]/text()')[0]

			source_link = self.url + each.xpath('./a/@href')[0]

			photo_link = "https:" + each.xpath('.//img/@src')[0]

			data['username'] = username

			data['content'] = content

			data['vote_num'] = vote_num

			data['comment_num'] = comment_num

			data['source_link'] = source_link

			data['photo_link'] = photo_link

			data_list.append(data)

			self.counter += 1

			# print(photo_link)

		print("Parsing completed")

		print("\n")

		self.write2json(data_list)

	def loadpage(self, page):
		# https://www.qiushibaike.com/8hr/page/1/
		print("Loading page")

		print("\n")

		self.pause()

		url = self.url + "/8hr/page/" + str(page) + "/"

		req = request.Request(url, headers=self.headers)

		html = urlopen(req).read().decode("utf-8")

		print("Loading completed")

		print("\n")

		# with open("qiushi.html", "w") as f :
		# 	f.write(html)
		self.parseHtml(html)


	def go(self):
		input("Push enter to start")
		
		while self.switch:
			try:
				self.loadpage(self.page)
			except request.URLError as e:
				print(e.message)
				continue

			self.page += 1

			haha = input("Push enter to continue, or type 'quit' to exit")

			if haha == 'quit':
				self.switch = False

				print("Thanks for using, bye(Collect jokes %d)"%self.counter)

				print("\n")

				break




if __name__ == "__main__":
	spider = qiushi()
	spider.go()