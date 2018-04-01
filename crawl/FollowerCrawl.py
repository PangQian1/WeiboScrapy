from selenium import webdriver
import re
from database import BaseCursor
from database import UserInfo

#登录微博的过程
def login_weibo(name, password, driver):

    # 输入登录名和密码
    driver.find_element_by_xpath('//*[@id="loginname"]').clear()
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(name)

    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').clear()
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys(password)

    # 点击一下登录按钮使其弹出验证码图片
    # //*[@id="pl_login_form"]/div/div[3]/div[6]/a
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()

    # 获取验证码
    res = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/a/img')
    # print(res)
    # print(res.get_attribute('height'))
    img = res.get_attribute('src')
    print(img)
    identify_code = input('Please input the identify_code:')

    #有些时候不需要验证码，这个时候此地便会报错，直接跳过就好
    try:
        # 将获得的验证码键入网页进行登录
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').clear()
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(identify_code)
        # 再次点击登录
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
    except:
        pass

#进入要研究的微博粉丝列表，并返回url，粉丝的数量，返回的是一个list，可通过下标访问
def get_FanList(driver):
    # 获取想要研究的微博名
    goal_weibo = input('Please input the the weiboName that you want to search:')

    # 在输入框中输入搜索内容并进行搜索
    driver.find_element_by_css_selector('#plc_top > div > div > div.gn_search_v2 > input').send_keys(goal_weibo)
    driver.find_element_by_css_selector('#plc_top > div > div > div.gn_search_v2 > a').click()

    # 搜索成功后，在列表的第一项点击进入粉丝列表
    res = driver.find_element_by_xpath('//*[@id="pl_weibo_directtop"]/div/div/div/div[2]/p[4]/span[2]/a')
    addr_fanList = res.get_attribute('href')
    driver.get(addr_fanList)

    #获取粉丝页的URL，每个微博账户的粉丝URL是有差别的
    url = driver.find_element_by_css_selector('div > div > div > div.follow_box > div.WB_cardpage.S_line1 > div > a.page.next.S_txt1.S_line1')
    url = url.get_attribute('href')

    #获取粉丝数量
    temp = driver.find_element_by_css_selector('div > div > div > div.WB_tab_b > div > ul > li > a > span').text
    str = temp[5:]
    fan_num = int(str)
    #print(fan_num)

    return url, fan_num

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
def get_fanList_url(str, num, driver):
    #承接get_FanList方法的返回值，num是想进入的粉丝列表页数
    pos = str.index('2#')
    str1 = str[0:pos]
    str2 = str[pos+1:]
    str0 = str1 + '%d' + str2
    driver.get(str0 % num)

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

#爬取粉丝列表
def crawl_FanList(url_fanList, database, driver):
    #url_fanList是一个list，第一项是粉丝列表的url，第二项是粉丝的数量
    url = url_fanList[0]
    num = url_fanList[1]
    print('共有%d个粉丝' % num)

    if num < 20:
        pagination = 1
    else:
        t = num % 20
        if t == 0:
            pass
        else:
            t = 1
        pagination = int(num / 20) + t

    print('分为%d页' % pagination)

    for page in range(pagination):
        if page == 5:#5
            break

        get_fanList_url(url, (page + 1), driver)

        fans = driver.find_elements_by_css_selector("ul.follow_list>li")

        # print('本页共有%s个粉丝' % len(fans))

        for fan in fans:
            #try:
            nickname = fan.find_element_by_css_selector('dl>dt>a').get_attribute('title')
            sex0 = fan.get_attribute('action-data')
            sex = get_sex(sex0)
            address = fan.find_element_by_css_selector('dl>dd>div.info_add>span').text

            # print(nickname, sex, address)
            f = Fan.Fan(nickname, sex, address)
            f.storeInfo(database)

            #此处进入继续爬每个粉丝关注的账户
            # 首先保存当前窗口句柄
            firstHandle = driver.current_window_handle
            handleDepot = []
            handleDepot.append(firstHandle)
            fan.find_element_by_css_selector('dl>dd>div.info_connect>span>em>a').click()#打开粉丝关注账户的列表页
            handles = driver.window_handles

            for handle in handles:  # 切换窗口
                if handle != firstHandle:
                    driver.switch_to.window(handle)  # 切换到第二个窗口

            #开始爬取并放入到数据库中
            crawl_account(database, driver)

            #爬取结束之后窗口切换回来并将第二个窗口关闭
            driver.close()
            driver.switch_to_window(firstHandle)

            #except:
             #   print('exception occurred!')

#该方法爬取粉丝关注的所有账户
def crawl_account(database, driver):

    for page in range(5):#5

        accounts = driver.find_elements_by_css_selector("ul.follow_list>li")
        #print(driver.current_url)

        for account in accounts:
            #每一个for循环获取到一页的账户并插入到数据库
            nickname = account.find_element_by_css_selector('dl>dt>a').get_attribute('title')
            temp = account.find_element_by_css_selector('dl>dt>a>img').get_attribute('usercard')

            try:
                accountID = get_ID(temp)
                # print(nickname)
                database.insertIntoRela(accountID, nickname)
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


if __name__ == "_main_":

    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    database = Database.Database_mysql()

    login_weibo('17865169752', '1835896411', driver)
    url_fanList = get_FanList(driver)
    crawl_FanList(url_fanList, database, driver)

















