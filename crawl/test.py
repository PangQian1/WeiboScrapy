import time
from selenium import webdriver
from database import UserInfo

driver = webdriver.Chrome()
driver.get('http://weibo.com/login.php')
driver.maximize_window()

# js = "var q = document.body.scrollTop=100000"
# driver.execute_script(js)

