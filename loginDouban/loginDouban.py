from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()

browser.get("http://www.douban.com")

email = input("Type your email: ")

password = input("Type your password: ")

browser.find_element_by_name("form_email").send_keys(email)

browser.find_element_by_name("form_password").send_keys(password)

browser.find_element_by_xpath("//input[@class='bn-submit']").click()

time.sleep(3)

browser.save_screenshot("douban.png")

with open("douban.html", "w") as f:
	f.write(browser.page_source)

browser.quit()