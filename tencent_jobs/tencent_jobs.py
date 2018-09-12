from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen

import time
import random
import json


class tencent(object):
	def __init__(self):
		self.switch = True
		self.page = 1
		self.url = "https://hr.tencent.com/"
		self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}
		self.counter = 1

	def pause(self):
		second = random.randint(1, 3)

		time.sleep(second)

	def write2json(self, list):
		print("Writing to file")

		print("\n")

		data = json.dumps(list, ensure_ascii=False)

		with open("tencent_jobs.json", "a") as f:
			f.write(data)

		print("Write complished")

		print("\n")

	def parseHtml(self, html):
		soup = BeautifulSoup(html, "lxml")

		list = soup.select("tr[class='even']")

		list = list + soup.select("tr[class='odd']")

		job_list = []

		for each in list:
			print("Process on job %d"%self.counter)

			print("\n")

			job = {}

			positionName = each.select("td a")[0].get_text()

			category = each.select("td")[1].get_text()

			number = each.select("td")[2].get_text()

			location = each.select("td")[3].get_text()

			publishDate = each.select("td")[4].get_text()

			link = self.url + each.select("td a")[0].attrs['href']

			job["positionName"] = positionName

			job["category"] = category

			job["number"] = number

			job["location"] = location

			job["publishDate"] = publishDate

			job["link"] = link

			job_list.append(job)

			print("Job %d was completed"%self.counter)

			self.counter += 1

			print("\n")

		self.write2json(job_list)

	def loadPage(self, page):
		self.pause()
		# https://hr.tencent.com/position.php?keywords=&start=30#a
		num = (page-1) * 10

		start = {"start" : str(num)}

		start = parse.urlencode(start)

		url = self.url + "position.php?keywords=&" + start + "#a"

		req = request.Request(url, headers=self.headers)

		html = urlopen(req).read().decode("utf-8")

		# print(html)
		# with open("tencent.html", "w") as f:
		# 	f.write(html)

		self.parseHtml(html)


	def go(self):
		input("Push the enter to crawl the jobs information")

		while self.switch:
			try:
				self.loadPage(self.page)
			except request.URLError as e:
				print(e.message)
				continue

			haha = input("Push the enter to crawl next page, or type quit to exit")

			print("\n")

			self.page += 1

			if haha == 'quit':
				self.switch = False

				print("%d jobs was crawled. Thanks for use, have a good day, bye!"%self.counter)

				break

if __name__ == "__main__":
	spider = tencent()
	spider.go()