# coding:utf-8
from urllib import parse
from urllib import request
from lxml import etree
from urllib.request import urlopen
from os import path
# from lxml.etree import HTMLParser

import os
import time
import random


class tieba(object):
	def __init__(self):
		self.headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}
		self.counter = 1
		self.tiebaName = ''
		self.dirs = ''

	def loadPage(self, keyword, page):
		# http://tieba.baidu.com/f?kw=python3&ie=utf-8&pn=50
		# pn = (page-1) * 50
		print("Start to load page %d"%page)

		print("\n")

		second = random.randint(1, 3)

		time.sleep(second)

		pn = (page -1) * 50

		kw = {'kw' : keyword}

		kw = parse.urlencode(kw)

		url = "http://tieba.baidu.com/f?" + kw + "&ie=utf-8&pn=" + str(pn)

		# print(url)

		req = request.Request(url, headers = self.headers)

		# print("haha")

		html = urlopen(req).read().decode('utf-8').replace('<!--', '').replace('-->', '')

		# with open("tieba.html", 'wb') as f:
		# 	f.write(html)

		# print(html)

		html = etree.HTML(html) # From string to HTML

		# print(html)

		# http://tieba.baidu.com/p/5850502928
		"""
		<a rel="noreferrer" href="/p/5850502928" title="怎么下载xml模块，求链接求教" target="_blank" class="j_th_tit ">怎么下载xml模块，求链接求教</a>
		"""
		list = html.xpath("//div[@class='t_con cleafix']/div/div[@class='threadlist_lz clearfix']/div/a/@href")

		# print(list)

		for link in list:
			link = "http://tieba.baidu.com" + link
			# print(link)
			self.loadImage(link)

	def loadImage(self, link):
		print("Ready to load images` link")

		print("\n")

		req = request.Request(link, headers=self.headers)

		html = urlopen(req).read()

		# with open("tieba.html", 'wb') as f:
		# 	f.write(html)

		# print(html)

		html = etree.HTML(html)

		list = html.xpath('//div[@class="d_post_content j_d_post_content "]/img/@src')

		# print(list)

		print("Load completed")

		print("\n")

		for link in list:
			self.writeImage(link)

	def writeImage(self, link):
		print("Downloading picture %d"%self.counter)

		print("\n")

		file = open(self.dirs + str(self.counter) + '.png', 'wb')

		image = urlopen(link).read()

		file.write(image)

		file.close()

		print("Picture downloaded")

		print("\n")

		self.counter += 1


	def progress(self, page):
		print("Page %s was downloaded"%page)



	def go(self):
		self.page = 1

		self.switch = True

		keyword = input("Type the tieba name what you like, then we will download the images from that website.")

		self.tiebaName = keyword

		self.dirs = './images/' + self.tiebaName + '/'

		if not path.exists(self.dirs):

			os.makedirs(self.dirs)

		while self.switch:
			try:
				self.loadPage(keyword, self.page)

			except request.URLError as e:
				print(e.message)
				continue

			self.progress(self.page)

			print("Type quit to exit, or push the enter to continue!")

			hehe = input()

			self.page += 1

			if hehe == "quit":
				self.switch = False

				print("Downloaded %d pictures, thanks for use, bye!"%self.counter)

				break




if __name__ == "__main__":
	spider = tieba()
	spider.go()