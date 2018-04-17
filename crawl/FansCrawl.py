from selenium import webdriver
from database import UserInfo
from database import UserFollowers
from crawl import FollowerCrawl, LoginCrawl
from crawl import BaseCrawl

#进入要研究的微博粉丝列表，账户的id
def searchGoalAccount(user_info, driver):
    # 获取想要研究的微博名
    goal_weibo = input('Please input the the weiboName that you want to search:')

    # 在输入框中输入搜索内容并进行搜索
    driver.find_element_by_css_selector('#plc_top > div > div > div.gn_search_v2 > input').send_keys(goal_weibo)
    driver.find_element_by_css_selector('#plc_top > div > div > div.gn_search_v2 > a').click()
    driver.find_element_by_css_selector('#pl_common_searchTop > div.search_topic > div > ul > li:nth-child(2) > a').click()
    #driver.find_element_by_css_selector('#pl_common_searchTop > div.search_head.clearfix > div.search_head_formbox > div.search_input > div > div.searchBtn_box > div > a').click()

    #找到后，获取账号的ucid
    ucid_str = driver.find_element_by_css_selector('#pl_user_feedList > div:nth-child(1) > div > div > div > div:nth-child(1) > div.person_pic > a > img').get_attribute('usercard')
    ucid     = BaseCrawl.getID(ucid_str)
    name     = driver.find_element_by_css_selector('#pl_user_feedList > div:nth-child(1) > div > div > div > div:nth-child(1) > div.person_detail > p.person_name > a.W_texta.W_fb > em').text
    address  = driver.find_element_by_xpath('//*[@id="pl_user_feedList"]/div[1]/div/div/div/div[1]/div[3]/p[2]/span[2]').text

    sex_str  = driver.find_element_by_xpath('//*[@id="pl_user_feedList"]/div[1]/div/div/div/div[1]/div[3]/p[2]/span[1]').get_attribute('class')
    if sex_str == 'male m_icon':
        sex = 'm'
    else:
        sex = 'f'

    try:
        introduction = driver.find_element_by_xpath('//*[@id="pl_user_feedList"]/div[1]/div/div/div/div[1]/div[3]/p[3]').text
    except:
        introduction = ''

    data = (ucid, name, sex, address, '', introduction)
    user_info.createUserInfo(data)

    return ucid

#定位到目标账户的粉丝列表页，并且获取粉丝数目，返回粉丝的url，返回的是一个list，可通过下标访问内容
def locateFanListUrl(driver):

    # 搜索成功后，在列表的第一项点击进入粉丝列表
    res = driver.find_element_by_css_selector('#pl_user_feedList > div:nth-child(1) > div > div > div > div:nth-child(1) > div.person_detail > p.person_num > span:nth-child(2) > a')
    addr_fanList = res.get_attribute('href')
    driver.get(addr_fanList)
    #input('test1')

    #获取粉丝页的URL，每个微博账户的粉丝URL是有差别的
    url = driver.find_element_by_css_selector('div.follow_inner > ul > li > a.S_txt1')
    url = url.get_attribute('href')

    #获取粉丝数量
    temp = driver.find_element_by_css_selector('div > div > div > div.WB_tab_b > div > ul > li > a > span').text
    str = temp[5:]
    fan_num = int(str)
    #print(fan_num)

    return url, fan_num

#爬取粉丝列表
def crawlFanList(ucid, driver):
    user_info = UserInfo.UserInfo()
    #url_fanList是一个list，第一项是粉丝列表的url，第二项是粉丝的数量
    # url = url_fanList[0]
    # num = url_fanList[1]
    # print('共有%d个粉丝' % num)
    #
    # if num < 20:
    #     pagination = 1
    # else:
    #     t = num % 20
    #     if t == 0:
    #         pass
    #     else:
    #         t = 1
    #     pagination = int(num / 20) + t
    #
    # print('分为%d页' % pagination)

    for page in range(5):
        if page == 5: #5
            break

        # getFanListUrl(url, (page + 1), driver)
        #input('test2')
        driver.get('https://weibo.com/p/' + ucid +'/follow?relate=fans&page=' + page)
        fans = driver.find_elements_by_css_selector("ul.follow_list>li")

        print('本页共有%s个粉丝' % len(fans))
        for fan in fans:

            ucid_str  = fan.find_element_by_css_selector('div > div > div > div.follow_box > div.follow_inner > ul > li > dl > dt > a > img').get_attribute('usercard')
            fans_ucid = BaseCrawl.getID(ucid_str)
            name      = fan.find_element_by_css_selector('dl>dt>a').get_attribute('title')
            sex_str   = fan.get_attribute('action-data')
            sex       = BaseCrawl.getSex(sex_str)
            address   = fan.find_element_by_css_selector('dl > dd > div.info_add > span').text

            try:
                #可能没有简介
                introduction = fan.find_element_by_css_selector('dl > dd > div.info_intro > span').text
            except:
                introduction = ''

            data_userInfo = (fans_ucid, name, sex, address, '', BaseCrawl.filterEmoji(introduction))
            user_info.createUserInfo(data_userInfo)

            #同时更新weibo_user_follower表
            user_follower     = UserFollowers.UserFollowers()
            data_userFollower = (ucid, fans_ucid)
            user_follower.createUserFollower(data_userFollower)

            # 此处进入继续爬每个粉丝关注的账户
            # 首先保存当前窗口句柄
            firstHandle = driver.current_window_handle
            #handleDepot = []
            #handleDepot.append(firstHandle)
            try:
                fan.find_element_by_css_selector('dl> dd > div.info_connect> span > em > a').click()  # 打开粉丝关注账户的列表页
                handles = driver.window_handles

                for handle in handles:  # 切换窗口
                    if handle != firstHandle:
                        driver.switch_to.window(handle)  # 切换到第二个窗口
            except:
                pass

            #开始爬取粉丝关注的人并放入到数据库中
            FollowerCrawl.crawlFollowList(fans_ucid, driver)

            #爬取结束之后窗口切换回来并将第二个窗口关闭
            driver.close()
            #input('test3')
            driver.switch_to_window(firstHandle)

            #except:
            # print('exception occurred!')

'''
https://weibo.com/1880883723/fans?refer_flag=1001030101_  山东大学
https://weibo.com/p/1002061880883723/follow?relate=fans&page=1#Pl_Official_HisRelation__50
https://weibo.com/p/1002061880883723/follow?relate=fans&page=3#Pl_Official_HisRelation__50
https://weibo.com/1676317545/fans?refer_flag=1001030101_  清华大学
https://weibo.com/p/1002061676317545/follow?relate=fans&page=2#Pl_Official_HisRelation__50
https://weibo.com/2009178141/fans?refer_flag=1001030101_  个人账户
https://weibo.com/p/1005052009178141/follow?relate=fans&page=2#Pl_Official_HisRelation__59
'''
#对粉丝列表的URL分析确定页数
def getFanListUrl(url, num, driver):
    #承接get_FanList方法的返回值，num是想进入的粉丝列表页数
    pos = url.index('2#')
    str1 = url[0:pos]
    str2 = url[pos + 1:]
    str0 = str1 + '%d' + str2
    driver.get(str0 % num)

if __name__ == "__main__":
    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    user_info = UserInfo.UserInfo()
    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    # ucid = searchGoalAccount(user_info, driver)
    # url_fanList = locateFanListUrl(driver)
                                               
    crawlFanList('1004061223178222', driver)
