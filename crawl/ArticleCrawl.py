import time
from selenium import webdriver
from crawl import LoginCrawl
from crawl import BaseCrawl
from database import UserInfo
from database import UserArticle

def crawlArticle(ucid, driver):
    user_article = UserArticle.UserArticle()

    user_home_url = 'https://weibo.com/u/' + ucid + '?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2#feedtop'
    driver.get(user_home_url)

    while (True):
        try:
            driver.find_element_by_css_selector('div.W_pages')
            nextPage = True
        except:
            nextPage = False

        if nextPage:
            break
        driver.execute_script("window.scrollBy(0,10000)")
        time.sleep(1)

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
    user_info = UserInfo.UserInfo()

    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)
    crawlArticle('1768305123', driver)


