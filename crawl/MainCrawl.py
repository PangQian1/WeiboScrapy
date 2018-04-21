from selenium import webdriver
from database import UserInfo
from database import UserFollowers
from crawl import LoginCrawl
from crawl import FansCrawl
from crawl import ArticleCrawl
from crawl import UserInfoCrawl

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
    #FansCrawl.crawlFanList(goal_ucid, driver)

    #input('test')

    #爬取粉丝所有的信息
    user_follower = UserFollowers.UserFollowers()
    fan_list = user_follower.searchFansUcid(goal_ucid)
    for fan in fan_list:
        UserInfoCrawl.crawlUserInfo(fan, driver)
        input('stop')

    input('test2')


    # 爬取微博
    ucid_list = user_follower.searchFollowersUcid(goal_ucid)
    num = 0
    for ucid in ucid_list:
        ArticleCrawl.crawlArticle(ucid, driver)
        num = num + 1
        print(num)