import time
from selenium import webdriver
from database import UserInfo
from crawl import LoginCrawl

# 爬取个人信息
def crawlUserInfo(ucid, driver):
    user_info     = UserInfo.UserInfo()

    user_url = 'https://weibo.com/' + str(ucid)
    driver.get(user_url)
    time.sleep(3)

    # 获取是否是认证微博
    try:
        driver.find_elements_by_css_selector("div.verify_area.W_tog_hover.S_line2 > p.verify.clearfix > span.icon_bed.W_fl > a")
        is_verify = 2
        #print('认证微博')
    except:
        is_verify = 1
        #print('未认证微博')

    # 获取个人信息详情页
    #user_info_url = driver.find_element_by_css_selector("#Pl_Core_UserInfo__6 > div > div.WB_cardwrap.S_bg2 > a.WB_cardmore.S_txt1.S_line1.clearfix").get_attribute('href')
    #print(user_info_url)
    user_info_url = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[4]/div/div/a').get_attribute('href')
    driver.get(user_info_url)

    # 关注 & 粉丝 & 微博
    follow_number = driver.find_element_by_css_selector(
        'div > div > div > table > tbody > tr > td:nth-child(1) > a > strong').text
    follower_number = driver.find_element_by_css_selector(
        'div > div > div > table > tbody > tr > td:nth-child(2) > a > strong').text
    weibo_number = driver.find_element_by_css_selector(
        'div > div > div > table > tbody > tr > td:nth-child(3) > a > strong').text

    # 注册时间
    sign_up_time = ''
    try:
        info_results = driver.find_elements_by_css_selector(
            "div:nth-child(1) > div > div.WB_innerwrap > div > ul > li")
        if len(info_results) > 0:
            sign_up_time = info_results[-1].text.replace('注册时间：', '').strip()
        else:
            #print('没有注册时间')
            pass
    except:
        #print('没有注册时间')
        pass

    # 用户等级
    level_text = driver.find_element_by_css_selector(
        "div > div > div > div:nth-child(2) > div > div.WB_innerwrap > div > div > a").text
    level = level_text.replace('Lv.', '').strip()

    #用户标签
    #try:
    model = driver.find_elements_by_css_selector('div.WB_frame_c > div.WB_cardwrap S_bg2')
    print(len(model))
    if len(model) > 1:

        num = 0
        for bg in model:

            num = num + 1

            if num == len(model):
                tags_text = bg.find_element_by_css_selector("div > div.WB_innerwrap > div > ul > li").text

                try:
                    index = tags_text.index('标签')
                    tags = tags_text.replace("\n标签：", '').replace('\n', ',')
                except:
                    tags = ''

    else:
        tags = ''
    #except:
     #   tags = ''

    print(follow_number)
    print(follower_number)
    print(weibo_number)
    print(level)
    print(sign_up_time)
    print(is_verify)
    print(tags)

    # 更新用户信息
    data_userInfo = (follow_number, follower_number, weibo_number, level, sign_up_time, is_verify, tags)
    sql = "UPDATE weibo_user_info SET " \
          "follow_number = '%s', " \
          "follower_number = '%s', " \
          "weibo_number = '%s', " \
          "level = '%s', " \
          "sign_up_time = '%s', " \
          "is_verify = '%s', " \
          "tags = '%s'" \
          "WHERE ucid = " + ucid
    user_info.executeSql(sql, data_userInfo)

    time.sleep(3)

if __name__ == "__main__":
    user_info = UserInfo.UserInfo()
    user_list = user_info.getUserInfoList(('ucid'))

    # 使用谷歌浏览器
    driver = webdriver.Firefox()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    # 登录
    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    time.sleep(5)
    crawlUserInfo('1049198655', driver)

    # for value in user_list:
    #     crawlUserInfo(value['ucid'], driver)