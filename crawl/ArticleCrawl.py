from selenium import webdriver
from web_crawl import dataOfFan
import time

if __name__ == "__main__":
    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    dataOfFan.login_weibo('17865169752', '1835896411', driver)
    driver.find_element_by_css_selector('#plc_top > div > div > div.gn_search_v2 > a').click()
    time.sleep(5)

    driver.find_element_by_css_selector('#pl_common_searchTop > div.search_topic > div > ul > li:nth-child(2) > a').click()
    driver.find_element_by_css_selector('#pl_common_searchTop > div.search_head.clearfix > div.search_head_formbox > div.search_input > div > div.searchInp_box > div > input').send_keys()

