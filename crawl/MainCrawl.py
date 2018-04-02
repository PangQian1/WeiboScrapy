from selenium import webdriver
from database import UserInfo
from crawl import LoginCrawl
from crawl import FansCrawl

if __name__ == "__main__":

    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    user_info = UserInfo.UserInfo()

    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    goal_ucid = FansCrawl.searchGoalAccount(user_info, driver)
    url_fanList = FansCrawl.locateFanListUrl(driver)
    FansCrawl.crawlFanList(url_fanList, goal_ucid, user_info, driver)
