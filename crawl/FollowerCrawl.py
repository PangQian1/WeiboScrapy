import re
from selenium import webdriver
from database import UserInfo
from crawl import BaseCrawl

#给定参数获取性别  利用字符串操作和正则表达式
def get_sex(str):
    pos = str.index('sex')
    str0 = str[pos:]
    sex = re.match(r'sex=m$', str0)
    #print(sex)
    if(sex):
        return 'm'
    else:
        return 'f'

#给定参数获取用户ID，利用字符串操作
def get_ID(str):
    pos = str.index('&')
    res = str[3:pos]
    return res

#该方法爬取粉丝关注的所有账户
def crawlFollowerList(follower_ucid, user_follower, user_info, driver):

    for page in range(5):#5

        followers = driver.find_elements_by_css_selector("ul.follow_list>li")
        #print(driver.current_url)

        for follower in followers:
            #每一个for循环获取到一页的账户并插入到数据库
            try:
                #可能没有简介
                introduction = follower.find_element_by_css_selector('dl > dd > div.info_intro > span').text
            except:
                introduction = ''

            try:
                ucid_tag = follower.find_element_by_css_selector('dl>dt>a>img').get_attribute('usercard')
                ucid     = BaseCrawl.getID(ucid_tag)
                name     = follower.find_element_by_css_selector('dl>dt>a').get_attribute('title')
                sex_str  = follower.get_attribute('action-data')
                sex      = BaseCrawl.getSex(sex_str)
                address  = follower.find_element_by_css_selector('dl > dd > div.info_add > span').text

                data_userFollower = (ucid, follower_ucid)
                user_follower.createUserFollower(data_userFollower)

                #同时更新weibo_user_info表
                data_userInfo = (ucid, name, sex, address, '', introduction)
                user_info.createUserInfo(data_userInfo)

            except:
                print('出现假账户！')

        #input('测试部分！')
        if page == 4:#如果page为4，爬的即是第五页，第六页已经不能访问，后续不须进行，网页加载浪费时间
            break

        try:
            #一页爬取完后进入到下一页，最多五页
            p = driver.find_element_by_css_selector('div > div > div > div.follow_box > div.WB_cardpage.S_line1 > div > a.page.next.S_txt1.S_line1')
            link = p.get_attribute('href')
            driver.get(link)
        except:
            #一旦发生异常表示没有下一页，关注账户数目不足五页，退出循环
            #print('爬取结束，粉丝数目不足五页！！')
            break


if __name__ == "__main__":

    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    user_info = UserInfo.UserInfo()
