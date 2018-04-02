from selenium import webdriver
from crawl import FansCrawl
from crawl import LoginCrawl
from crawl import Constants
from database import UserInfo
from database import UserArticle

def searchFollowers(goal_ucid, driver):
    user_article = UserArticle.UserArticle()
    followers_ucid = user_article.searchFollowersUcid(goal_ucid)

    for follower_ucid in followers_ucid:

        follower_ucid = str(follower_ucid[0])
        if follower_ucid == goal_ucid:
            continue

        driver.find_element_by_css_selector(Constants.dict['search_box_css']).clear()
        driver.find_element_by_css_selector(Constants.dict['search_box_css']).send_keys(follower_ucid)
        driver.find_element_by_css_selector(Constants.dict['search_button_css']).click()
        input('test')

def crawlArticle(home_url, driver):




 if __name__ == "__main__":
    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    user_info = UserInfo.UserInfo()

    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    goal_ucid = FansCrawl.searchGoalAccount(user_info, driver)



