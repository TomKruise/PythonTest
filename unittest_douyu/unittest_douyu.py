import unittest
import time

from selenium import webdriver
from bs4 import BeautifulSoup


class douyu(unittest.TestCase):
	def setUp(self):
		self.chrome = webdriver.Chrome()

	def testDouyu(self):
		self.chrome.get("http://www.douyu.com/directory/all")
		while True:
			time.sleep(2)

			soup = BeautifulSoup(self.chrome.page_source, "lxml")

			titles = soup.find_all('h3', {'class': 'ellipsis'})

			numbers = soup.find_all('span', {'class': 'dy-num fr'})

			for title, number in zip(titles, numbers):
				print("Room title: %s, viewer %s"%(title.get_text().strip(), number.get_text().strip()))

			if self.chrome.page_source.find('shark-pager-next shark-pager-disable shark-pager-disable-next') != -1:
				break

			self.chrome.find_element_by_class_name('shark-pager-next').click()

	def tearDown(self):
		print("Page loaded")
		self.chrome.quit()

if __name__ == "__main__":
	unittest.main()