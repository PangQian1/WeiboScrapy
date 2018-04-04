import time
from selenium import webdriver
from crawl import LoginCrawl
from crawl import BaseCrawl
from database import UserArticle
from database import UserFollowers

# 文章爬虫
def crawlArticle(ucid, driver):
    user_article = UserArticle.UserArticle()

    for page in range(3):
        page += 1
        print('UCID:' + ucid)
        print('页数:' + str(page))
        user_home_url = 'https://weibo.com/u/' + ucid + '?is_all=1&page=' + str(page)
        driver.get(user_home_url)

        next = 1
        while (True):
            try:
                driver.find_element_by_css_selector('div.W_pages')
                nextPage = True
            except:
                nextPage = False

            if nextPage:
                break
            driver.execute_script("window.scrollBy(0,10000)")
            # 存在有的微博第一页不全
            next += 1
            if next > 4:
                break
            time.sleep(1)

        articles = driver.find_elements_by_css_selector("div.WB_feed.WB_feed_v3.WB_feed_v4 > div")
        print('文章数量：' + str(len(articles) - 2))
        if len(articles) < 2:
            print('已经爬完该用户文章~' + ucid)
            break

        for article in articles:
            try:
                article.find_element_by_css_selector("a.WB_text_opt").click()
                print('有展开全文')
            except:
                pass

        dealArticles(ucid, articles, user_article)

# 处理爬取下来的文章
def dealArticles(ucid, articles, user_article):
    for article in articles:
        try:
            # 微博ID
            mid = article.get_attribute("mid")
            # 微博发布信息
            publish_tags   = article.find_elements_by_css_selector("div.WB_from.S_txt2 > a")
            publish_time   = publish_tags[0].text
            publish_device = publish_tags[1].text

            article_contents = article.find_elements_by_css_selector("div.WB_text.W_f14")
            print(len(article_contents))
            content = article_contents[0].text
            if len(article_contents) > 1:
                content = article_contents[1].text

            print(content)

            # 文章的转发 点赞 评论
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
    LoginCrawl.loginWeibo('15901057573', 'zs123456', driver)

    # 获取ucid列表
    SDU_ID    = '3237705130'
    user_follower = UserFollowers.UserFollowers()
    ucid_list     = user_follower.searchFollowersUcid(SDU_ID)

    for ucid in ucid_list:
        crawlArticle(ucid, driver)

    # crawlArticle('5983730812', driver)