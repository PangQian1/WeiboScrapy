from selenium import webdriver
from database import UserInfo
from database import UserFollowers
from crawl import LoginCrawl
from crawl import FansCrawl
from crawl import ArticleCrawl

if __name__ == "__main__":

    # 使用谷歌浏览器
    driver = webdriver.Firefox()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    user_info = UserInfo.UserInfo()

    # 登录
    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    # 爬取粉丝
    goal_ucid = FansCrawl.searchGoalAccount(user_info, driver)
    #url_fanList = FansCrawl.locateFanListUrl(driver)
    #FansCrawl.crawlFanList(url_fanList, goal_ucid, user_info, driver)

    # 爬取微博
    user_follower = UserFollowers.UserFollowers()
    ucid_list = user_follower.searchFollowersUcid(goal_ucid)
    for ucid in ucid_list:
        ArticleCrawl.crawlArticle(ucid, driver)