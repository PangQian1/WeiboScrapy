from selenium import webdriver
from crawl import LoginCrawl
from crawl import Constants
from crawl import BaseCrawl
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

def crawlArticle(ucid, driver):
    user_article = UserArticle.UserArticle()

    user_home_url = 'https://weibo.com/u/1768305123'
    driver.get(user_home_url)

    articles = driver.find_elements_by_css_selector("#Pl_Official_MyProfileFeed__22 > div > div")
    print(len(articles))

    for article in articles:
        try:
            # 微博ID
            mid = article.get_attribute("mid")
            # 微博发布信息
            publish_tags   = article.find_elements_by_css_selector("div.WB_from.S_txt2 > a")
            publish_time   = publish_tags[0].text
            publish_device = publish_tags[1].text

            content = article.find_elements_by_css_selector("div.WB_text.W_f14")[0].text
            content = BaseCrawl.filterEmoji(content)

            article_foot = article.find_elements_by_css_selector("div.WB_handle > ul > li")
            transmit = BaseCrawl.filterNumber(article_foot[1].text)
            comment  = BaseCrawl.filterNumber(article_foot[2].text)
            praise   = BaseCrawl.filterNumber(article_foot[3].text)

            user_article.createUserArticle((ucid,
                                            mid,
                                            content,
                                            publish_time,
                                            publish_device,
                                            transmit,
                                            comment,
                                            praise
                                            ))

        except:
            pass

if __name__ == "__main__":
    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    user_info = UserInfo.UserInfo()

    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)
    crawlArticle('123', driver)


