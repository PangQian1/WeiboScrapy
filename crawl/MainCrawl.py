from selenium import webdriver
from database import UserInfo
from database import UserFollowers
from crawl import LoginCrawl
from crawl import FansCrawl
from crawl import ArticleCrawl
from crawl import UserInfoCrawl
from logic import AnalysisLogic
from logic import SklearnLogic
import time

if __name__ == "__main__":

    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()

    user_info = UserInfo.UserInfo()
    user_follower = UserFollowers.UserFollowers()

    # 登录
    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    #获取目标用户id
    goal_ucid = FansCrawl.searchGoalAccount(user_info, driver)


    # 爬取粉丝
    FansCrawl.crawlFanList(goal_ucid, driver)

    #爬取粉丝所有的信息
    print('Start crawling all fans\' information...')
    fan_list = user_follower.searchFansUcid(goal_ucid)
    for fan in fan_list:
        res = 1
        while res:
            res = UserInfoCrawl.crawlUserInfo(fan, driver)


    # 爬取微博
    print('Start crawling Follow Weibo’s Weibo posting')
    ucid_list = user_follower.searchFollowersUcid(goal_ucid)
    num = 0
    for ucid in ucid_list:
        ArticleCrawl.crawlArticle(ucid, driver)
        num = num + 1
        print(num)


    print('Data is crawled!!')
    print('\n**************************************************************************************************************\n')
    print('Start data analysis...')


    # 微博分词
    spilt_article = AnalysisLogic.AnalysisLogic()

    ucid_list = user_follower.searchFollowersUcid(goal_ucid)

    for ucid in ucid_list:
        spilt_article.splitArticle(ucid)


    # 获取分析结果
    sklearn_logic = SklearnLogic.SklearnLogic()

     # 首先计算tfidf矩阵，接下来直接聚类
    weight = sklearn_logic.calculateTFIDF(goal_ucid)
    clf = sklearn_logic.getKmeans(weight)

    result = sklearn_logic.getKeyWords(goal_ucid, clf)
    print(result)


    print('\n\nEnd of information processing~~~~')