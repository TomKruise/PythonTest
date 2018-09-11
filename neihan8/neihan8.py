# coding:utf-8
from urllib import request
from urllib import parse
from urllib.request import urlopen

import re
import time
import random


class neihanSpider(object):
	def loadPage(self, page):
		second = random.randint(1, 3)

		time.sleep(second)

		url = "https://www.neihan8.com/article/list_5_" + str(page) + ".html"

		user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"

		headers = {"User-Agent":user_agent}

		req = request.Request(url, headers=headers)

		response = urlopen(req)

		html = response.read()

		html = html.decode('gbk')

		# print(html)

		"""<div class="f18 mb20">
							<p>
	　　老师:“小明，你的梦想是什么？”小明沉思片刻道:“有房有铺，自己当老板，<br>
	妻子貌美如花，还有当官的兄弟” 老师:北宋有个人和你一样，他姓武！</p>

							
						</div>"""

		pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)

		list = pattern.findall(str(html))

		return list

	def printPage(self, list, page):
		print("Page %s was done!"%page)

		for item in list:
			print("="*130)
			item = item.strip().replace('<br />', '').replace("&ldquo;", "").replace('&rdquo;', '').replace('<p>', '').replace('</p>', '').replace('&hellip;', '').replace('&lsquo;', '').replace('&rsquo;', '').replace('&nbsp;', '').replace('&quot;', '')
			print(item)
			self.writePage(item)

	def writePage(self, text):
		file = open("./neihan8.txt", "a")
		file.write(text)
		file.write("\n")
		file.write("\n")
		file.write("\n")
		file.close()

	def doWork(self):
		self.switch = True
		self.page = 1
		while self.switch:
			try:
				list = self.loadPage(self.page)
			except request.URLError as e:
				print(e.message)
				continue

			self.printPage(list, self.page)
			self.page += 1

			print("Push enter to continue, or type quit to exit!")
			haha = input() # Receive the input string

			if haha == 'quit':
				self.switch = False
				break


if __name__ == "__main__":
	neihan = neihanSpider()
	neihan.doWork()
