import time
from selenium import webdriver
from crawl import LoginCrawl
from crawl import BaseCrawl
from database import UserArticle
from database import UserFollowers
import traceback

# 文章爬虫
def crawlArticle(ucid, driver):
    user_article = UserArticle.UserArticle()

    for page in range(1000000):
        page += 1
        #print('UCID:' + ucid)
        #print('页数:' + str(page))
        user_home_url = 'https://weibo.com/u/' + ucid + '?is_all=1&page=' + str(page)

        driver.get(user_home_url)

        next = 1
        nextPage = False
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
            if next > 5:
                break
            time.sleep(2)

        articles = driver.find_elements_by_css_selector("div.WB_feed.WB_feed_v3.WB_feed_v4 > div")
        #print('文章数量：' + str(len(articles) - 3))

        if len(articles) <= 3:
            #print('已经爬完该用户文章~' + ucid)
            break

        for article in articles:

            try:
                article.find_element_by_css_selector("a.WB_text_opt").click()
                #print('有展开全文')
            except:
                pass


            '''
            try:
                spread = article.find_element_by_css_selector("div.WB_feed_detail.clearfix > div.WB_detail > div.WB_feed_expand > div.WB_expand.S_bg1 > div.WB_text > a")
                spread.click()
                print('转发有展开全文')
            except:
                print('traceback.format_exc():\n%s' % traceback.format_exc())

        
            try:
                expand_articles = article.find_elements_by_css_selector("a.WB_text_opt")

                for value in expand_articles:
                    value.click()
                    print('有展开全文')
            except:
                print('没有展开全文')

            '''


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

            # 获取文章内容
            article_contents = article.find_elements_by_css_selector("div.WB_text.W_f14")
            #print(len(article_contents))
            content = article_contents[0].text
            if len(article_contents) > 1:
                content = article_contents[1].text
            #print(content)

            # 获取转发文章的内容
            try:
                article_expand = article.find_elements_by_css_selector("div.WB_feed_detail.clearfix > div.WB_detail > div.WB_feed_expand > div.WB_expand.S_bg1 > div.WB_text")
                #print(len(article_expand))
                content += article_expand[0].text

                if len(article_expand) > 1:
                    content += article_expand[1].text
                #print('转发微博')
            except:
                #print('traceback.format_exc():\n%s' % traceback.format_exc())
                pass
            content = BaseCrawl.filterEmoji(content)

            #print(content)

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
    driver = webdriver.Firefox()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    #LoginCrawl.loginWeibo('15901057573', 'zs123456', driver)
    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    # 获取ucid列表
    #SDU_ID    = '3237705130'
    #user_follower = UserFollowers.UserFollowers()
    #ucid_list     = user_follower.searchFollowersUcid(SDU_ID)

    # for ucid in ucid_list:
    #     crawlArticle(ucid, driver)

    crawlArticle('5359730794', driver)#5702552653